"""
Documentos transmitidos: lo que hemos emitido por cuenta de nuestros clientes.

Es la pantalla que se abre cuando un integrado llama diciendo «mi factura 1043 no
llegó». Desde aquí se ve qué se recibió, con qué número salió, qué contestó el
proveedor y en qué momento — sin pedirle a nadie que mire la base de datos.

Estos documentos **no** son nuestras ventas: viven en `documentos`, no en
`facturas`, y por eso no aparecen en el tablero ni en los reportes. Lo nuestro es
la mensualidad del plan, no lo que vende cada cliente.
"""
from fastapi import APIRouter, Request, Response
from fastapi.responses import RedirectResponse

from services.api_key_service import get_all_clientes_api, get_cliente_api_by_id
from services.branches import get_branch_by_id
from services.documento_canonico import emisor_desde_empresa
from services.documento_service import (a_documento_canonico, buscar_documentos,
                                        contar_documentos, get_documento, get_eventos,
                                        get_lineas, get_receptor, totales_por_estado)
from services.pdf_service import generate_invoice_pdf
from templates_config import templates

router = APIRouter(prefix="/documentos")

POR_PAGINA = 40
TIPOS = ("FV", "NC", "ND")
ESTADOS = ("ACEPTADO", "PENDIENTE", "RECHAZADO", "ERROR")


@router.get("", name="documentos")
def documentos(request: Request, cliente: str = "", tipo: str = "", estado: str = "",
               desde: str = "", hasta: str = "", q: str = "", pagina: int = 1):
    filtros = {"cod_cliente_api": cliente if cliente.isdigit() else None,
               "tipo": tipo if tipo in TIPOS else None,
               "estado": estado if estado in ESTADOS else None,
               "desde": desde or None, "hasta": hasta or None, "q": q.strip() or None}

    pagina = max(1, pagina)
    total = contar_documentos(filtros)
    paginas = max(1, -(-total // POR_PAGINA))
    pagina = min(pagina, paginas)

    return templates.TemplateResponse(request, "documentos/index.html", {
        "documentos": buscar_documentos(filtros, limite=POR_PAGINA,
                                        desplazamiento=(pagina - 1) * POR_PAGINA),
        "por_estado": totales_por_estado(filtros),
        "total": total,
        "pagina": pagina,
        "paginas": paginas,
        "clientes": get_all_clientes_api(),
        "tipos": TIPOS,
        "estados": ESTADOS,
        "filtros": {"cliente": cliente, "tipo": tipo, "estado": estado,
                    "desde": desde, "hasta": hasta, "q": q},
    })


@router.get("/{id_publico}", name="ver_documento")
def ver_documento(request: Request, id_publico: str):
    documento = get_documento(id_publico)
    if not documento:
        return RedirectResponse(url="/documentos", status_code=302)

    return templates.TemplateResponse(request, "documentos/detalle.html", {
        "documento": documento,
        "lineas": get_lineas(documento["cod_documento"]),
        "eventos": get_eventos(documento["cod_documento"]),
        "receptor": get_receptor(documento["cod_receptor"]),
        "emisor": get_branch_by_id(documento["cod_empresa"]) or {},
        "cliente": get_cliente_api_by_id(documento["cod_cliente_api"]),
    })


@router.get("/{id_publico}/pdf", name="documento_pdf")
def documento_pdf(id_publico: str):
    """La misma representación gráfica que descarga el cliente por la API.

    Se regenera de los datos guardados en vez de almacenarse: lo que hay deber de
    conservar es el XML, que es lo que se firma; el PDF es una vista de eso.
    """
    documento = get_documento(id_publico)
    if not documento:
        return RedirectResponse(url="/documentos", status_code=302)

    empresa = get_branch_by_id(documento["cod_empresa"]) or {}
    cabecera, lineas, emisor = a_documento_canonico(
        documento, get_lineas(documento["cod_documento"]),
        get_receptor(documento["cod_receptor"]), emisor_desde_empresa(empresa))
    return Response(
        content=generate_invoice_pdf(cabecera, lineas, emisor=empresa),
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{documento["numero"]}.pdf"'})


@router.get("/{id_publico}/xml", name="documento_xml")
def documento_xml(id_publico: str):
    documento = get_documento(id_publico)
    if not documento or not documento.get("xml"):
        return RedirectResponse(url=f"/documentos/{id_publico}", status_code=302)
    return Response(
        content=documento["xml"].encode("utf-8"),
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{documento["numero"]}.xml"'})
