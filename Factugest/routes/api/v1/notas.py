"""
Notas crédito y débito por la API.

Una nota no se emite sola: corrige un documento que ya salió. Eso cambia dos
cosas frente a la factura de venta.

**Las líneas no las envía el cliente.** Una nota crédito devuelve *lo que se
facturó*, con los precios, descuentos e impuestos con los que se facturó. Si el
integrador pudiera mandar líneas nuevas, podría devolver a un precio distinto del
que cobró, y la diferencia sería dinero salido de la nada. Por eso solo se
mandan cantidades y el resto sale del original.

**Numeran en su propia serie.** NC y ND llevan consecutivos aparte del de la
factura, y se reservan con `reservar_numero`, igual de atómico: dos devoluciones
simultáneas del mismo emisor no pueden salir con el mismo número.

**El cupo del plan no bloquea una nota.** Cuenta para el consumo del mes, pero no
se rechaza por cupo agotado: negarle a un cliente la corrección de una factura mal
emitida lo dejaría con un documento equivocado ante la DIAN y sin forma de
arreglarlo hasta el mes siguiente. Cobrar el excedente es un asunto entre él y
nosotros; el documento tiene que poder salir.
"""
from fastapi import APIRouter, BackgroundTasks, Request, Response, status

from database import get_one

from routes.api.v1.comun import (con_ultimo_evento, enviar_por_correo,
                                 lineas_para_guardar, proveedor_o_error,
                                 respuesta_documento)
from routes.api.v1.dependencias import ClienteAPI
from routes.api.v1.errores import error as _error
from routes.api.v1.modelos import (FacturaResponse, NotaCreditoRequest,
                                   NotaDebitoRequest, RespuestaError, ResultadoDian)
from services.branches import get_branch_by_id
from services.calculo_documento import (calcular_nota_credito, calcular_nota_debito,
                                        tasa_promedio)
from services.cufe_service import generate_cufe
from services.dian_proveedor import ErrorProveedorDian
from services.documento_canonico import emisor_desde_empresa
from services.documento_service import (a_documento_canonico, get_documento,
                                        get_documento_por_referencia, get_lineas,
                                        get_receptor, registrar_evento,
                                        registrar_transmision, reservar_y_guardar)
from services.numeracion_service import RangoResolucionAgotadoError
from services.xml_service import generate_invoice_xml

router = APIRouter(prefix="/api/v1", tags=["Documentos"])

RESPUESTAS = {
    200: {"model": FacturaResponse,
          "description": "La referencia externa ya se había emitido: se devuelve "
                         "la misma nota"},
    401: {"model": RespuestaError, "description": "Llave ausente o inválida"},
    403: {"model": RespuestaError, "description": "Cliente suspendido"},
    404: {"model": RespuestaError, "description": "El documento que se corrige no existe"},
    409: {"model": RespuestaError,
          "description": "No se puede emitir la nota sobre ese documento"},
    422: {"model": RespuestaError, "description": "Datos inválidos"},
    502: {"model": RespuestaError, "description": "No se pudo contactar al proveedor DIAN"},
}


def _original_del_cliente(id_publico: str, cliente: dict) -> dict:
    """El documento que se corrige, comprobando que sea de quien lo pide."""
    documento = get_documento(id_publico, cliente["cod_cliente_api"])
    if not documento:
        raise _error(status.HTTP_404_NOT_FOUND, "documento_no_encontrado",
                     "No existe ese documento.", campo="documento")

    if documento.get("tipo") != "FV":
        raise _error(status.HTTP_409_CONFLICT, "documento_no_corregible",
                     "Solo se pueden emitir notas sobre una factura de venta.",
                     campo="documento")

    if documento.get("estado") == "RECHAZADO":
        raise _error(status.HTTP_409_CONFLICT, "documento_rechazado",
                     "Ese documento fue rechazado y nunca tuvo efecto: no hay nada "
                     "que corregir con una nota.", campo="documento")

    return documento


def _ya_emitida(cliente: dict, referencia: str, peticion: Request,
                respuesta_http: Response):
    """Idempotencia: la misma referencia devuelve la nota que ya existe."""
    if not referencia:
        return None
    existente = get_documento_por_referencia(cliente["cod_cliente_api"], referencia)
    if not existente:
        return None
    respuesta_http.status_code = status.HTTP_200_OK
    completo = get_documento(existente["id_publico"], cliente["cod_cliente_api"])
    return con_ultimo_evento(respuesta_documento(completo, peticion), completo)


