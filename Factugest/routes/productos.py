from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.products_service import (get_all_products_detailed, get_product_by_id,
                                        create_product, update_product, delete_product)
from services.taxes import get_all_invoice_taxes
from templates_config import templates

router = APIRouter(prefix="/products")


@router.get("/product", name="product")
def products(request: Request):
    data = get_all_products_detailed()
    return templates.TemplateResponse(request, "product/index.html", {"products": data})


@router.get("/product/new", name="product_new")
def product_new(request: Request):
    taxes = get_all_invoice_taxes()
    return templates.TemplateResponse(request, "product/form.html", {"product": None, "taxes": taxes})


@router.post("/product/new", name="create_product")
def create_product_post(
    sku: str = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(""),
    precio_unitario: float = Form(...),
    stock: int = Form(0),
    stock_minimo: int = Form(5),
    cod_impuesto: int = Form(1),
    unidad_medida: str = Form("C62"),
    codigo_barras: str = Form(""),
    activo: int = Form(1),
):
    create_product(sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
                   cod_impuesto, unidad_medida, codigo_barras, activo)
    return RedirectResponse(url="/products/product", status_code=303)


@router.get("/product/edit/{product_id}", name="edit_product")
def edit_product(request: Request, product_id: int):
    product = get_product_by_id(product_id)
    taxes = get_all_invoice_taxes()
    if not product:
        return RedirectResponse(url="/products/product", status_code=302)
    return templates.TemplateResponse(request, "product/form.html", {"product": product, "taxes": taxes})


@router.post("/product/edit/{product_id}", name="update_product")
def update_product_post(
    product_id: int,
    sku: str = Form(...),
    nombre: str = Form(...),
    descripcion: str = Form(""),
    precio_unitario: float = Form(...),
    stock: int = Form(0),
    stock_minimo: int = Form(5),
    cod_impuesto: int = Form(1),
    unidad_medida: str = Form("C62"),
    codigo_barras: str = Form(""),
    activo: int = Form(1),
):
    update_product(product_id, sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
                   cod_impuesto, unidad_medida, codigo_barras, activo)
    return RedirectResponse(url="/products/product", status_code=303)


@router.get("/product/delete/{product_id}", name="delete_product")
def delete_product_get(product_id: int):
    delete_product(product_id)
    return RedirectResponse(url="/products/product", status_code=302)
