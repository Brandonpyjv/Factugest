"""
Emisión de facturas por la API de integración.

Aquí se juntan todas las piezas anteriores: el cálculo tributario de la fase 1,
la reserva atómica del consecutivo, el CUFE, el XML, el adaptador de proveedor y
el almacén de documentos. Este archivo no debería tener lógica propia — si algo
se calcula aquí, es que le falta su sitio.
"""
from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Query, Request, Response, status

from services.api_key_service import get_cliente_api_by_id
from services.branches import get_branch_by_id
from services.calculo_documento import calcular_documento
from services.consumo_service import cupo_disponible
from services.cufe_service import generate_cufe
from services.dian_proveedor import ErrorProveedorDian
from services.documento_canonico import emisor_desde_empresa
from services.documento_service import (a_documento_canonico, buscar_documentos,
                                        contar_documentos, get_documento,
                                        get_documento_por_referencia, get_lineas,
                                        get_receptor, registrar_transmision,
                                        reservar_y_guardar)
from services.numeracion_service import RangoResolucionAgotadoError
from services.pdf_service import generate_invoice_pdf
from services.xml_service import generate_invoice_xml
from routes.api.v1.dependencias import ClienteAPI
from routes.api.v1.comun import (con_ultimo_evento, enviar_por_correo,
                                 lineas_para_guardar, proveedor_o_error,
                                 respuesta_documento)
from routes.api.v1.errores import error as _error
from routes.api.v1.modelos import (DocumentoResumen, FacturaRequest, FacturaResponse,
                                   ListaDocumentos, RespuestaError, ResultadoDian)

router = APIRouter(prefix="/api/v1", tags=["Documentos"])


@router.post("/facturas", response_model=FacturaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Emitir una factura de venta",
             responses={
                 200: {"model": FacturaResponse,
                       "description": "La referencia externa ya se había emitido: "
                                      "se devuelve el mismo documento"},
                 401: {"model": RespuestaError, "description": "Llave ausente o inválida"},
                 403: {"model": RespuestaError,
                       "description": "Cliente suspendido, o cupo del plan agotado"},
                 409: {"model": RespuestaError,
                       "description": "El emisor no puede numerar: rango agotado"},
                 422: {"model": RespuestaError, "description": "Datos inválidos"},
                 502: {"model": RespuestaError,
                       "description": "No se pudo contactar al proveedor DIAN"},
             })
