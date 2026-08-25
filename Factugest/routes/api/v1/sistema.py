"""Endpoints de servicio de la API: comprobar que la llave sirve."""
from fastapi import APIRouter
from pydantic import BaseModel, Field

from routes.api.v1.dependencias import ClienteAPI

router = APIRouter(prefix="/api/v1", tags=["Sistema"])


class Emisor(BaseModel):
    cod_empresa: int = Field(description="Identificador de la empresa emisora")
    nombre: str | None = Field(default=None, description="Razón social del emisor")
    nit: str | None = Field(default=None, description="NIT con el que se emite")


class RespuestaPing(BaseModel):
    ok: bool = True
    cliente: str = Field(description="Nombre del cliente integrado")
    plan: str
    emisor: Emisor

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "ok": True,
                "cliente": "Siste Soluciones",
                "plan": "BASICO",
                "emisor": {"cod_empresa": 3, "nombre": "Siste Soluciones S.A.S.",
                           "nit": "901555444"},
            }]
        }
    }


@router.get("/ping", response_model=RespuestaPing, summary="Verificar la llave",
            responses={
                401: {"description": "Falta la llave o no es válida"},
                403: {"description": "El cliente está suspendido o revocado"},
            })
def ping(cliente: ClienteAPI):
    """Confirma que la llave sirve y con qué emisor va a numerar.

    Es lo primero que prueba quien se integra: si esto responde, el resto de la
    API está a un encabezado de distancia.
    """
    return RespuestaPing(
        cliente=cliente["nombre"],
        plan=cliente["plan"],
        emisor=Emisor(
            cod_empresa=cliente["cod_empresa"],
            nombre=cliente.get("empresa_nombre"),
            nit=cliente.get("empresa_nit"),
        ),
    )
