from fastapi import APIRouter, Request
from services.discounts import get_all_discount
from templates_config import templates

router = APIRouter()


@router.get("/discount", name="discount")
def discount(request: Request):
    data = get_all_discount()
    return templates.TemplateResponse(request, "discount/index.html", {"all_discount": data})


@router.get("/new_discount", name="new_discount")
def new_discount(request: Request):
    return templates.TemplateResponse(request, "discount/form.html")
