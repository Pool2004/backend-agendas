import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Credenciales del servidor SMTP configuradas mediante variables de entorno.
# Para usar Gmail, habilite "Contrasenas de aplicacion" en la cuenta y asigne:
#   EMAIL_SENDER   : correo remitente (ej: notificaciones@comfandi.edu.co)
#   EMAIL_PASSWORD : contrasena de aplicacion de 16 caracteres generada por Google
# Si las variables no estan definidas, el envio se omite sin bloquear el flujo principal.
EMAIL_SENDER = os.environ.get("EMAIL_SENDER", "")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))

def enviar_correo_confirmacion(
    destinatario: str,
    acudiente: str,
    estudiante: str,
    grado: str,
    grupo: str,
    docente: str,
    horario: str,
    telefono: str
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
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_SENDER, destinatario, mensaje.as_string())
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
    telefono: str
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
                Comfandi E &mdash; Sede Yumbo &mdash; 2026<br>
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
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.login(EMAIL_SENDER, EMAIL_PASSWORD)
            servidor.sendmail(EMAIL_SENDER, correo_docente, mensaje.as_string())
        print(f"[Correo] Notificacion enviada exitosamente al docente: {correo_docente}")
        return True
    except Exception as e:
        print(f"[Correo] Error al enviar notificacion al docente {correo_docente}: {e}")
        return False
