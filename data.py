import os
import json
from typing import List, Dict, Any

# Ruta al archivo de persistencia de citas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CITAS_FILE_PATH = os.path.join(BASE_DIR, "citas.txt")

# Fechas de atencion: miercoles 8 y jueves 9 de julio de 2026
FECHAS_ATENCION = [
    {"etiqueta": "Mié 8/Jul", "fecha": "2026-07-08"},
    {"etiqueta": "Jue 9/Jul", "fecha": "2026-07-09"},
]

# Franjas horarias base de 7 AM a 3 PM (incluyendo las 15:00) con intervalos de 15 minutos
HORAS_BASE = []
for h in range(7, 16):
    for m in ["00", "15", "30", "45"]:
        if h == 15 and m != "00":
            break
        HORAS_BASE.append(f"{h:02d}:{m}")

# Franja de almuerzo excluida por grupo
# Grupo A: no atiende de 12:00 a 12:45
# Grupo B: no atiende de 13:00 a 13:45
ALMUERZO = {
    "A": "12",
    "B": "13"
}


def generar_horarios(grupo: str) -> List[str]:
    """
    Genera la lista completa de franjas horarias disponibles para los dos dias
    de atencion, excluyendo la hora de almuerzo correspondiente al grupo.
    El formato de cada slot es: 'Mie 8/Jul 07:00' o 'Jue 9/Jul 07:00'.
    """
    prefijo_excluido = ALMUERZO.get(grupo, "")
    slots = []
    for fecha in FECHAS_ATENCION:
        for hora in HORAS_BASE:
            if prefijo_excluido and hora.startswith(f"{prefijo_excluido}:"):
                continue
            slots.append(f"{fecha['etiqueta']} {hora}")
    return slots


# Base de datos del personal asignado para el proceso de matriculas 2026-2027.
# Cada entrada incluye un identificador unico, nombre del funcionario, area asignada y grupo.
PERSONAL_DB = [
    {"id": "1",  "docente": "Mónica Moreno",         "area": "Coordinación de Auditoría",    "grupo": "A", "correo": None},
    {"id": "2",  "docente": "Daniela Gordillo",       "area": "Auditoría",                    "grupo": "A", "correo": None},
    {"id": "3",  "docente": "Juan Pablo",              "area": "Auditoría",                    "grupo": "A", "correo": None},
    {"id": "4",  "docente": "Johny Julián Ospina",    "area": "Auditoría",                    "grupo": "A", "correo": "johnyospina@comfandi.edu.co"},
    {"id": "5",  "docente": "Lorena Burbano",          "area": "Auditoría",                    "grupo": "A", "correo": "lorenaburbano@comfandi.edu.co"},
    {"id": "6",  "docente": "Sofía Vargas",            "area": "Auditoría",                    "grupo": "A", "correo": "sofiavargas@comfandi.edu.co"},
    {"id": "7",  "docente": "Yuli Figueroa",           "area": "Auditoría",                    "grupo": "A", "correo": "yulifigueroa@comfandi.edu.co"},
    {"id": "8",  "docente": "Zandra Rodríguez",        "area": "Auditoría",                    "grupo": "A", "correo": "zandrarodriguez@comfandi.edu.co"},
    {"id": "9",  "docente": "Yulieth Pulgarín",        "area": "Matrículas - Grado Primero",   "grupo": "A", "correo": "yuliethpulgarin@comfandi.edu.co"},
    {"id": "10", "docente": "Yoselin Clavijo",         "area": "Matrículas - Grado Primero",   "grupo": "A", "correo": "yoselinclavijo@comfandi.edu.co"},
    {"id": "11", "docente": "Valery de Jesús",         "area": "Matrículas - Grado Segundo",   "grupo": "A", "correo": "valerydejesus@comfandi.edu.co"},
    {"id": "12", "docente": "Alejandra Méndez",        "area": "Matrículas - Grado Segundo",   "grupo": "A", "correo": "alejandramendez@comfandi.edu.co"},
    {"id": "13", "docente": "Óscar Gómez Peña",        "area": "Matrículas - Grado Tercero",   "grupo": "A", "correo": "oscargomez@comfandi.edu.co"},
    {"id": "14", "docente": "Brandon David Muñoz",     "area": "Matrículas - Grado Tercero",   "grupo": "A", "correo": "brandonmunoz@comfandi.edu.co"},
    {"id": "15", "docente": "Carolina Ortiz",          "area": "Matrículas - Grado Cuarto",    "grupo": "A", "correo": "carolinaortiz@comfandi.edu.co"},
    {"id": "16", "docente": "Eubeimar Samboni",        "area": "Matrículas - Grado Cuarto",    "grupo": "A", "correo": "hernandosamboni@comfandi.edu.co"},
    {"id": "17", "docente": "Jenny Salas",             "area": "Matrículas - Grado Quinto",    "grupo": "A", "correo": "jennysalas@comfandi.edu.co"},
    {"id": "18", "docente": "Juan David Celis",        "area": "Matrículas - Grado Quinto",    "grupo": "B", "correo": "juandavidcelisruiz@comfandi.edu.co"},
    {"id": "19", "docente": "Maritza Muñoz",           "area": "Matrículas - Grado Sexto",     "grupo": "B", "correo": "maritzamunoz@comfandi.edu.co"},
    {"id": "20", "docente": "Faber Tenorio",           "area": "Matrículas - Grado Sexto",     "grupo": "B", "correo": "fabertenorio@comfandi.edu.co"},
    {"id": "21", "docente": "Alejandro Londoño",       "area": "Matrículas - Grado Séptimo",   "grupo": "B", "correo": "luisalejandrolondono@comfandi.edu.co"},
    {"id": "22", "docente": "Vanessa García",          "area": "Matrículas - Grado Séptimo",   "grupo": "B", "correo": "vanessagarcia@comfandi.edu.co"},
    {"id": "23", "docente": "Catalina Quijano",        "area": "Matrículas - Grado Octavo",    "grupo": "B", "correo": "catalinaquijano@comfandi.edu.co"},
    {"id": "24", "docente": "Ricardo Palacios",        "area": "Matrículas - Grado Octavo",    "grupo": "B", "correo": "ricardopalacio@comfandi.edu.co"},
    {"id": "25", "docente": "Gustavo Montaña",         "area": "Matrículas - Grado Octavo",    "grupo": "B", "correo": "gustavomontana@comfandi.edu.co"},
    {"id": "26", "docente": "Andrés Amariles",         "area": "Matrículas - Grado Noveno",    "grupo": "B", "correo": "leonelamariles@comfandi.edu.co"},
    {"id": "27", "docente": "Ana María Osorio",        "area": "Matrículas - Grado Noveno",    "grupo": "B", "correo": "anamariaadarme@comfandi.edu.co"},
    {"id": "28", "docente": "Carlos Hernán Méndez",    "area": "Matrículas - Grado Décimo",    "grupo": "B", "correo": "carlosmendez@comfandi.edu.co"},
    {"id": "29", "docente": "Bdahian Libeth",          "area": "Matrículas - Grado Décimo",    "grupo": "B", "correo": "dahianlibhetortiz@comfandi.edu.co"},
    {"id": "30", "docente": "Diana Carabalí",          "area": "Matrículas - Grado Once",      "grupo": "B", "correo": "dianacarabali@comfandi.edu.co"},
    {"id": "31", "docente": "Geraldine Ospina",        "area": "Matrículas - Grado Once",      "grupo": "B", "correo": "geraldinelopez@comfandi.edu.co"}
]

