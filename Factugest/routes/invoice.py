from fastapi import APIRouter, Request
from services.invoice_service import get_all_invoices_detailed
from templates_config import templates

router = APIRouter()


@router.get("/invoice", name="invoice")
def invoice(request: Request):
    data = get_all_invoices_detailed()
    return templates.TemplateResponse(request, "invoice/index.html", {"all_invoices": data})


@router.get("/new_invoice", name="new_invoice")
def new_invoice(request: Request):
    return templates.TemplateResponse(request, "invoice/form.html")
