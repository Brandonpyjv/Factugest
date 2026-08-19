"""
Contrato de la API de integración.

Estos modelos son lo que el sistema del cliente ve y contra lo que programa, así
que cambiarlos rompe integraciones: cualquier cambio incompatible sale en
`/api/v2/` y la v1 se mantiene hasta que migren.

**Las reglas no se escriben aquí.** Salen de `services/validaciones.py`, las
mismas que usan los formularios web. Repetirlas sería tener dos definiciones de
«qué es una cédula válida» que empiezan iguales y terminan distintas. Esta es la
tarea V.8 del track de validación.
"""
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from services.validaciones import (CODIGOS_IMPUESTO_DIAN, ErrorValidacion,
                                   REGIMENES_TRIBUTARIOS, TIPOS_PERSONA, cantidad,
                                   correo, nombre_persona, numero_documento, opcion,
                                   porcentaje, precio, razon_social, telefono, texto,
                                   tipo_documento)

FORMAS_PAGO = ("CONTADO", "CREDITO")


def regla(funcion, *args, **kwargs):
    """Aplica una regla del dominio como validador de Pydantic.

    Traduce `ErrorValidacion` a `ValueError`, que es lo que Pydantic entiende y
    lo que FastAPI convierte en un 422 con el campo señalado.
    """
    try:
        return funcion(*args, **kwargs)
    except ErrorValidacion as e:
        raise ValueError(e.mensaje)


# ── Petición ────────────────────────────────────────────────────────────────

class Impuesto(BaseModel):
    codigo: str = Field(default="01",
                        description="Código del anexo técnico DIAN. 01 = IVA")
    porcentaje: float = Field(default=0, description="Tarifa aplicada a la línea",
                              examples=[19])

    @field_validator("codigo")
    @classmethod
    def _codigo(cls, v):
        return regla(opcion, (v or "01").strip().upper(),
                     tuple(CODIGOS_IMPUESTO_DIAN), campo="codigo")

    @field_validator("porcentaje")
    @classmethod
    def _porcentaje(cls, v):
        return regla(porcentaje, v, campo="porcentaje")


class Item(BaseModel):
    codigo: str | None = Field(default=None, max_length=60,
                               description="Referencia del producto en el sistema del "
                                           "cliente. No se valida contra nuestro catálogo.")
    descripcion: str = Field(description="Lo que se imprime en la factura",
                             examples=["Teclado mecánico Redragon K552"])
    cantidad: float = Field(description="Admite decimales: kilos, horas, metros",
                            examples=[2])
    precio_unitario: float = Field(description="Antes de impuestos", examples=[189000])
    unidad_medida: str = Field(default="94", max_length=10)
    descuento_porcentaje: float = Field(default=0, examples=[5])
    descuento_descripcion: str | None = Field(default=None, max_length=200)
    impuesto: Impuesto = Field(default_factory=Impuesto)

    @field_validator("descripcion")
    @classmethod
    def _descripcion(cls, v):
        return regla(texto, v, campo="descripcion", maximo=300, minimo=1)

    @field_validator("cantidad")
    @classmethod
    def _cantidad(cls, v):
        # Fraccionaria: la DIAN admite unidades no enteras y un POS puede vender
        # medio kilo. El mínimo evita la línea de cantidad cero.
        return regla(cantidad, v, campo="cantidad", minimo=0.001, fraccionaria=True)

    @field_validator("precio_unitario")
    @classmethod
    def _precio(cls, v):
        return regla(precio, v, campo="precio_unitario")

    @field_validator("descuento_porcentaje")
    @classmethod
    def _descuento(cls, v):
        return regla(porcentaje, v, campo="descuento_porcentaje")


