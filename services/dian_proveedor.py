"""
Adaptador del proveedor con el que se transmite a la DIAN.

Esta es la costura del proyecto. Hoy no hay conexión real: el proveedor
`simulado` valida el documento y lo da por aceptado. Cuando se consiga el plan
con Factus, entra `factus` implementando esta misma interfaz y **no cambia nada
más**: ni el endpoint, ni el almacenamiento, ni el PDF, ni el panel.

Se elige con la variable de entorno `DIAN_PROVEEDOR`. En desarrollo se deja en
`simulado` para no gastar cupo real en pruebas.

El simulador no es un `return True`. Comprueba lo mismo que rechazaría la DIAN
—que los totales cuadren, que el CUFE tenga la forma correcta, que el XML esté
bien formado, que el emisor y el receptor estén identificados— y por eso sirve:
encuentra los errores de *nuestra* generación antes de que exista un proveedor
real al que echarle la culpa.
"""
import hashlib
import os
from dataclasses import dataclass, field
from datetime import datetime
# Se importa la función y no el módulo: el parámetro se llama `xml` y taparía a
# `xml.dom.minidom`.
from xml.dom.minidom import parseString

# Catálogo de habilitación de la DIAN, no el de producción: mientras el CUFE se
# calcule con tipAmbiente = 2, apuntar al de producción sería mentir.
CATALOGO_QR = "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey="

ACEPTADO = "ACEPTADO"
RECHAZADO = "RECHAZADO"
ERROR = "ERROR"


@dataclass
class RespuestaDian:
    """Lo que devuelve un proveedor. Es el contrato que `factus` tendrá que cumplir.

    Se usa una clase y no un dict porque esto lo va a implementar otra persona
    contra otro servicio: los campos tienen que estar escritos en alguna parte.

    `numero`, `cufe`, `xml` y `pdf` vienen en blanco con el simulador porque los
    generamos nosotros, pero un proveedor real puede devolver los suyos —Factus
    asigna su propia numeración y firma el XML—, y entonces mandan los de él.
    """
    estado: str
    codigo: str
    mensaje: str
    proveedor: str
    aceptado: bool = False
    numero: str = None
    cufe: str = None
    qr: str = None
    xml: str = None
    pdf: bytes = None
    payload: dict = field(default_factory=dict)


class ErrorProveedorDian(Exception):
    """El proveedor no se pudo contactar o contestó algo que no se entiende.

    Es distinto de un documento rechazado: rechazado significa que llegó y no
    pasó; esto significa que ni siquiera se supo si llegó.
    """


class ProveedorDian:
    """Interfaz que implementa cada proveedor."""

    nombre = "base"
    ambiente = "2"   # 1 producción · 2 habilitación

    def transmitir(self, cabecera: dict, lineas: list, emisor: dict,
                   xml: str) -> RespuestaDian:
        """Envía el documento y devuelve el resultado.

        Recibe el documento canónico (ver `services/documento_canonico.py`) más
        el XML ya generado. No debe lanzar por un documento rechazado: eso se
        informa con `estado = RECHAZADO`. `ErrorProveedorDian` se reserva para
        cuando falla la comunicación.
        """
        raise NotImplementedError


# ── Proveedor simulado ──────────────────────────────────────────────────────