def _emitir(cliente: dict, tipo: str, calculo: dict, original: dict, motivo: str,
            datos, peticion: Request, tareas=None) -> FacturaResponse:
    """El tramo que comparten las dos notas: numerar, guardar y transmitir."""
    empresa = get_branch_by_id(cliente["cod_empresa"])
    if not empresa:
        raise _error(status.HTTP_409_CONFLICT, "emisor_no_configurado",
                     "El cliente no tiene una empresa emisora configurada.")
    emisor = emisor_desde_empresa(empresa)
    receptor = get_receptor(original["cod_receptor"])
    proveedor = proveedor_o_error()

    referencias = {
        "motivo_nota": motivo,
        "numero_referencia": original.get("numero"),
        "cufe_referencia": original.get("cufe"),
        "fecha_referencia": original.get("fecha_emision"),
    }

    def cufe_de(cab):
        return generate_cufe({
            "numero_factura": cab["numero"],
            "fecha": cab["fecha_emision"],
            "subtotal": calculo["subtotal"],
            "total_impuestos": calculo["total_impuestos"],
            "total": calculo["total"],
            "document_number": receptor.get("numero_documento", ""),
        }, empresa)

    def xml_de(cab, _cod_receptor):
        cabecera, lineas, emi = a_documento_canonico(
            {"numero": cab["numero"], "tipo": tipo, "fecha_emision": cab["fecha_emision"],
             "fecha_vencimiento": None, "cufe": cab["cufe"], "forma_pago": "CONTADO",
             "observaciones": motivo,
             "subtotal": calculo["subtotal"], "total_descuentos": calculo["total_descuentos"],
             "total_impuestos": calculo["total_impuestos"], "total": calculo["total"],
             **referencias},
            lineas_para_guardar(calculo), receptor, emisor)
        return generate_invoice_xml(cabecera, lineas, emi)

    try:
        emitido = reservar_y_guardar(
            cliente, tipo, calculo, receptor, cufe_de, xml_de,
            {"forma_pago": "CONTADO", "plazo_dias": 0,
             "referencia_externa": datos.referencia_externa,
             "observaciones": motivo, "proveedor_dian": proveedor.nombre,
             "cod_documento_referencia": original["cod_documento"],
             **referencias})
    except RangoResolucionAgotadoError as e:
        raise _error(status.HTTP_409_CONFLICT, "rango_agotado", str(e))

    documento = get_documento(emitido["id_publico"], cliente["cod_cliente_api"])
    cabecera, lineas, emi = a_documento_canonico(
        documento, get_lineas(documento["cod_documento"]), receptor, emisor)

    try:
        respuesta = proveedor.transmitir(cabecera, lineas, emi, emitido["xml"])
    except ErrorProveedorDian as e:
        raise _error(status.HTTP_502_BAD_GATEWAY, "proveedor_no_disponible", str(e))

    registrar_transmision(documento["cod_documento"], respuesta)

    # La anulación queda anotada en el documento original y no solo en la nota: es
    # ahí donde va a mirar quien pregunte por la factura, no en un documento que
    # todavía no sabe que existe.
    if tipo == "NC":
        registrar_evento(original["cod_documento"], "ANULADO",
                         mensaje=f"Nota crédito {emitido['numero']}: {motivo}")

    if datos.enviar_email and tareas is not None:
        tareas.add_task(enviar_por_correo, emitido["id_publico"])

    documento = get_documento(emitido["id_publico"], cliente["cod_cliente_api"])
    salida = respuesta_documento(documento, peticion)
    salida.qr = respuesta.qr
    salida.dian = ResultadoDian(proveedor=respuesta.proveedor, codigo=respuesta.codigo,
                                mensaje=respuesta.mensaje)
    return salida


@router.post("/notas-credito", response_model=FacturaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Emitir una nota crédito",
             responses=RESPUESTAS)
