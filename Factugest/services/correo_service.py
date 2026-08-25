"""
Envío del documento al comprador.

La DIAN exige que el documento electrónico llegue a quien compró, y el comprador
espera los dos archivos: el PDF para leerlo y el XML porque es el documento de
verdad. Aquí se arma ese correo y se manda.

**Se manda después de responder.** La emisión ya terminó cuando esto corre: el
sistema del cliente no tiene por qué esperar a que un servidor de correo ajeno
conteste para saber que su factura salió. Por eso la ruta lo agenda como tarea de
fondo y el resultado —haya llegado o no— queda anotado en `documento_eventos`,
que es donde se mira cuando alguien dice que no le llegó.

**Sin configurar no falla, avisa.** En desarrollo no hay servidor de correo, y una
emisión no debería reventar por eso. Si faltan las variables, el intento se anota
como omitido y ya.
"""
import os
import smtplib
from email.message import EmailMessage

ASUNTOS = {
    "FV": "Factura electrónica {numero} de {emisor}",
    "NC": "Nota crédito {numero} de {emisor}",
    "ND": "Nota débito {numero} de {emisor}",
}

NOMBRES = {"FV": "factura electrónica", "NC": "nota crédito", "ND": "nota débito"}


class CorreoNoConfigurado(Exception):
    """Faltan las variables del servidor de correo."""


class CorreoFallido(Exception):
    """El servidor de correo rechazó el envío o no contestó."""


def configurado() -> bool:
    return bool(os.getenv("SMTP_HOST") and os.getenv("SMTP_DESDE"))


def _configuracion() -> dict:
    if not configurado():
        raise CorreoNoConfigurado(
            "Falta configurar el correo saliente (SMTP_HOST y SMTP_DESDE).")
    return {
        "host": os.getenv("SMTP_HOST"),
        "puerto": int(os.getenv("SMTP_PORT", "587")),
        "usuario": os.getenv("SMTP_USUARIO") or "",
        "clave": os.getenv("SMTP_CLAVE") or "",
        "desde": os.getenv("SMTP_DESDE"),
        "tls": (os.getenv("SMTP_TLS", "si").lower() not in ("no", "0", "false")),
    }


def _cuerpo(documento: dict, emisor: dict) -> str:
    tipo = NOMBRES.get(documento.get("tipo"), "documento electrónico")
    return (
        f"Buen día,\n\n"
        f"Adjuntamos su {tipo} {documento.get('numero')}, emitida por "
        f"{emisor.get('nombre')} (NIT {emisor.get('nit')}).\n\n"
        f"Total: ${float(documento.get('total') or 0):,.2f}\n"
        f"CUFE: {documento.get('cufe') or '—'}\n"
        + (f"\nPuede verificarla en:\n{documento['qr']}\n" if documento.get("qr") else "")
        + "\nSe adjuntan la representación gráfica en PDF y el archivo XML, que es "
        "el documento con validez legal.\n\n"
        "Este mensaje se generó automáticamente; no responda a esta dirección.\n"
    )


def enviar_documento(documento: dict, emisor: dict, destinatario: str,
                     pdf: bytes, xml: str = None) -> str:
    """Manda el documento y devuelve a quién se le mandó.

    Lanza `CorreoNoConfigurado` o `CorreoFallido`; quien llama decide qué anotar.
    """
    if not destinatario:
        raise CorreoFallido("El comprador no tiene correo registrado.")

    cfg = _configuracion()
    numero = documento.get("numero") or "documento"

    mensaje = EmailMessage()
    mensaje["Subject"] = ASUNTOS.get(documento.get("tipo"), "Documento electrónico {numero}") \
        .format(numero=numero, emisor=emisor.get("nombre", ""))
    mensaje["From"] = cfg["desde"]
    mensaje["To"] = destinatario
    mensaje.set_content(_cuerpo(documento, emisor))

    if pdf:
        mensaje.add_attachment(pdf, maintype="application", subtype="pdf",
                               filename=f"{numero}.pdf")
    if xml:
        mensaje.add_attachment(xml.encode("utf-8"), maintype="application",
                               subtype="xml", filename=f"{numero}.xml")

    try:
        with smtplib.SMTP(cfg["host"], cfg["puerto"], timeout=20) as servidor:
            if cfg["tls"]:
                servidor.starttls()
            if cfg["usuario"]:
                servidor.login(cfg["usuario"], cfg["clave"])
            servidor.send_message(mensaje)
    except (smtplib.SMTPException, OSError) as e:
        raise CorreoFallido(f"El servidor de correo no aceptó el envío: {e}")

    return destinatario
