import re
import threading
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Any

from data import (
    obtener_todos_los_grados,
    obtener_horarios_disponibles,
    leer_citas,
    buscar_grado_por_id,
    verificar_cita_existente,
    crear_cita,
    eliminar_cita,
    obtener_rol_admin,
    reprogramar_cita
)
from email_utils import enviar_correo_confirmacion, enviar_correo_docente

router = APIRouter(prefix="/api")

# Modelo de Pydantic para validar los datos de la cita recibida
class CitaSchema(BaseModel):
    acudiente: str = Field(..., min_length=2, description="Nombre completo del acudiente")
    telefono: str = Field(..., min_length=7, description="Número de teléfono de contacto")
    correo: str = Field(..., description="Correo electrónico de contacto")
    estudiante: str = Field(..., min_length=2, description="Nombre completo del estudiante")
    grado: str = Field(..., description="Grado seleccionado")
    horario: str = Field(..., description="Horario seleccionado")

# Modelo de Pydantic para el inicio de sesión administrativo
class LoginSchema(BaseModel):
    usuario: str = Field(..., min_length=1, description="Nombre de usuario del administrativo")
    contrasena: str = Field(..., min_length=1, description="Contraseña del administrativo")

# Modelo de Pydantic para reprogramar citas
class ReprogramarCitaSchema(BaseModel):
    grado_actual: str = Field(..., description="ID actual del docente/grado")
    grado_nuevo: str = Field(..., description="Nuevo ID del docente/grado")
    horario_actual: str = Field(..., description="Horario actual de la cita")
    horario_nuevo: str = Field(..., description="Nuevo horario solicitado")

# Expresión regular sencilla para validar el formato de correo electrónico sin dependencias adicionales
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

@router.get("/grados", response_model=List[Dict[str, str]])
def list_grados():
    """
    Retorna la lista de todos los grados con su grupo y docente asignado.
    """
    return obtener_todos_los_grados()

@router.get("/horarios/{grado}", response_model=Dict[str, Any])
def get_horarios(grado: str):
    """
    Retorna el docente y los horarios disponibles para el grado especificado.
    Lanza error 404 si el grado no existe.
    """
    horarios_info = obtener_horarios_disponibles(grado)
    if not horarios_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El grado '{grado}' no está registrado en el sistema."
        )
    return horarios_info