# Pre-calcular los horarios base de cada persona segun su grupo al iniciar el modulo
for persona in PERSONAL_DB:
    persona["horarios_base"] = generar_horarios(persona["grupo"])


def obtener_todos_los_grados() -> List[Dict[str, str]]:
    """
    Retorna la lista del personal disponible para agendamiento.
    Incluye el campo 'area' para que el frontend pueda mostrar informacion descriptiva.
    """
    return [
        {
            "grado": p["id"],
            "grupo": p["grupo"],
            "docente": p["docente"],
            "area": p["area"]
        }
        for p in PERSONAL_DB
    ]


def buscar_grado_por_id(grado_id: str) -> Dict[str, Any]:
    """
    Busca un miembro del personal por su identificador unico.
    Retorna None si no existe.
    """
    for p in PERSONAL_DB:
        if p["id"] == grado_id:
            return p
    return None


def leer_citas() -> List[Dict[str, Any]]:
    """
    Lee las citas registradas desde el archivo de texto citas.txt.
    Retorna una lista vacia si el archivo no existe o esta corrupto.
    """
    if not os.path.exists(CITAS_FILE_PATH):
        guardar_citas([])
        return []
    try:
        with open(CITAS_FILE_PATH, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return []
            return json.loads(contenido)
    except (json.JSONDecodeError, IOError):
        return []


def guardar_citas(citas: List[Dict[str, Any]]) -> bool:
    """
    Escribe la lista completa de citas en el archivo citas.txt en formato JSON.
    """
    try:
        with open(CITAS_FILE_PATH, "w", encoding="utf-8") as archivo:
            json.dump(citas, archivo, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False


def obtener_horarios_disponibles(grado_id: str) -> Dict[str, Any]:
    """
    Retorna el nombre, area y horarios disponibles del funcionario especificado,
    filtrando los que ya han sido reservados por otros acudientes.
    """
    persona = buscar_grado_por_id(grado_id)
    if not persona:
        return None

    citas_existentes = leer_citas()

    # Obtener el conjunto de horarios ya reservados para esta persona especifica
    horarios_reservados = {
        cita["horario"]
        for cita in citas_existentes
        if cita["grado"] == grado_id
    }

    horarios_disponibles = [
        h for h in persona["horarios_base"]
        if h not in horarios_reservados
    ]

    return {
        "docente": persona["docente"],
        "area": persona["area"],
        "grupo": persona["grupo"],
        "correo": persona["correo"],
        "horarios": horarios_disponibles
    }