class Receptor(BaseModel):
    tipo_documento: str = Field(description="Código DIAN: 13 cédula, 31 NIT, 41 pasaporte",
                                examples=["13"])
    numero_documento: str = Field(examples=["1090234567"])
    dv: str | None = Field(default=None, max_length=1,
                           description="Dígito de verificación, solo para NIT")
    nombre: str = Field(examples=["María Fernanda Ospina"])
    tipo_persona: str = Field(default="NATURAL")
    regimen_tributario: str = Field(default="NO_RESPONSABLE_IVA")
    email: str | None = Field(default=None,
                              description="Si se envía, es a donde llega la factura")
    telefono: str | None = None
    direccion: str | None = Field(default=None, max_length=200)
    cod_municipio: str | None = Field(default=None, max_length=5,
                                      description="Código DANE. 54001 = Cúcuta",
                                      examples=["54001"])

    @field_validator("tipo_documento")
    @classmethod
    def _tipo(cls, v):
        return regla(tipo_documento, v, campo="tipo_documento")

    @field_validator("tipo_persona")
    @classmethod
    def _persona(cls, v):
        return regla(opcion, v, TIPOS_PERSONA, campo="tipo_persona")

    @field_validator("regimen_tributario")
    @classmethod
    def _regimen(cls, v):
        return regla(opcion, v, REGIMENES_TRIBUTARIOS, campo="regimen_tributario")

    @field_validator("email")
    @classmethod
    def _email(cls, v):
        return regla(correo, v, campo="email") or None

    @field_validator("telefono")
    @classmethod
    def _telefono(cls, v):
        return regla(telefono, v, campo="telefono") or None

    @model_validator(mode="after")
    def _documento_segun_su_tipo(self):
        """La identificación depende del tipo: una cédula solo admite dígitos y un
        pasaporte admite letras. Por eso se validan juntos y no por separado."""
        self.numero_documento = regla(numero_documento, self.numero_documento,
                                      tipo=self.tipo_documento,
                                      campo="numero_documento")
        # El nombre de una empresa lleva dígitos —«Comercial 3M S.A.S.»— y el de
        # una persona no.
        funcion = razon_social if self.tipo_persona == "JURIDICA" else nombre_persona
        self.nombre = regla(funcion, self.nombre, campo="nombre")
        return self


class DescuentoGlobal(BaseModel):
    valor: float = Field(default=0, description="En pesos, no en porcentaje")
    descripcion: str | None = Field(default=None, max_length=200)

    @field_validator("valor")
    @classmethod
    def _valor(cls, v):
        if v is None:
            return 0.0
        if float(v) < 0:
            raise ValueError("No puede ser negativo")
        return round(float(v), 2)


class FacturaRequest(BaseModel):
    referencia_externa: str | None = Field(
        default=None, max_length=80,
        description="Identificador de la venta en el sistema del cliente. Si se "
                    "reenvía el mismo, se devuelve el documento ya emitido en lugar "
                    "de emitir otro.",
        examples=["VENTA-1043"])
    receptor: Receptor = Field(description="A quién se le factura")
    items: list[Item] = Field(min_length=1, max_length=200,
                              description="Líneas de la factura. Al menos una.")
    forma_pago: str = Field(default="CONTADO",
                            description="CONTADO o CREDITO. A crédito hace falta plazo.")
    plazo_dias: int = Field(default=0, ge=0, le=365,
                            description="Días para el vencimiento. 0 = contado")
    descuento_global: DescuentoGlobal | None = Field(
        default=None,
        description="Descuento sobre el total, aparte de los de cada línea. "
                    "El IVA se prorratea.")
    observaciones: str | None = Field(default=None, max_length=1000,
                                      description="Texto libre que sale en la factura")
    orden_compra: str | None = Field(default=None, max_length=100,
                                     description="Orden de compra del comprador, si la hay")
    enviar_email: bool = Field(default=False,
                               description="Enviar la factura al correo del receptor")

    @field_validator("forma_pago")
    @classmethod
    def _forma(cls, v):
        return regla(opcion, (v or "CONTADO").strip().upper(), FORMAS_PAGO,
                     campo="forma_pago")

    @model_validator(mode="after")
    def _coherencia(self):
        if self.forma_pago == "CREDITO" and self.plazo_dias == 0:
            raise ValueError("Una venta a crédito necesita un plazo mayor que cero")
        if self.forma_pago == "CONTADO" and self.plazo_dias:
            raise ValueError("Una venta de contado no lleva plazo")

        # El descuento de factura no puede pasarse de la base sobre la que se
        # aplica: más allá, el total quedaría en negativo.
        descuento = self.descuento_global.valor if self.descuento_global else 0
        if descuento:
            base = sum(i.precio_unitario * i.cantidad *
                       (1 - i.descuento_porcentaje / 100) for i in self.items)
            if descuento > round(base, 2):
                raise ValueError(
                    f"El descuento global ({descuento}) no puede pasar de la base "
                    f"gravable ({round(base, 2)})")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "referencia_externa": "VENTA-1043",
                "receptor": {
                    "tipo_documento": "13",
                    "numero_documento": "1090234567",
                    "nombre": "María Fernanda Ospina",
                    "email": "mospina@correo.com",
                    "direccion": "Av. 0 # 12-45",
                    "cod_municipio": "54001",
                    "tipo_persona": "NATURAL",
                    "regimen_tributario": "NO_RESPONSABLE_IVA",
                },
                "items": [{
                    "codigo": "SKU-TEC-014",
                    "descripcion": "Teclado mecánico Redragon K552",
                    "cantidad": 2,
                    "precio_unitario": 189000,
                    "unidad_medida": "94",
                    "descuento_porcentaje": 5,
                    "impuesto": {"codigo": "01", "porcentaje": 19},
                }],
                "forma_pago": "CONTADO",
                "plazo_dias": 0,
                "enviar_email": True,
            }]
        }
    }