def emitir_nota_credito(datos: NotaCreditoRequest, cliente: ClienteAPI,
                        peticion: Request, respuesta_http: Response,
                        tareas: BackgroundTasks) -> FacturaResponse:
    """Anula una factura completa o devuelve unas cantidades de ella.

    **Sin `items` se anula el documento entero**, que es el caso más común. Con
    `items` se devuelve solo lo que se indique, y de cada línea vuelve la parte
    proporcional de su base, su descuento y su IVA.

    Los precios salen del documento original: no se pueden enviar otros. Devolver
    a un precio distinto del que se cobró convertiría una devolución en una
    transferencia de dinero.
    """
    ya = _ya_emitida(cliente, datos.referencia_externa, peticion, respuesta_http)
    if ya:
        return ya

    original = _original_del_cliente(datos.documento, cliente)
    lineas_originales = get_lineas(original["cod_documento"])

    devoluciones = None
    if datos.items:
        por_orden = {int(l["orden"]): l for l in lineas_originales}
        devoluciones = {}
        for item in datos.items:
            linea = por_orden.get(item.linea)
            if not linea:
                raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "linea_inexistente",
                             f"El documento no tiene una línea {item.linea}.",
                             campo="items")
            disponible = float(linea["cantidad"]) - _ya_devuelto(original, item.linea)
            if item.cantidad > disponible + 0.0001:
                raise _error(
                    status.HTTP_409_CONFLICT, "cantidad_no_disponible",
                    f"De la línea {item.linea} quedan {disponible:g} por devolver y "
                    f"se pidieron {item.cantidad:g}.", campo="items")
            devoluciones[item.linea] = item.cantidad

    calculo = calcular_nota_credito(lineas_originales, devoluciones)
    if not calculo["lineas"]:
        raise _error(status.HTTP_422_UNPROCESSABLE_ENTITY, "nota_vacia",
                     "La nota no devuelve ninguna cantidad.", campo="items")

    return _emitir(cliente, "NC", calculo, original, datos.motivo, datos, peticion,
                   tareas)


def _ya_devuelto(original: dict, orden: int) -> float:
    """Cuánto se devolvió antes de esta línea, en notas anteriores.

    Sin esto, dos devoluciones parciales seguidas podrían devolver más unidades de
    las que se vendieron.
    """
    fila = get_one(
        "SELECT COALESCE(SUM(l.cantidad), 0) AS n "
        "FROM documentos d JOIN documento_lineas l ON l.cod_documento = d.cod_documento "
        "WHERE d.cod_documento_referencia = %s AND d.tipo = 'NC' "
        "  AND d.estado <> 'RECHAZADO' AND l.orden = %s",
        (original["cod_documento"], orden))
    return float(fila["n"] if fila else 0)


@router.post("/notas-debito", response_model=FacturaResponse,
             status_code=status.HTTP_201_CREATED,
             summary="Emitir una nota débito",
             responses=RESPUESTAS)
def emitir_nota_debito(datos: NotaDebitoRequest, cliente: ClienteAPI,
                       peticion: Request, respuesta_http: Response,
                       tareas: BackgroundTasks) -> FacturaResponse:
    """Agrega un cargo sobre una factura ya emitida: un flete, un interés, un ajuste.

    `incluye_impuesto` decide cómo se lee `valor`: con `true` el IVA va adentro y
    se descompone; con `false` es una base y el IVA se suma encima. Si no se manda
    `porcentaje_impuesto`, se usa la tarifa promedio que llevó la factura original,
    que es la que corresponde a un cargo que no pertenece a ninguna línea.
    """
    ya = _ya_emitida(cliente, datos.referencia_externa, peticion, respuesta_http)
    if ya:
        return ya

    original = _original_del_cliente(datos.documento, cliente)

    tarifa = datos.porcentaje_impuesto
    if tarifa is None:
        tarifa = tasa_promedio(original.get("subtotal"), original.get("total_impuestos"))

    calculo = calcular_nota_debito(datos.valor, tarifa, datos.incluye_impuesto)

    # La nota débito también lleva línea: sin InvoiceLine el XML no es válido. El
    # ajuste es un concepto, no un producto del catálogo del cliente.
    calculo["lineas"] = [{
        "codigo": None,
        "descripcion": datos.motivo,
        "unidad_medida": "WSD",
        "cantidad": 1,
        "precio_unitario": calculo["subtotal"],
        "valor_bruto": calculo["subtotal"],
        "descuento_porcentaje": 0,
        "descuento_valor": 0,
        "subtotal": calculo["subtotal"],
        "impuesto_codigo_dian": "01",
        "impuesto_porcentaje": calculo["impuesto_porcentaje"],
        "impuesto_valor": calculo["total_impuestos"],
    }]

    return _emitir(cliente, "ND", calculo, original, datos.motivo, datos, peticion,
                   tareas)
