from fastapi import APIRouter, Request
from services.customer_service import get_all_customers
from templates_config import templates

router = APIRouter()


@router.get("/customer", name="customer")
def customer(request: Request):
    data = get_all_customers()
    return templates.TemplateResponse(request, "customer/index.html", {"all_customers": data})


@router.get("/new_customer", name="new_customer")
def new_customer(request: Request):
    return templates.TemplateResponse(request, "customer/form.html")
