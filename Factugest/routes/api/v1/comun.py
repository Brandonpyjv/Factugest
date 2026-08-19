"""
Lo que comparten los tres documentos que emite la API.

Una factura, una nota crédito y una nota débito se diferencian en cómo se calcula
lo que llevan; en todo lo demás —cómo se arma la respuesta, cómo se elige el
proveedor, cómo se transmite y cómo se guarda lo que contestó— son el mismo
procedimiento. Tenerlo tres veces garantizaría que las tres respuestas terminaran
siendo distintas sin que nadie lo decidiera.
"""
from fastapi import Request, status

from routes.api.v1.errores import error
from routes.api.v1.modelos import FacturaResponse, ResultadoDian, Totales
from services.dian_proveedor import ErrorProveedorDian, get_proveedor
from services.documento_service import get_eventos


def respuesta_documento(documento: dict, peticion: Request = None) -> FacturaResponse:
    """La misma forma para los tres tipos de documento."""
    base = str(peticion.base_url).rstrip("/") if peticion else ""
    ruta = f"{base}/api/v1/documentos/{documento['id_publico']}"
    return FacturaResponse(
        id=documento["id_publico"],
        numero=documento["numero"],
        tipo=documento.get("tipo") or "FV",
        cufe=documento.get("cufe"),
        estado=documento["estado"],
        fecha_emision=documento["fecha_emision"],
        fecha_vencimiento=(str(documento["fecha_vencimiento"])
                           if documento.get("fecha_vencimiento") else None),
        totales=Totales(
            bruto=float(documento.get("subtotal_bruto") or 0),
            descuentos=float(documento.get("total_descuentos") or 0),
            base_gravable=float(documento.get("subtotal") or 0),
            impuestos=float(documento.get("total_impuestos") or 0),
            total=float(documento.get("total") or 0),
        ),
        qr=documento.get("qr"),
        pdf_url=f"{ruta}/pdf",
        xml_url=f"{ruta}/xml",
        documento_referencia=documento.get("id_referencia"),
        anulado=bool(documento.get("anulado")),
        dian=ResultadoDian(
            proveedor=documento.get("proveedor_dian") or "",
            codigo=documento.get("codigo_dian") or "",
            mensaje=documento.get("mensaje_dian") or "",
        ),
    )


def con_ultimo_evento(salida: FacturaResponse, documento: dict) -> FacturaResponse:
    """Rellena el bloque `dian` de un documento que ya estaba emitido.

    Lo que contestó el proveedor no se guarda en `documentos` sino en sus eventos,
    porque un documento puede haberse transmitido más de una vez. Al consultarlo
    después, lo que importa es la última respuesta.
    """
    eventos = [e for e in get_eventos(documento["cod_documento"])
               if e["tipo"] in ("ACEPTADO", "RECHAZADO", "ERROR")]
    if eventos:
        ultimo = eventos[-1]
        salida.dian = ResultadoDian(proveedor=ultimo.get("proveedor") or "",
                                    codigo=ultimo.get("codigo") or "",
                                    mensaje=ultimo.get("mensaje") or "")
    return salida


def lineas_para_guardar(calculo: dict) -> list:
    """Las líneas ya calculadas, con los nombres que usa `documento_lineas`."""
    return [{
        "codigo": l.get("codigo"),
        "descripcion": l.get("descripcion"),
        "unidad_medida": l.get("unidad_medida"),
        "cantidad": l["cantidad"],
        "precio_unitario": l["precio_unitario"],
        "valor_bruto": l["valor_bruto"],
        "descuento_porcentaje": l["descuento_porcentaje"],
        "descuento_valor": l["descuento_valor"],
        # La factura llama al campo `descuento_descripcion` y la línea guardada
        # `descripcion_descuento`; una nota se arma a partir de la segunda.
        "descripcion_descuento": (l.get("descuento_descripcion")
                                  or l.get("descripcion_descuento")),
        "subtotal": l["subtotal"],
        "impuesto_codigo_dian": l.get("impuesto_codigo_dian"),
        "impuesto_porcentaje": l["impuesto_porcentaje"],
        "impuesto_valor": l["impuesto_valor"],
    } for l in calculo["lineas"]]


def proveedor_o_error():
    try:
        return get_proveedor()
    except ErrorProveedorDian as e:
        raise error(status.HTTP_502_BAD_GATEWAY, "proveedor_mal_configurado", str(e))


def enviar_por_correo(id_publico: str):
    """Manda el documento al comprador. Corre en segundo plano, después de responder.

    Se traga cualquier excepción a propósito: esto se ejecuta cuando la respuesta
    HTTP ya salió, así que un fallo aquí no puede llegarle al cliente. Lo que sí
    queda es el rastro en `documento_eventos`, que es donde se mira cuando alguien
    dice que no le llegó su factura.
    """
    from services.branches import get_branch_by_id
    from services.correo_service import (CorreoFallido, CorreoNoConfigurado,
                                         enviar_documento)
    from services.documento_canonico import emisor_desde_empresa
    from services.documento_service import (a_documento_canonico, get_documento,
                                            get_lineas, get_receptor,
                                            registrar_evento)
    from services.pdf_service import generate_invoice_pdf

    documento = get_documento(id_publico)
    if not documento:
        return

    cod = documento["cod_documento"]
    try:
        emisor = get_branch_by_id(documento["cod_empresa"]) or {}
        receptor = get_receptor(documento["cod_receptor"]) or {}
        cabecera, lineas, emi = a_documento_canonico(
            documento, get_lineas(cod), receptor, emisor_desde_empresa(emisor))

        destino = enviar_documento(documento, emisor, receptor.get("email"),
                                   generate_invoice_pdf(cabecera, lineas),
                                   documento.get("xml"))
        registrar_evento(cod, "CORREO_ENVIADO",
                         mensaje=f"Enviado a {destino} con el PDF y el XML adjuntos")
    except CorreoNoConfigurado as e:
        registrar_evento(cod, "CORREO_OMITIDO", mensaje=str(e))
    except CorreoFallido as e:
        registrar_evento(cod, "CORREO_FALLIDO", mensaje=str(e))
    except Exception as e:                      # noqa: BLE001 — ver el docstring
        registrar_evento(cod, "CORREO_FALLIDO",
                         mensaje=f"No se pudo armar el correo: {type(e).__name__}: {e}")