def emitir_factura(datos: FacturaRequest, cliente: ClienteAPI, peticion: Request,
                   respuesta_http: Response,
                   tareas: BackgroundTasks) -> FacturaResponse:
    """Emite una factura electrónica y devuelve el documento validado.

    Reenviar la misma `referencia_externa` **no emite otra factura**: devuelve la
    que ya existe, con código 200 en lugar de 201. Es lo que evita que un
    reintento por corte de red queme un segundo número de la resolución.
    """
    # Idempotencia: se comprueba antes de tocar nada.
    ya_emitido = get_documento_por_referencia(cliente["cod_cliente_api"],
                                              datos.referencia_externa)
    if ya_emitido:
        # 200 y no 201: no se creó nada, se está devolviendo lo que ya existía.
        respuesta_http.status_code = status.HTTP_200_OK
        return con_ultimo_evento(respuesta_documento(ya_emitido, peticion), ya_emitido)

    # El cupo se comprueba antes de numerar. Después de reservar el consecutivo ya
    # se gastó un número de la resolución, y devolverlo no es posible.
    cupo = cupo_disponible(cliente)
    if cupo["agotado"]:
        raise _error(
            status.HTTP_403_FORBIDDEN, "cupo_agotado",
            f"El plan {cliente['plan']} incluye {cupo['cupo']} documentos al mes y "
            f"este mes ya se emitieron {cupo['emitidos']}. Escríbenos para ampliar "
            "el plan.")

    empresa = get_branch_by_id(cliente["cod_empresa"])
    if not empresa:
        raise _error(status.HTTP_409_CONFLICT, "emisor_no_configurado",
                     "El cliente no tiene una empresa emisora configurada.")
    emisor = emisor_desde_empresa(empresa)

    calculo = calcular_documento(
        [{
            "codigo": i.codigo,
            "descripcion": i.descripcion,
            "unidad_medida": i.unidad_medida,
            "cantidad": i.cantidad,
            "precio_unitario": i.precio_unitario,
            "descuento_porcentaje": i.descuento_porcentaje,
            "descuento_descripcion": i.descuento_descripcion,
            "impuesto_porcentaje": i.impuesto.porcentaje,
            "impuesto_codigo_dian": i.impuesto.codigo,
        } for i in datos.items],
        datos.descuento_global.valor if datos.descuento_global else 0,
    )

    receptor = datos.receptor.model_dump()
    proveedor = proveedor_o_error()

    # El CUFE necesita el número, y el XML necesita el CUFE: por eso se pasan
    # como funciones, para que se calculen dentro de la transacción que reserva.
    def cufe_de(cab):
        return generate_cufe({
            "numero_factura": cab["numero"],
            "fecha": cab["fecha_emision"],
            "subtotal": calculo["subtotal"],
            "total_impuestos": calculo["total_impuestos"],
            "total": calculo["total"],
            "document_number": receptor["numero_documento"],
        }, empresa)

    def xml_de(cab, cod_receptor):
        cabecera, lineas, emi = a_documento_canonico(
            {"numero": cab["numero"], "tipo": "FV", "fecha_emision": cab["fecha_emision"],
             "fecha_vencimiento": cab["fecha_vencimiento"], "cufe": cab["cufe"],
             "forma_pago": datos.forma_pago, "observaciones": datos.observaciones,
             "orden_compra": datos.orden_compra,
             "subtotal": calculo["subtotal"], "total_descuentos": calculo["total_descuentos"],
             "total_impuestos": calculo["total_impuestos"], "total": calculo["total"]},
            lineas_para_guardar(calculo), receptor, emisor)
        return generate_invoice_xml(cabecera, lineas, emi)

    try:
        emitido = reservar_y_guardar(
            cliente, "FV", calculo, receptor, cufe_de, xml_de,
            {"plazo_dias": datos.plazo_dias, "forma_pago": datos.forma_pago,
             "referencia_externa": datos.referencia_externa,
             "observaciones": datos.observaciones, "orden_compra": datos.orden_compra,
             "proveedor_dian": proveedor.nombre})
    except RangoResolucionAgotadoError as e:
        raise _error(status.HTTP_409_CONFLICT, "rango_agotado", str(e))

    # Transmisión: fuera de la transacción, para no dejar bloqueada la fila del
    # emisor esperando una respuesta de red.
    documento = get_documento(emitido["id_publico"], cliente["cod_cliente_api"])
    receptor_guardado = get_receptor(emitido["cod_receptor"])
    cabecera, lineas, emi = a_documento_canonico(
        documento, get_lineas(documento["cod_documento"]), receptor_guardado, emisor)

    try:
        respuesta = proveedor.transmitir(cabecera, lineas, emi, emitido["xml"])
    except ErrorProveedorDian as e:
        raise _error(status.HTTP_502_BAD_GATEWAY, "proveedor_no_disponible", str(e))

    registrar_transmision(documento["cod_documento"], respuesta)

    # El correo sale después de responder: el punto de venta no tiene por qué
    # esperar a que un servidor de correo ajeno conteste para saber que ya facturó.
    if datos.enviar_email:
        tareas.add_task(enviar_por_correo, emitido["id_publico"])

    documento = get_documento(emitido["id_publico"], cliente["cod_cliente_api"])
    salida = respuesta_documento(documento, peticion)
    salida.qr = respuesta.qr
    salida.dian = ResultadoDian(proveedor=respuesta.proveedor, codigo=respuesta.codigo,
                                mensaje=respuesta.mensaje)
    return salida


# ── Consulta ────────────────────────────────────────────────────────────────

@router.get("/documentos", response_model=ListaDocumentos,
            summary="Listar los documentos emitidos",
            responses={401: {"model": RespuestaError}, 403: {"model": RespuestaError}})
