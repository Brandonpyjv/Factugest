from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.invoice_payments_service import (get_all_invoice_payments, get_invoice_payment_by_id,
                                                create_invoice_payment, update_invoice_payment, delete_invoice_payment)
from templates_config import templates

router = APIRouter(prefix="/invoice_payments")


@router.get("", name="invoice_payments")
def invoice_payments(request: Request):
    data = get_all_invoice_payments()
    return templates.TemplateResponse(request, "invoice_payments/index.html", {"all_invoices": data})


@router.get("/new", name="invoice_payments_new")
def new_invoice_payment(request: Request):
    return templates.TemplateResponse(request, "invoice_payments/form.html", {"payment": None})


@router.post("/new", name="create_invoice_payment")
def create_invoice_payment_post(status: str = Form(...)):
    create_invoice_payment(status)
    return RedirectResponse(url="/invoice_payments", status_code=303)


@router.get("/edit/{payment_id}", name="edit_invoice_payment")
def edit_invoice_payment(request: Request, payment_id: int):
    payment = get_invoice_payment_by_id(payment_id)
    if not payment:
        return RedirectResponse(url="/invoice_payments", status_code=302)
    return templates.TemplateResponse(request, "invoice_payments/form.html", {"payment": payment})


@router.post("/edit/{payment_id}", name="update_invoice_payment")
def update_invoice_payment_post(payment_id: int, status: str = Form(...)):
    update_invoice_payment(payment_id, status)
    return RedirectResponse(url="/invoice_payments", status_code=303)


@router.get("/delete/{payment_id}", name="delete_invoice_payment")
def delete_invoice_payment_get(payment_id: int):
    delete_invoice_payment(payment_id)
    return RedirectResponse(url="/invoice_payments", status_code=302)