class ProveedorSimulado(ProveedorDian):
    """Valida el documento y lo da por aceptado, sin salir a ninguna parte."""

    nombre = "simulado"

    def transmitir(self, cabecera, lineas, emisor, xml) -> RespuestaDian:
        problemas = self._revisar(cabecera, lineas, emisor, xml)
        if problemas:
            return RespuestaDian(
                estado=RECHAZADO,
                codigo="RCH-001",
                mensaje="; ".join(problemas),
                proveedor=self.nombre,
                payload={"proveedor": self.nombre, "ambiente": self.ambiente,
                         "problemas": problemas},
            )

        cufe = str(cabecera.get("cufe") or "")
        # El acuse se deriva del CUFE en lugar de ser aleatorio, para que repetir
        # una prueba dé siempre el mismo resultado.
        acuse = hashlib.sha1(cufe.encode("utf-8")).hexdigest()[:24]

        return RespuestaDian(
            estado=ACEPTADO,
            codigo="00",
            mensaje="Documento validado por el proveedor simulado",
            proveedor=self.nombre,
            aceptado=True,
            qr=CATALOGO_QR + cufe,
            payload={
                "proveedor": self.nombre,
                "ambiente": self.ambiente,
                "acuse": acuse,
                "recibido_en": datetime.now().isoformat(timespec="seconds"),
                "advertencia": "Documento no transmitido a la DIAN: proveedor simulado",
            },
        )

    # ── Comprobaciones ──────────────────────────────────────────────────────

    def _revisar(self, cabecera, lineas, emisor, xml) -> list:
        problemas = []
        cabecera = cabecera or {}
        emisor = emisor or {}
        lineas = lineas or []

        if not str(cabecera.get("numero_factura") or "").strip():
            problemas.append("el documento no tiene número")

        cufe = str(cabecera.get("cufe") or "").strip()
        if not cufe:
            problemas.append("el documento no tiene CUFE")
        elif len(cufe) != 96 or not all(c in "0123456789abcdef" for c in cufe.lower()):
            # El CUFE es un SHA-384 en hexadecimal: 96 caracteres.
            problemas.append("el CUFE no tiene la forma de un SHA-384")

        if not str(emisor.get("nit") or "").strip():
            problemas.append("el emisor no tiene NIT")
        if not str(cabecera.get("document_number") or "").strip():
            problemas.append("el receptor no está identificado")

        if not lineas:
            problemas.append("el documento no tiene líneas")

        problemas += self._revisar_totales(cabecera, lineas)

        if not (xml or "").strip():
            problemas.append("no se generó el XML")
        else:
            try:
                parseString(xml.encode("utf-8"))
            except Exception as e:
                problemas.append(f"el XML no está bien formado ({e})")

        fecha = cabecera.get("fecha")
        if hasattr(fecha, "date") and fecha.date() > datetime.now().date():
            problemas.append("la fecha de emisión está en el futuro")

        return problemas

    @staticmethod
    def _revisar_totales(cabecera, lineas) -> list:
        """Los totales de la cabecera tienen que corresponder a las líneas.

        Es la comprobación que más veces salva: un descuadre aquí significa que
        el documento impreso y el transmitido no dicen lo mismo.
        """
        def num(valor):
            try:
                return round(float(valor or 0), 2)
            except (TypeError, ValueError):
                return None

        problemas = []
        subtotal = num(cabecera.get("subtotal"))
        impuestos = num(cabecera.get("total_impuestos"))
        total = num(cabecera.get("total"))
        if None in (subtotal, impuestos, total):
            return ["los totales no son numéricos"]

        # Se compara en valor absoluto porque una nota crédito los lleva negativos.
        if abs(abs(total) - abs(round(subtotal + impuestos, 2))) > 0.01:
            problemas.append(
                f"el total ({total}) no corresponde a la base más los impuestos "
                f"({round(subtotal + impuestos, 2)})")

        suma_lineas = sum(num(l.get("subtotal")) or 0 for l in lineas)
        suma_impuestos = sum(num(l.get("impuesto_valor")) or 0 for l in lineas)
        descuento_global = abs(round(suma_lineas, 2)) - abs(subtotal)
        if descuento_global < -0.01:
            problemas.append(
                f"la base gravable ({subtotal}) es mayor que la suma de las líneas "
                f"({round(suma_lineas, 2)})")
        # Con descuento global el IVA se prorratea, así que solo se exige que no
        # sea mayor que el de las líneas.
        if abs(impuestos) - abs(round(suma_impuestos, 2)) > 0.01:
            problemas.append(
                f"los impuestos ({impuestos}) superan la suma de los de cada línea "
                f"({round(suma_impuestos, 2)})")

        return problemas


# ── Selección del proveedor ─────────────────────────────────────────────────

_PROVEEDORES = {
    "simulado": ProveedorSimulado,
}

# Se implementa en la fase 7; se nombra aquí para que el error diga qué falta en
# lugar de «proveedor desconocido».
_PENDIENTES = {
    "factus": "El proveedor «factus» todavía no está implementado (tarea 7.2). "
              "Deja DIAN_PROVEEDOR=simulado mientras tanto.",
}


def get_proveedor(nombre: str = None) -> ProveedorDian:
    """Devuelve el proveedor configurado.

    Sin argumento lo toma de `DIAN_PROVEEDOR`, que por defecto es `simulado`.
    """
    nombre = (nombre or os.getenv("DIAN_PROVEEDOR") or "simulado").strip().lower()
    if nombre in _PROVEEDORES:
        return _PROVEEDORES[nombre]()
    if nombre in _PENDIENTES:
        raise ErrorProveedorDian(_PENDIENTES[nombre])
    raise ErrorProveedorDian(
        f"Proveedor DIAN desconocido: «{nombre}». "
        f"Disponibles: {', '.join(sorted(_PROVEEDORES))}.")


def proveedores_disponibles() -> list:
    return sorted(_PROVEEDORES)
