from fastapi import APIRouter, Request
from services.payment_methods_service import get_all_payment_methods
from templates_config import templates

router = APIRouter()


@router.get("/payment_methods", name="payment_methods")
def payment_methods(request: Request):
    data = get_all_payment_methods()
    return templates.TemplateResponse(request, "payment_methods/index.html", {"all_payment_methods": data})


@router.get("/payment_methods/new", name="payment_methods_new")
def payment_methods_new(request: Request):
    return templates.TemplateResponse(request, "payment_methods/form.html")
