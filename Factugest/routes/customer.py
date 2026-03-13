from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.customer_service import (get_all_customers, get_customer_by_id,
                                        create_customer, update_customer, delete_customer)
from templates_config import templates

router = APIRouter(prefix="/customer")


@router.get("", name="customer")
def customer(request: Request):
    data = get_all_customers()
    return templates.TemplateResponse(request, "customer/index.html", {"all_customers": data})


@router.get("/new", name="new_customer")
def new_customer(request: Request):
    return templates.TemplateResponse(request, "customer/form.html", {"customer": None})


@router.post("/new", name="create_customer")
def create_customer_post(
    full_name: str = Form(...),
    document_type: str = Form(...),
    document_number: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    ciudad: str = Form(""),
    departamento: str = Form(""),
    pais: str = Form("Colombia"),
    tipo_persona: str = Form("NATURAL"),
    regimen_tributario: str = Form("NO_RESPONSABLE_IVA"),
):
    create_customer(full_name, document_type, document_number, phone, email, address,
                    ciudad, departamento, pais, tipo_persona, regimen_tributario)
    return RedirectResponse(url="/customer", status_code=303)


@router.get("/edit/{customer_id}", name="edit_customer")
def edit_customer(request: Request, customer_id: int):
    c = get_customer_by_id(customer_id)
    if not c:
        return RedirectResponse(url="/customer", status_code=302)
    return templates.TemplateResponse(request, "customer/form.html", {"customer": c})


@router.post("/edit/{customer_id}", name="update_customer")
def update_customer_post(
    customer_id: int,
    full_name: str = Form(...),
    document_type: str = Form(...),
    document_number: str = Form(...),
    phone: str = Form(""),
    email: str = Form(""),
    address: str = Form(""),
    ciudad: str = Form(""),
    departamento: str = Form(""),
    pais: str = Form("Colombia"),
    tipo_persona: str = Form("NATURAL"),
    regimen_tributario: str = Form("NO_RESPONSABLE_IVA"),
):
    update_customer(customer_id, full_name, document_type, document_number, phone, email,
                    address, ciudad, departamento, pais, tipo_persona, regimen_tributario)
    return RedirectResponse(url="/customer", status_code=303)


@router.get("/delete/{customer_id}", name="delete_customer")
def delete_customer_get(customer_id: int):
    delete_customer(customer_id)
    return RedirectResponse(url="/customer", status_code=302)
