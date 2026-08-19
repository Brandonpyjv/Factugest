"""
Configuración: un solo sitio para los catálogos que se tocan de vez en cuando.

Impuestos, descuentos, métodos de pago y estados de pago vivían sueltos en el
menú lateral, al mismo nivel que facturar. No es donde van: no son trabajo del
día, son parámetros que se ajustan cuando algo cambia. Aquí quedan agrupados por
para qué sirven, con el conteo al lado para saber si están configurados sin tener
que entrar a mirar.

La página anterior mostraba el framework y el motor de base de datos, que no es
configuración de nada. Eso se fue.
"""
import os

from fastapi import APIRouter, Request

from database import get_one
from services.autoservicio_client import configurado as autoservicio_configurado
from templates_config import templates

router = APIRouter(prefix="/configuracion")


def _cuantos(tabla: str, condicion: str = "") -> int:
    fila = get_one(f"SELECT COUNT(*) AS n FROM {tabla} {condicion}")
    return int(fila["n"] if fila else 0)


@router.get("", name="configuracion")
def configuracion(request: Request):
    return templates.TemplateResponse(request, "configuracion/index.html", {
        "conteos": {
            "impuestos":       _cuantos("impuestos"),
            "descuentos":      _cuantos("descuentos"),
            "metodos_pago":    _cuantos("metodos_pago"),
            "estados_pago":    _cuantos("pagos_factura"),
            "empresas":        _cuantos("empresas"),
            "usuarios":        _cuantos("usuarios", "WHERE activo = 1"),
            "clientes_api":    _cuantos("clientes_api", "WHERE estado = 'ACTIVO'"),
            "documentos":      _cuantos("documentos"),
        },
        "proveedor_dian": os.getenv("DIAN_PROVEEDOR", "simulado"),
        "autoservicio": autoservicio_configurado(),
        "rol": request.session.get("user", {}).get("rol", ""),
    })