# ── Notas ───────────────────────────────────────────────────────────────────

class LineaDevuelta(BaseModel):
    """Qué se devuelve de una línea del documento original.

    Se identifica por `linea` —el orden con el que se emitió, empezando en 1— y no
    por el código del producto: un mismo código puede aparecer dos veces en una
    factura, y por código no habría forma de saber de cuál de las dos se está
    devolviendo.
    """
    linea: int = Field(ge=1, description="Número de línea del documento original",
                       examples=[1])
    cantidad: float = Field(description="Cuánto se devuelve de esa línea. No puede "
                                        "pasar de lo que se facturó.",
                            examples=[1])

    @field_validator("cantidad")
    @classmethod
    def _cantidad(cls, v):
        return regla(cantidad, v, campo="cantidad", minimo=0.001, fraccionaria=True)


class NotaCreditoRequest(BaseModel):
    documento: str = Field(
        description="Identificador del documento que se corrige, el que devolvió "
                    "la emisión",
        examples=["doc_7f21c9a4"])
    motivo: str = Field(description="Por qué se emite. Sale impresa en la nota.",
                        examples=["Devolución de mercancía en mal estado"])
    items: list[LineaDevuelta] | None = Field(
        default=None,
        description="Qué se devuelve. **Omitirlo anula el documento completo**, "
                    "que es el caso más común.")
    referencia_externa: str | None = Field(
        default=None, max_length=80,
        description="Identificador de la devolución en el sistema del cliente. "
                    "Reenviar el mismo devuelve la nota ya emitida.",
        examples=["DEV-1043"])
    enviar_email: bool = Field(default=False)

    @field_validator("motivo")
    @classmethod
    def _motivo(cls, v):
        return regla(texto, v, campo="motivo", maximo=300, minimo=5)

    @model_validator(mode="after")
    def _sin_lineas_repetidas(self):
        if self.items:
            vistas = [i.linea for i in self.items]
            if len(vistas) != len(set(vistas)):
                raise ValueError("Hay una misma línea repetida en la devolución")
        return self

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"documento": "doc_7f21c9a4", "motivo": "Anulación por error de digitación"},
                {"documento": "doc_7f21c9a4",
                 "motivo": "Devolución de una unidad en mal estado",
                 "items": [{"linea": 1, "cantidad": 1}],
                 "referencia_externa": "DEV-1043"},
            ]
        }
    }


class NotaDebitoRequest(BaseModel):
    documento: str = Field(description="Identificador del documento al que se le "
                                       "agrega el cargo",
                           examples=["doc_7f21c9a4"])
    motivo: str = Field(description="Qué se está cobrando de más",
                        examples=["Flete de entrega a domicilio"])
    valor: float = Field(gt=0, description="Cuánto se agrega, en pesos",
                         examples=[50000])
    incluye_impuesto: bool = Field(
        default=True,
        description="`true`: el valor ya trae el IVA adentro y se descompone. "
                    "`false`: es una base y el IVA se suma encima. Confundirlos "
                    "cambia lo que paga el comprador.")
    porcentaje_impuesto: float | None = Field(
        default=None,
        description="Tarifa del ajuste. Si se omite, se usa la tarifa promedio "
                    "que llevó el documento original.",
        examples=[19])
    referencia_externa: str | None = Field(default=None, max_length=80)
    enviar_email: bool = Field(default=False)

    @field_validator("motivo")
    @classmethod
    def _motivo(cls, v):
        return regla(texto, v, campo="motivo", maximo=300, minimo=5)

    @field_validator("valor")
    @classmethod
    def _valor(cls, v):
        return regla(precio, v, campo="valor")

    @field_validator("porcentaje_impuesto")
    @classmethod
    def _tarifa(cls, v):
        return None if v is None else regla(porcentaje, v, campo="porcentaje_impuesto")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "documento": "doc_7f21c9a4",
                "motivo": "Flete de entrega a domicilio",
                "valor": 50000,
                "incluye_impuesto": True,
                "referencia_externa": "ND-1043",
            }]
        }
    }


# ── Respuesta ───────────────────────────────────────────────────────────────

class Totales(BaseModel):
    bruto: float = Field(description="Suma de las líneas antes de descuentos")
    descuentos: float
    base_gravable: float = Field(description="Sobre lo que se calculan los impuestos")
    impuestos: float
    total: float = Field(description="Lo que paga el comprador")


