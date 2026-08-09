from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from services.products_service import (get_all_products_detailed, get_product_by_id,
                                        create_product, update_product, delete_product)
from services.inventory_service import ajustar_stock, registrar_saldo_inicial
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
    request: Request,
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
    controla_stock: int = Form(1),
):
    product_id = create_product(sku, nombre, descripcion, precio_unitario, stock, stock_minimo,
                                cod_impuesto, unidad_medida, codigo_barras, activo, controla_stock)
    registrar_saldo_inicial(
        product_id,
        cod_usuario=request.session.get("user", {}).get("cod_usuario"),
        observaciones="Saldo inicial al crear el producto",
    )
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
    request: Request,
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
    controla_stock: int = Form(1),
):
    anterior = get_product_by_id(product_id)
    if not anterior:
        return RedirectResponse(url="/products/product", status_code=302)

    cod_usuario = request.session.get("user", {}).get("cod_usuario")
    ya_controlaba = bool(anterior.get("controla_stock"))

    # Si el producto ya lleva kardex, el stock no se pisa desde el formulario: se
    # conserva el saldo y la diferencia entra como un ajuste trazable.
    stock_a_guardar = anterior["stock"] if (controla_stock and ya_controlaba) else stock

    update_product(product_id, sku, nombre, descripcion, precio_unitario, stock_a_guardar,
                   stock_minimo, cod_impuesto, unidad_medida, codigo_barras, activo,
                   controla_stock)

    if controla_stock and ya_controlaba:
        ajustar_stock(product_id, stock, cod_usuario=cod_usuario,
                      observaciones="Ajuste desde el formulario de producto")
    elif controla_stock and not ya_controlaba:
        registrar_saldo_inicial(product_id, cod_usuario=cod_usuario,
                                observaciones="Saldo de apertura al activar control de inventario")

    return RedirectResponse(url="/products/product", status_code=303)


@router.get("/product/delete/{product_id}", name="delete_product")
def delete_product_get(product_id: int):
    delete_product(product_id)
    return RedirectResponse(url="/products/product", status_code=302)
