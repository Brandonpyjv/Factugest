from fastapi import APIRouter, Request
from services.products_service import get_all_products_detailed
from templates_config import templates

router = APIRouter(prefix="/products")


@router.get("/product", name="product")
def products(request: Request):
    data = get_all_products_detailed()
    return templates.TemplateResponse(request, "product/index.html", {"products": data})


@router.get("/product/new", name="product_new")
def product_new(request: Request):
    return templates.TemplateResponse(request, "product/form.html")