@router.post("/citas", response_model=Dict[str, Any])
def create_cita(cita: CitaSchema):
    """
    Registra una nueva cita si pasa todas las validaciones:
    - Campos obligatorios no vacíos (manejado por Pydantic y validación manual de espacios).
    - Email con formato correcto.
    - El grado especificado debe existir.
    - El horario debe ser uno de los horarios base del grado.
    - Evita reservas duplicadas: el horario para este grado no debe estar ya reservado.
    """
    # Limpieza de espacios en blanco al inicio y al final de los textos
    acudiente = cita.acudiente.strip()
    telefono = cita.telefono.strip()
    correo = cita.correo.strip()
    estudiante = cita.estudiante.strip()
    grado_id = cita.grado.strip()
    horario = cita.horario.strip()

    # Validaciones manuales de campos obligatorios para asegurar que no contengan solo espacios
    if not acudiente or not telefono or not correo or not estudiante or not grado_id or not horario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Todos los campos son obligatorios y no deben contener únicamente espacios."
        )

    # Validación de formato de correo electrónico
    if not EMAIL_REGEX.match(correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo electrónico ingresado no tiene un formato válido."
        )

    # Validar que el grado exista en el sistema
    grado_info = buscar_grado_por_id(grado_id)
    if not grado_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El grado '{grado_id}' no existe."
        )

    # Validar que el horario propuesto pertenezca a los horarios base de ese grado
    if horario not in grado_info["horarios_base"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El horario '{horario}' no pertenece al cronograma del docente asignado al grado {grado_id}."
        )

    # Evitar reservas duplicadas: verificar si ya existe una cita registrada para ese grado y horario
    if verificar_cita_existente(grado_id, horario):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El horario '{horario}' para el grado {grado_id} ya ha sido reservado por otro acudiente."
        )

    # Crear la nueva cita y guardarla en la base de datos
    if not crear_cita(acudiente, telefono, correo, estudiante, grado_id, horario):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al intentar guardar la cita en la base de datos."
        )

    # Enviar correo de confirmacion en segundo plano sin bloquear la respuesta HTTP.
    # Se ejecuta en un hilo separado para que posibles demoras del servidor SMTP
    # no afecten el tiempo de respuesta del endpoint.
    hilo_correo = threading.Thread(
        target=enviar_correo_confirmacion,
        kwargs={
            "destinatario": correo,
            "acudiente": acudiente,
            "estudiante": estudiante,
            "grado": grado_id,
            "grupo": grado_info["grupo"],
            "docente": grado_info["docente"],
            "horario": horario,
            "telefono": telefono
        },
        daemon=True
    )
    hilo_correo.start()

    # Enviar notificacion al docente si tiene correo configurado
    correo_docente = grado_info.get("correo")
    if correo_docente:
        hilo_correo_docente = threading.Thread(
            target=enviar_correo_docente,
            kwargs={
                "correo_docente": correo_docente,
                "docente": grado_info["docente"],
                "acudiente": acudiente,
                "estudiante": estudiante,
                "grado": grado_id,
                "grupo": grado_info["grupo"],
                "horario": horario,
                "telefono": telefono
            },
            daemon=True
        )
        hilo_correo_docente.start()

    return {
        "success": True,
        "message": "Agendamiento registrado correctamente. Se ha enviado un correo de confirmacion a su direccion de correo electronico."
    }

@router.get("/citas", response_model=List[Dict[str, Any]])
def list_citas():
    """
    Retorna la lista completa de todas las citas agendadas y guardadas.
    """
    return leer_citas()

@router.delete("/citas")
def delete_cita(grado: str, horario: str):
    """
    Cancela un agendamiento existente buscando por grado y horario.
    """
    grado_id = grado.strip()
    horario_str = horario.strip()

    if not verificar_cita_existente(grado_id, horario_str):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró ningún agendamiento para el grado y horario especificados."
        )

    if not eliminar_cita(grado_id, horario_str):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al intentar guardar los cambios en la base de datos."
        )

    return {
        "success": True,
        "message": "El agendamiento ha sido cancelado con éxito y el horario ha sido liberado."
    }

@router.post("/login")
def login(credentials: LoginSchema):
    """
    Autentica a un administrativo con usuario y contraseña y retorna su rol.
    """
    rol = obtener_rol_admin(credentials.usuario, credentials.contrasena)
    if rol:
        return {
            "success": True,
            "message": "Inicio de sesión exitoso",
            "rol": rol
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )

@router.put("/citas/reprogramar")
def route_reprogramar_cita(payload: ReprogramarCitaSchema):
    """
    Reprograma un agendamiento liberando el horario anterior y validando el nuevo.
    """
    grado_actual = payload.grado_actual.strip()
    grado_nuevo = payload.grado_nuevo.strip()
    horario_actual = payload.horario_actual.strip()
    horario_nuevo = payload.horario_nuevo.strip()
    
    # Validar disponibilidad
    if verificar_cita_existente(grado_nuevo, horario_nuevo):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El horario '{horario_nuevo}' ya se encuentra reservado para este grado."
        )
        
    # Intentar la reprogramación en base de datos
    if not reprogramar_cita(grado_actual, grado_nuevo, horario_actual, horario_nuevo):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al intentar reprogramar la cita en la base de datos."
        )
        
    # (Opcional) Se podría enviar correo aquí, pero la respuesta confirma el éxito de la transacción
    
    return {
        "success": True,
        "message": "La cita ha sido reprogramada con éxito."
    }
