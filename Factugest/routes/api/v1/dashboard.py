from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from services.invoice_service import get_dashboard_stats
from routes.api.v1.auth import get_current_user

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard (mobile)"])


class RecentInvoiceItem(BaseModel):
    cod_factura: int
    numero_factura: str | None = None
    fecha: datetime
    total: float
    tipo_factura: str | None = None
    cliente: str | None = None
    estado_pago: str | None = None


class DashboardStatsResponse(BaseModel):
    total_facturas: int
    ingresos_cobrados: float
    total_clientes: int
    productos_activos: int
    facturas_pendientes: float
    productos_bajo_stock: int
    facturas_recientes: list[RecentInvoiceItem]


@router.get("/stats", response_model=DashboardStatsResponse)
def dashboard_stats(user: dict = Depends(get_current_user)):
    return get_dashboard_stats()
