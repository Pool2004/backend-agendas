import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Credenciales del servidor SMTP configuradas mediante variables de entorno.
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.office365.com")  # default a Office 365
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

def enviar_correo_confirmacion(
    destinatario: str,
    acudiente: str,
    estudiante: str,
    grado: str,
    grupo: str,
    docente: str,
    horario: str,
    telefono: str,
    servidor=None
) -> bool:
    """
    Envia un correo electronico de confirmacion al acudiente con los detalles
    del agendamiento de matricula academica registrado en el sistema.

    Retorna True si el envio fue exitoso, False en caso contrario.
    """
    # Si no hay credenciales configuradas, omitir el envio silenciosamente
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print(
            "[Correo] Las variables EMAIL_SENDER y EMAIL_PASSWORD no estan configuradas. "
            "El correo de confirmacion no fue enviado."
        )
        return False

    # Separar el dia y la hora del horario para mostrarlo de forma mas clara
    partes_horario = horario.split(" ")
    dia_cita = partes_horario[0] if len(partes_horario) > 0 else horario
    hora_cita = partes_horario[1] if len(partes_horario) > 1 else ""

    # Construccion del cuerpo HTML del correo con todos los detalles del agendamiento
    cuerpo_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f7f6;
                margin: 0;
                padding: 0;
            }}
            .container {{
                max-width: 580px;
                margin: 32px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 16px rgba(0,0,0,0.08);
            }}
            .header {{
                background-color: #264fa0;
                padding: 28px 32px;
                text-align: center;
            }}
            .header h1 {{
                color: #ffffff;
                margin: 0;
                font-size: 20px;
                font-weight: 700;
            }}
            .header p {{
                color: #b3c9f0;
                margin: 6px 0 0;
                font-size: 13px;
            }}
            .body {{
                padding: 28px 32px;
            }}
            .greeting {{
                font-size: 15px;
                color: #334155;
                margin-bottom: 16px;
                line-height: 1.6;
            }}
            .detail-box {{
                background-color: #f0f5ff;
                border-left: 4px solid #264fa0;
                border-radius: 8px;
                padding: 20px 24px;
                margin: 20px 0;
            }}
            .detail-box h2 {{
                color: #264fa0;
                font-size: 14px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                margin: 0 0 14px;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                font-size: 14px;
                padding: 6px 0;
                border-bottom: 1px solid #dbeafe;
            }}
            .detail-row:last-child {{
                border-bottom: none;
            }}
            .detail-label {{
                color: #64748b;
                font-weight: 600;
            }}
            .detail-value {{
                color: #1e293b;
                font-weight: 500;
                text-align: right;
            }}
            .notice {{
                background-color: #fffbeb;
                border: 1px solid #fde68a;
                border-radius: 8px;
                padding: 14px 18px;
                font-size: 13px;
                color: #92400e;
                line-height: 1.6;
                margin-top: 20px;
            }}
            .footer {{
                background-color: #264fa0;
                padding: 16px 32px;
                text-align: center;
                font-size: 12px;
                color: #b3c9f0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Confirmacion de Agendamiento de Matricula</h1>
                <p>Sistema de Agendamiento Academico - Comfandi Sede Yumbo</p>
            </div>
            <div class="body">
                <p class="greeting">
                    Estimado/a <strong>{acudiente}</strong>,<br><br>
                    Le confirmamos que su agendamiento de cita para el proceso de
                    <strong>Matricula Academica 2026</strong> ha sido registrado correctamente
                    en nuestro sistema. A continuacion encontrara los detalles de su cita:
                </p>

                <div class="detail-box">
                    <h2>Detalles del Agendamiento</h2>
                    <div class="detail-row">
                        <span class="detail-label">Estudiante:</span>
                        <span class="detail-value">{estudiante}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Grado a matricular:</span>
                        <span class="detail-value">Grado {grado} (Grupo {grupo})</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Docente encargado:</span>
                        <span class="detail-value">{docente}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Dia de la cita:</span>
                        <span class="detail-value">{dia_cita}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Hora de atencion:</span>
                        <span class="detail-value">{hora_cita}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Telefono de contacto:</span>
                        <span class="detail-value">{telefono}</span>
                    </div>
                </div>

                <div class="notice">
                    <strong>Recuerde:</strong> Asista puntualmente a su cita con la documentacion
                    completa requerida para el proceso de matricula. En caso de no poder asistir,
                    comuniquese con la institucion con la mayor anticipacion posible.
                </div>
            </div>
            <div class="footer">
                Comfandi E &mdash; Sede Yumbo &mdash; 2026<br>
                Este es un mensaje automatico, por favor no responda a este correo.
            </div>
        </div>
    </body>
    </html>
    """

    # Construccion del mensaje MIME con soporte HTML y texto plano como alternativa
    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = f"Confirmacion de Matricula - {estudiante} | Comfandi Yumbo 2026"
    mensaje["From"] = f"Comfandi Yumbo <{EMAIL_SENDER}>"
    mensaje["To"] = destinatario

    # Parte de texto plano como respaldo para clientes que no soporten HTML
    texto_plano = (
        f"Confirmacion de Agendamiento de Matricula - Comfandi Yumbo 2026\n\n"
        f"Acudiente: {acudiente}\n"
        f"Estudiante: {estudiante}\n"
        f"Grado: {grado} (Grupo {grupo})\n"
        f"Docente: {docente}\n"
        f"Horario: {horario}\n"
        f"Telefono: {telefono}\n\n"
        f"Por favor asista puntualmente con la documentacion requerida."
    )

    mensaje.attach(MIMEText(texto_plano, "plain", "utf-8"))
    mensaje.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    try:
        if servidor:
            servidor.sendmail(EMAIL_SENDER, destinatario, mensaje.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(EMAIL_SENDER, EMAIL_PASSWORD)
                s.sendmail(EMAIL_SENDER, destinatario, mensaje.as_string())
        print(f"[Correo] Confirmacion enviada exitosamente a: {destinatario}")
        return True
    except smtplib.SMTPAuthenticationError:
        print("[Correo] Error de autenticacion SMTP. Verifique EMAIL_SENDER y EMAIL_PASSWORD.")
        return False
    except smtplib.SMTPException as e:
        print(f"[Correo] Error SMTP al enviar el correo: {e}")
        return False
    except Exception as e:
        print(f"[Correo] Error inesperado al enviar correo: {e}")
        return False


def enviar_correo_docente(
    correo_docente: str,
    docente: str,
    acudiente: str,
    estudiante: str,
    grado: str,
    grupo: str,
    horario: str,
    telefono: str,
    servidor=None
) -> bool:
    """
    Envia un correo electronico de notificacion al docente con los detalles
    del nuevo agendamiento de matricula academica.
    """
    if not EMAIL_SENDER or not EMAIL_PASSWORD or not correo_docente:
        return False

    partes_horario = horario.split(" ")
    dia_cita = partes_horario[0] if len(partes_horario) > 0 else horario
    hora_cita = partes_horario[1] if len(partes_horario) > 1 else ""

    cuerpo_html = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; }}
            .container {{ max-width: 580px; margin: 32px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
            .header {{ background-color: #0f766e; padding: 28px 32px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 20px; font-weight: 700; }}
            .header p {{ color: #ccfbf1; margin: 6px 0 0; font-size: 13px; }}
            .body {{ padding: 28px 32px; }}
            .greeting {{ font-size: 15px; color: #334155; margin-bottom: 16px; line-height: 1.6; }}
            .detail-box {{ background-color: #f0fdfa; border-left: 4px solid #0f766e; border-radius: 8px; padding: 20px 24px; margin: 20px 0; }}
            .detail-box h2 {{ color: #0f766e; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px; }}
            .detail-row {{ display: flex; justify-content: space-between; font-size: 14px; padding: 6px 0; border-bottom: 1px solid #ccfbf1; }}
            .detail-row:last-child {{ border-bottom: none; }}
            .detail-label {{ color: #64748b; font-weight: 600; }}
            .detail-value {{ color: #1e293b; font-weight: 500; text-align: right; }}
            .footer {{ background-color: #0f766e; padding: 16px 32px; text-align: center; font-size: 12px; color: #ccfbf1; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Nuevo Agendamiento Recibido</h1>
                <p>Sistema de Agendamiento Academico - Comfandi Sede Yumbo</p>
            </div>
            <div class="body">
                <p class="greeting">
                    Hola <strong>{docente}</strong>,<br><br>
                    Se ha registrado un nuevo agendamiento para el proceso de
                    <strong>Matricula Academica 2026</strong>. A continuacion, los detalles del estudiante y acudiente asignado a tu cargo:
                </p>

                <div class="detail-box">
                    <h2>Detalles de la Cita</h2>
                    <div class="detail-row">
                        <span class="detail-label">Dia:</span>
                        <span class="detail-value">{dia_cita}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Hora:</span>
                        <span class="detail-value">{hora_cita}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Estudiante:</span>
                        <span class="detail-value">{estudiante}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Grado a matricular:</span>
                        <span class="detail-value">Grado {grado} (Grupo {grupo})</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Acudiente:</span>
                        <span class="detail-value">{acudiente}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Telefono de contacto:</span>
                        <span class="detail-value">{telefono}</span>
                    </div>
                </div>
            </div>
            <div class="footer">
                Comfandi E &mdash; Comfandi E Yumbo &mdash; 2026<br>
                Este es un mensaje automatico.
            </div>
        </div>
    </body>
    </html>
    """

    mensaje = MIMEMultipart("alternative")
    mensaje["Subject"] = f"Nuevo Agendamiento: {estudiante} | {dia_cita} {hora_cita}"
    mensaje["From"] = f"Sistema de Agendamientos <{EMAIL_SENDER}>"
    mensaje["To"] = correo_docente

    texto_plano = (
        f"Nuevo Agendamiento de Matricula - Comfandi Yumbo\n\n"
        f"Dia: {dia_cita}\n"
        f"Hora: {hora_cita}\n"
        f"Estudiante: {estudiante}\n"
        f"Grado: {grado} (Grupo {grupo})\n"
        f"Acudiente: {acudiente}\n"
        f"Telefono: {telefono}\n"
    )

    mensaje.attach(MIMEText(texto_plano, "plain", "utf-8"))
    mensaje.attach(MIMEText(cuerpo_html, "html", "utf-8"))

    try:
        if servidor:
            servidor.sendmail(EMAIL_SENDER, correo_docente, mensaje.as_string())
        else:
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(EMAIL_SENDER, EMAIL_PASSWORD)
                s.sendmail(EMAIL_SENDER, correo_docente, mensaje.as_string())
        print(f"[Correo] Notificacion enviada exitosamente al docente: {correo_docente}")
        return True
    except Exception as e:
        print(f"[Correo] Error al enviar notificacion al docente {correo_docente}: {e}")
        return False


def enviar_correo_cancelacion(
    destinatario_padre: str,
    correo_docente: str,
    acudiente: str,
    estudiante: str,
    grado: str,
    grupo: str,
    docente: str,
    horario: str,
    telefono: str
) -> bool:
    """
    Envía correos electrónicos de cancelación al acudiente y al docente.
    """
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return False

    # Correo para el acudiente
    msg_padre = MIMEMultipart("alternative")
    msg_padre["Subject"] = f"Cancelacion de Cita - {estudiante} | Comfandi Yumbo 2026"
    msg_padre["From"] = f"Comfandi Yumbo <{EMAIL_SENDER}>"
    msg_padre["To"] = destinatario_padre

    cuerpo_padre = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; }}
            .container {{ max-width: 580px; margin: 32px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
            .header {{ background-color: #be123c; padding: 28px 32px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 20px; font-weight: 700; }}
            .header p {{ color: #ffe4e6; margin: 6px 0 0; font-size: 13px; }}
            .body {{ padding: 28px 32px; }}
            .greeting {{ font-size: 15px; color: #334155; margin-bottom: 16px; line-height: 1.6; }}
            .detail-box {{ background-color: #fff1f2; border-left: 4px solid #be123c; border-radius: 8px; padding: 20px 24px; margin: 20px 0; }}
            .detail-box h2 {{ color: #be123c; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px; }}
            .detail-row {{ display: flex; justify-content: space-between; font-size: 14px; padding: 6px 0; border-bottom: 1px solid #ffe4e6; }}
            .detail-row:last-child {{ border-bottom: none; }}
            .detail-label {{ color: #64748b; font-weight: 600; }}
            .detail-value {{ color: #1e293b; font-weight: 500; text-align: right; }}
            .footer {{ background-color: #be123c; padding: 16px 32px; text-align: center; font-size: 12px; color: #ffe4e6; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Cancelacion de Agendamiento de Matricula</h1>
                <p>Sistema de Agendamiento Academico - Comfandi E Yumbo</p>
            </div>
            <div class="body">
                <p class="greeting">
                    Estimado/a <strong>{acudiente}</strong>,<br><br>
                    Le informamos que el agendamiento de cita para el proceso de
                    <strong>Matricula Academica 2026 - 2027</strong> ha sido <strong>cancelado</strong>.
                    El horario previamente seleccionado ha quedado libre. A continuacion, los detalles del agendamiento cancelado:
                </p>

                <div class="detail-box">
                    <h2>Detalles de la Cita Cancelada</h2>
                    <div class="detail-row">
                        <span class="detail-label">Estudiante:</span>
                        <span class="detail-value">{estudiante}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Grado / Grupo:</span>
                        <span class="detail-value">Grado {grado} (Grupo {grupo})</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Docente encargado:</span>
                        <span class="detail-value">{docente}</span>
                    </div>
                    <div class="detail-row">
                        <span class="detail-label">Horario:</span>
                        <span class="detail-value">{horario}</span>
                    </div>
                </div>
            </div>
            <div class="footer">
                Comfandi E &mdash; Sede Yumbo &mdash; 2026<br>
                Este es un mensaje automatico.
            </div>
        </div>
    </body>
    </html>
    """
    msg_padre.attach(MIMEText(cuerpo_padre, "html", "utf-8"))

    # Correo para el docente
    msg_docente = None
    if correo_docente:
        msg_docente = MIMEMultipart("alternative")
        msg_docente["Subject"] = f"Cancelacion de Cita: {estudiante} | {horario}"
        msg_docente["From"] = f"Sistema de Agendamientos <{EMAIL_SENDER}>"
        msg_docente["To"] = correo_docente

        cuerpo_docente = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; }}
                .container {{ max-width: 580px; margin: 32px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
                .header {{ background-color: #be123c; padding: 28px 32px; text-align: center; }}
                .header h1 {{ color: #ffffff; margin: 0; font-size: 20px; font-weight: 700; }}
                .header p {{ color: #ffe4e6; margin: 6px 0 0; font-size: 13px; }}
                .body {{ padding: 28px 32px; }}
                .greeting {{ font-size: 15px; color: #334155; margin-bottom: 16px; line-height: 1.6; }}
                .detail-box {{ background-color: #fff1f2; border-left: 4px solid #be123c; border-radius: 8px; padding: 20px 24px; margin: 20px 0; }}
                .detail-box h2 {{ color: #be123c; font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 14px; }}
                .detail-row {{ display: flex; justify-content: space-between; font-size: 14px; padding: 6px 0; border-bottom: 1px solid #ffe4e6; }}
                .detail-row:last-child {{ border-bottom: none; }}
                .detail-label {{ color: #64748b; font-weight: 600; }}
                .detail-value {{ color: #1e293b; font-weight: 500; text-align: right; }}
                .footer {{ background-color: #be123c; padding: 16px 32px; text-align: center; font-size: 12px; color: #ffe4e6; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Cita Cancelada</h1>
                    <p>Sistema de Agendamiento Academico - Comfandi E Yumbo</p>
                </div>
                <div class="body">
                    <p class="greeting">
                        Hola <strong>{docente}</strong>,<br><br>
                        Se ha cancelado la cita programada con el acudiente del estudiante <strong>{estudiante}</strong>.
                        El horario ha quedado liberado.
                    </p>

                    <div class="detail-box">
                        <h2>Detalles de la Cita Cancelada</h2>
                        <div class="detail-row">
                            <span class="detail-label">Estudiante:</span>
                            <span class="detail-value">{estudiante}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Acudiente:</span>
                            <span class="detail-value">{acudiente}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Horario:</span>
                            <span class="detail-value">{horario}</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Telefono:</span>
                            <span class="detail-value">{telefono}</span>
                        </div>
                    </div>
                </div>
                <div class="footer">
                    Comfandi E &mdash; Yumbo &mdash; 2026<br>
                    Este es un mensaje automatico.
                </div>
            </div>
        </body>
        </html>
        """
        msg_docente.attach(MIMEText(cuerpo_docente, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            # Enviar a padre
            servidor.sendmail(EMAIL_SENDER, destinatario_padre, msg_padre.as_string())
            print(f"[Correo] Notificacion de cancelacion enviada a acudiente: {destinatario_padre}")
            
            # Enviar a docente
            if msg_docente and correo_docente:
                servidor.sendmail(EMAIL_SENDER, correo_docente, msg_docente.as_string())
                print(f"[Correo] Notificacion de cancelacion enviada a docente: {correo_docente}")
        return True
    except Exception as e:
        print(f"[Correo] Error al enviar correos de cancelacion: {e}")
        return False


def enviar_correo_reprogramacion(
    destinatario_padre: str,
    correo_docente_antiguo: str,
    correo_docente_nuevo: str,
    acudiente: str,
    estudiante: str,
    telefono: str,
    docente_antiguo: str,
    docente_nuevo: str,
    grado_antiguo: str,
    grado_nuevo: str,
    grupo_antiguo: str,
    grupo_nuevo: str,
    horario_antiguo: str,
    horario_nuevo: str
) -> bool:
    """
    Envía correos electrónicos de reprogramación al acudiente y a los docentes correspondientes.
    """
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        return False

    # Correo para el acudiente
    msg_padre = MIMEMultipart("alternative")
    msg_padre["Subject"] = f"Reprogramacion de Cita - {estudiante} | Comfandi Yumbo 2026"
    msg_padre["From"] = f"Comfandi Yumbo <{EMAIL_SENDER}>"
    msg_padre["To"] = destinatario_padre

    cuerpo_padre = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f4f7f6; margin: 0; padding: 0; }}
            .container {{ max-width: 580px; margin: 32px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
            .header {{ background-color: #d97706; padding: 28px 32px; text-align: center; }}
            .header h1 {{ color: #ffffff; margin: 0; font-size: 20px; font-weight: 700; }}
            .header p {{ color: #fef3c7; margin: 6px 0 0; font-size: 13px; }}
            .body {{ padding: 28px 32px; }}
            .greeting {{ font-size: 15px; color: #334155; margin-bottom: 16px; line-height: 1.6; }}
            .compare-box {{ display: flex; flex-direction: column; gap: 16px; margin: 20px 0; }}
            .detail-box {{ border-radius: 8px; padding: 18px 22px; }}
            .box-old {{ background-color: #fcf8f2; border-left: 4px solid #d97706; }}
            .box-new {{ background-color: #f0fdf4; border-left: 4px solid #16a34a; }}
            .detail-box h2 {{ font-size: 14px; text-transform: uppercase; letter-spacing: 0.5px; margin: 0 0 10px; }}
            .box-old h2 {{ color: #d97706; }}
            .box-new h2 {{ color: #16a34a; }}
            .detail-row {{ display: flex; justify-content: space-between; font-size: 13px; padding: 5px 0; border-bottom: 1px dashed #e2e8f0; }}
            .detail-row:last-child {{ border-bottom: none; }}
            .detail-label {{ color: #64748b; font-weight: 600; }}
            .detail-value {{ color: #1e293b; font-weight: 500; text-align: right; }}
            .footer {{ background-color: #d97706; padding: 16px 32px; text-align: center; font-size: 12px; color: #fef3c7; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Reprogramacion de Agendamiento de Matricula</h1>
                <p>Sistema de Agendamiento Academico - Comfandi E Yumbo</p>
            </div>
            <div class="body">
                <p class="greeting">
                    Estimado/a <strong>{acudiente}</strong>,<br><br>
                    Le confirmamos que su agendamiento de cita para el proceso de
                    <strong>Matricula Academica 2026 - 2027</strong> del estudiante <strong>{estudiante}</strong>
                    ha sido <strong>reprogramado</strong> exitosamente.
                </p>

                <div class="compare-box">
                    <div class="detail-box box-old">
                        <h2>Información Anterior</h2>
                        <div class="detail-row">
                            <span class="detail-label">Docente:</span>
                            <span class="detail-value">{docente_antiguo} (Grado {grado_antiguo})</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Horario:</span>
                            <span class="detail-value">{horario_antiguo}</span>
                        </div>
                    </div>

                    <div class="detail-box box-new">
                        <h2>Nueva Información Asignada</h2>
                        <div class="detail-row">
                            <span class="detail-label">Docente:</span>
                            <span class="detail-value">{docente_nuevo} (Grado {grado_nuevo})</span>
                        </div>
                        <div class="detail-row">
                            <span class="detail-label">Horario:</span>
                            <span class="detail-value">{horario_nuevo}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="footer">
                Comfandi E &mdash; Comfandi E Yumbo &mdash; 2026<br>
                Este es un mensaje automatico.
            </div>
        </div>
    </body>
    </html>
    """
    msg_padre.attach(MIMEText(cuerpo_padre, "html", "utf-8"))

    # Correos para docentes
    emails_to_send = []

    # Si es el mismo docente y el mismo correo, enviamos un solo correo informando el cambio de horario
    if correo_docente_antiguo == correo_docente_nuevo and correo_docente_antiguo:
        msg_doc = MIMEMultipart("alternative")
        msg_doc["Subject"] = f"Reprogramacion de Cita: {estudiante} | {horario_nuevo}"
        msg_doc["From"] = f"Sistema de Agendamientos <{EMAIL_SENDER}>"
        msg_doc["To"] = correo_docente_antiguo
        cuerpo_doc = f"""
        <html>
        <body>
            <h3>Cita Reprogramada</h3>
            <p>Hola <strong>{docente_antiguo}</strong>,</p>
            <p>Le informamos que la cita del estudiante <strong>{estudiante}</strong> con acudiente <strong>{acudiente}</strong> ha sido reprogramada.</p>
            <p><strong>Horario anterior:</strong> {horario_antiguo}</p>
            <p><strong>Nuevo horario:</strong> {horario_nuevo}</p>
        </body>
        </html>
        """
        msg_doc.attach(MIMEText(cuerpo_doc, "html", "utf-8"))
        emails_to_send.append((correo_docente_antiguo, msg_doc))
    else:
        # Docentes diferentes. Notificar a docente antiguo que se canceló/movió, y a docente nuevo que se agendó.
        if correo_docente_antiguo:
            msg_doc_ant = MIMEMultipart("alternative")
            msg_doc_ant["Subject"] = f"Cancelacion de Cita (Movida): {estudiante} | {horario_antiguo}"
            msg_doc_ant["From"] = f"Sistema de Agendamientos <{EMAIL_SENDER}>"
            msg_doc_ant["To"] = correo_docente_antiguo
            cuerpo_doc_ant = f"""
            <html>
            <body>
                <h3>Cita Cancelada / Reasignada</h3>
                <p>Hola <strong>{docente_antiguo}</strong>,</p>
                <p>La cita programada con el estudiante <strong>{estudiante}</strong> y acudiente <strong>{acudiente}</strong> para el horario <strong>{horario_antiguo}</strong> ha sido cancelada o reasignada a otro docente. Este horario ha quedado libre.</p>
            </body>
            </html>
            """
            msg_doc_ant.attach(MIMEText(cuerpo_doc_ant, "html", "utf-8"))
            emails_to_send.append((correo_docente_antiguo, msg_doc_ant))
        
        if correo_docente_nuevo:
            msg_doc_nue = MIMEMultipart("alternative")
            msg_doc_nue["Subject"] = f"Nueva Cita Agendada (Reprogramacion): {estudiante} | {horario_nuevo}"
            msg_doc_nue["From"] = f"Sistema de Agendamientos <{EMAIL_SENDER}>"
            msg_doc_nue["To"] = correo_docente_nuevo
            cuerpo_doc_nue = f"""
            <html>
            <body>
                <h3>Nueva Cita Asignada</h3>
                <p>Hola <strong>{docente_nuevo}</strong>,</p>
                <p>Se le ha asignado una nueva cita debido a la reprogramacion del estudiante <strong>{estudiante}</strong> con acudiente <strong>{acudiente}</strong> (Telefono: {telefono}).</p>
                <p><strong>Horario:</strong> {horario_nuevo}</p>
                <p><strong>Grado:</strong> {grado_nuevo} (Grupo {grupo_nuevo})</p>
            </body>
            </html>
            """
            msg_doc_nue.attach(MIMEText(cuerpo_doc_nue, "html", "utf-8"))
            emails_to_send.append((correo_docente_nuevo, msg_doc_nue))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            # Enviar a padre
            servidor.sendmail(EMAIL_SENDER, destinatario_padre, msg_padre.as_string())
            print(f"[Correo] Notificacion de reprogramacion enviada a acudiente: {destinatario_padre}")
            
            # Enviar a docentes
            for dest_email, msg_obj in emails_to_send:
                servidor.sendmail(EMAIL_SENDER, dest_email, msg_obj.as_string())
                print(f"[Correo] Notificacion de reprogramacion enviada a docente: {dest_email}")
        return True
    except Exception as e:
        print(f"[Correo] Error al enviar correos de reprogramacion: {e}")
        return False


def enviar_correos_nuevo_agendamiento(
    correo_padre: str,
    correo_docente: str,
    acudiente: str,
    estudiante: str,
    grado: str,
    grupo: str,
    docente: str,
    horario: str,
    telefono: str
) -> bool:
    """
    Envía la confirmación al acudiente y la notificación al docente en una única sesión SMTP
    para evitar colisiones de conexión/login con Office 365.
    """
    if not EMAIL_SENDER or not EMAIL_PASSWORD:
        print("[Correo] Falta configuración de EMAIL_SENDER o EMAIL_PASSWORD.")
        return False

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(EMAIL_SENDER, EMAIL_PASSWORD)
            
            # Enviar al acudiente
            enviar_correo_confirmacion(
                destinatario=correo_padre,
                acudiente=acudiente,
                estudiante=estudiante,
                grado=grado,
                grupo=grupo,
                docente=docente,
                horario=horario,
                telefono=telefono,
                servidor=s
            )
            
            # Enviar al docente si tiene correo
            if correo_docente:
                enviar_correo_docente(
                    correo_docente=correo_docente,
                    docente=docente,
                    acudiente=acudiente,
                    estudiante=estudiante,
                    grado=grado,
                    grupo=grupo,
                    horario=horario,
                    telefono=telefono,
                    servidor=s
                )
        return True
    except Exception as e:
        print(f"[Correo] Error en la sesión SMTP combinada: {e}")
        return False