class ResultadoDian(BaseModel):
    proveedor: str = Field(examples=["simulado"])
    codigo: str = Field(examples=["00"])
    mensaje: str


class FacturaResponse(BaseModel):
    id: str = Field(description="Identificador del documento en FactuGest",
                    examples=["doc_7f21c9a4"])
    numero: str = Field(description="Número con el prefijo de la resolución",
                        examples=["SETP42"])
    tipo: str = Field(default="FV", description="FV factura · NC nota crédito · ND nota débito")
    cufe: str | None = Field(default=None,
                             description="Código Único de Factura Electrónica")
    estado: str = Field(description="ACEPTADO · RECHAZADO · PENDIENTE · ERROR")
    fecha_emision: datetime = Field(description="Cuándo se emitió, hora de Colombia")
    fecha_vencimiento: str | None = Field(default=None,
                                          description="Solo en ventas a crédito")
    totales: Totales = Field(description="Calculados por FactuGest, no por el cliente")
    qr: str | None = Field(default=None,
                           description="Enlace de verificación que va en la representación gráfica")
    pdf_url: str | None = Field(default=None, description="Dónde descargar el PDF")
    xml_url: str | None = Field(default=None, description="Dónde descargar el XML UBL")
    documento_referencia: str | None = Field(
        default=None,
        description="En una nota, el documento que corrige",
        examples=["doc_7f21c9a4"])
    anulado: bool = Field(
        default=False,
        description="Si una nota crédito por el total ya dejó sin efecto este "
                    "documento. `estado` no cambia: sigue contando lo que "
                    "respondió la DIAN cuando se emitió.")
    dian: ResultadoDian = Field(description="Qué respondió el proveedor")

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": "doc_7f21c9a4",
                "numero": "SETP42",
                "tipo": "FV",
                "cufe": "a91f…3d70",
                "estado": "ACEPTADO",
                "fecha_emision": "2026-08-18T14:22:07",
                "fecha_vencimiento": None,
                "totales": {"bruto": 378000, "descuentos": 18900,
                            "base_gravable": 359100, "impuestos": 68229,
                            "total": 427329},
                "qr": "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey=a91f…",
                "pdf_url": "/api/v1/documentos/doc_7f21c9a4/pdf",
                "xml_url": "/api/v1/documentos/doc_7f21c9a4/xml",
                "dian": {"proveedor": "simulado", "codigo": "00",
                         "mensaje": "Documento validado por el proveedor simulado"},
            }]
        }
    }


class DocumentoResumen(BaseModel):
    """Una fila del listado. Para el detalle completo está `GET /documentos/{id}`."""
    id: str = Field(examples=["doc_7f21c9a4"])
    numero: str | None = None
    tipo: str = Field(examples=["FV"])
    estado: str = Field(examples=["ACEPTADO"])
    fecha_emision: datetime
    total: float
    cufe: str | None = None
    referencia_externa: str | None = Field(
        default=None, description="El identificador de la venta en el sistema del "
                                  "cliente, para conciliar contra sus propios datos")


class ListaDocumentos(BaseModel):
    """Los documentos de un cliente, paginados.

    `total` es cuántos hay con esos filtros, no cuántos vienen en esta página: es
    lo que permite saber si falta traer más sin pedir una página de más.
    """
    total: int = Field(description="Documentos que cumplen el filtro", examples=[412])
    pagina: int = Field(examples=[1])
    por_pagina: int = Field(examples=[50])
    paginas: int = Field(description="Cuántas páginas hay en total", examples=[9])
    documentos: list[DocumentoResumen]


class ErrorRespuesta(BaseModel):
    """El detalle de un error. Siempre viaja dentro de `RespuestaError`."""
    codigo: str = Field(
        description="Identificador estable del error. Es contra esto que se "
                    "programa: el mensaje está escrito para leerlo y puede "
                    "cambiar de redacción.",
        examples=["llave_invalida"])
    mensaje: str = Field(description="Explicación para una persona",
                         examples=["La llave no es válida."])
    campo: str | None = Field(default=None,
                              description="Ruta del dato que falló dentro del "
                                          "cuerpo enviado, cuando el problema es "
                                          "de un campo concreto",
                              examples=["items.0.cantidad"])


class RespuestaError(BaseModel):
    """Todos los errores de la API salen así, del 401 al 500.

    Un solo bloque de manejo de errores sirve para toda la integración.
    """
    detail: ErrorRespuesta

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "detail": {
                    "codigo": "rango_agotado",
                    "mensaje": "El consecutivo 5001 está fuera del rango autorizado "
                               "1–5000 de la resolución DIAN",
                    "campo": None,
                }
            }]
        }
    }