def listar_documentos(
    cliente: ClienteAPI,
    tipo: Annotated[str | None, Query(description="FV, NC o ND")] = None,
    estado: Annotated[str | None, Query(
        description="ACEPTADO, PENDIENTE, RECHAZADO o ERROR")] = None,
    desde: Annotated[str | None, Query(description="Fecha inicial, AAAA-MM-DD")] = None,
    hasta: Annotated[str | None, Query(description="Fecha final, AAAA-MM-DD")] = None,
    buscar: Annotated[str | None, Query(
        description="Texto libre: número, referencia externa, CUFE o nombre del "
                    "comprador")] = None,
    pagina: Annotated[int, Query(ge=1)] = 1,
    por_pagina: Annotated[int, Query(ge=1, le=200)] = 50,
) -> ListaDocumentos:
    """Los documentos de **este** cliente, del más reciente al más antiguo.

    Es lo que alimenta la conciliación: el sistema del cliente pide los documentos
    de un mes y compara contra sus propias ventas. Por eso cada fila trae la
    `referencia_externa` con la que él los envió.

    La llave decide qué se ve: no hay forma de pedir los documentos de otro
    cliente, ni siquiera conociendo su identificador.
    """
    filtros = {
        "cod_cliente_api": cliente["cod_cliente_api"],
        "tipo": tipo.upper() if tipo else None,
        "estado": estado.upper() if estado else None,
        "desde": desde, "hasta": hasta, "q": (buscar or "").strip() or None,
    }

    total = contar_documentos(filtros)
    paginas = max(1, -(-total // por_pagina))
    filas = buscar_documentos(filtros, limite=por_pagina,
                              desplazamiento=(pagina - 1) * por_pagina)

    return ListaDocumentos(
        total=total, pagina=pagina, por_pagina=por_pagina, paginas=paginas,
        documentos=[DocumentoResumen(
            id=f["id_publico"], numero=f["numero"], tipo=f["tipo"], estado=f["estado"],
            fecha_emision=f["fecha_emision"], total=float(f["total"] or 0),
            cufe=f["cufe"], referencia_externa=f["referencia_externa"],
        ) for f in filas],
    )


# ── Descarga ────────────────────────────────────────────────────────────────

def _documento_del_cliente(id_publico: str, cliente: dict) -> dict:
    documento = get_documento(id_publico, cliente["cod_cliente_api"])
    if not documento:
        raise _error(status.HTTP_404_NOT_FOUND, "documento_no_encontrado",
                     "No existe ese documento.")
    return documento


@router.get("/documentos/{id_publico}", response_model=FacturaResponse,
            summary="Consultar un documento",
            responses={404: {"model": RespuestaError}})
def consultar_documento(id_publico: str, cliente: ClienteAPI,
                        peticion: Request) -> FacturaResponse:
    """Recupera un documento ya emitido. Sirve para reconciliar cuando el sistema
    del cliente perdió la respuesta."""
    documento = _documento_del_cliente(id_publico, cliente)
    return con_ultimo_evento(respuesta_documento(documento, peticion), documento)


@router.get("/documentos/{id_publico}/pdf", summary="Descargar la representación gráfica",
            response_class=Response,
            responses={200: {"content": {"application/pdf": {}}},
                       404: {"model": RespuestaError}})
def descargar_pdf(id_publico: str, cliente: ClienteAPI):
    """El PDF se genera al momento a partir de lo guardado.

    No se almacena porque es reproducible: lo que hay que conservar es el XML,
    que es lo que se firma y valida.
    """
    documento = _documento_del_cliente(id_publico, cliente)
    empresa = get_branch_by_id(documento["cod_empresa"]) or {}
    cabecera, lineas, emisor = a_documento_canonico(
        documento, get_lineas(documento["cod_documento"]),
        get_receptor(documento["cod_receptor"]), emisor_desde_empresa(empresa))
    return Response(
        content=generate_invoice_pdf(cabecera, lineas, emisor=empresa),
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{documento["numero"]}.pdf"'})


@router.get("/documentos/{id_publico}/xml", summary="Descargar el XML UBL",
            response_class=Response,
            responses={200: {"content": {"application/xml": {}}},
                       404: {"model": RespuestaError}})
def descargar_xml(id_publico: str, cliente: ClienteAPI):
    """El XML que se transmitió, tal cual. Es el que hay deber de conservar."""
    documento = _documento_del_cliente(id_publico, cliente)
    if not documento.get("xml"):
        raise _error(status.HTTP_404_NOT_FOUND, "xml_no_disponible",
                     "Ese documento no tiene XML almacenado.")
    return Response(
        content=documento["xml"].encode("utf-8"),
        media_type="application/xml",
        headers={"Content-Disposition": f'attachment; filename="{documento["numero"]}.xml"'})
