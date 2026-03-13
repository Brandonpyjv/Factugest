from fastapi import APIRouter, Request
from services.invoice_payments_service import get_all_invoice_payments
from templates_config import templates

router = APIRouter()


@router.get("/invoice_payments", name="invoice_payments")
def invoice_payments(request: Request):
    data = get_all_invoice_payments()
    return templates.TemplateResponse(request, "invoice_payments/index.html", {"all_invoices": data})


@router.get("/invoice_payments/new", name="invoice_payments_new")
def invoice_payments_new(request: Request):
    return templates.TemplateResponse(request, "invoice_payments/form.html")
