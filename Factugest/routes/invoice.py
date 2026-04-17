from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, Response, JSONResponse
from typing import List, Optional
from datetime import datetime, date as date_type
from services.invoice_service import (get_all_invoices_detailed, get_invoice_by_id,
                                       get_invoice_details, create_invoice,
                                       create_invoice_detail, update_invoice_status, delete_invoice)
from services.branches import get_all_branches
from services.payment_methods_service import get_all_payment_methods
from services.invoice_payments_service import get_all_invoice_payments
from services.pdf_service import generate_invoice_pdf
from services.user_service import get_user_by_id
from templates_config import templates
from database import get_one, get_many

router = APIRouter(prefix="/invoice")


@router.get("", name="invoice")
def invoice(request: Request):
    data = get_all_invoices_detailed()
    return templates.TemplateResponse(request, "invoice/index.html", {"all_invoices": data})


@router.get("/new", name="new_invoice")
def new_invoice(request: Request):
    session_user = request.session.get("user", {})
    cod_empresa = session_user.get("cod_empresa")

    # Si la sesión es antigua y no trae cod_empresa, consultarlo de la BD
    if not cod_empresa:
        cod_usuario = session_user.get("cod_usuario")
        if cod_usuario:
            db_user = get_user_by_id(cod_usuario)
            if db_user:
                cod_empresa = db_user.get("cod_empresa")
                request.session["user"]["cod_empresa"] = cod_empresa
                request.session["user"]["empresa_nombre"] = db_user.get("empresa_nombre")

    empresa = get_one(
        "SELECT cod_empresa, nombre, nit, dv FROM empresas WHERE cod_empresa = %s",
        (cod_empresa,)
    ) if cod_empresa else None
    invoice_discounts = get_many(
        "SELECT cod_descuento, descripcion, porcentaje FROM descuentos "
        "WHERE aplica_a_factura = 1 ORDER BY descripcion"
    )
    return templates.TemplateResponse(request, "invoice/form.html", {
        "empresa": empresa,
        "metodos_pago": get_all_payment_methods(),
        "pagos_factura": get_all_invoice_payments(),
        "invoice_discounts": invoice_discounts,
        "invoice": None,
    })


@router.post("/new", name="create_invoice")
async def create_invoice_post(
    request: Request,
    cod_cliente: int = Form(...),
    cod_metodo_pago: int = Form(...),
    cod_pago: int = Form(...),
    tipo_factura: str = Form("FV"),
    observaciones: str = Form(""),
    cod_producto: List[int] = Form(...),
    precio_unitario: List[float] = Form(...),
    cantidad: List[int] = Form(...),
    descuento_porcentaje: List[float] = Form(None),
    valor_descuento_factura: float = Form(0.0),
):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fecha_vencimiento = date_type.today().strftime("%Y-%m-%d")

    subtotal_bruto = 0.0
    total_descuentos = 0.0
    total_impuestos = 0.0
    lineas = []

    desc_list = descuento_porcentaje if descuento_porcentaje else [0.0] * len(cod_producto)

    for i in range(len(cod_producto)):
        prod = get_one(
            "SELECT p.precio_unitario, i.porcentaje AS tax_pct FROM productos p "
            "LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto WHERE p.cod_producto = %s",
            (cod_producto[i],)
        )
        tax_pct = float(prod["tax_pct"] or 0) if prod else 0
        precio = float(precio_unitario[i])
        cant = int(cantidad[i])
        desc_pct = float(desc_list[i] if i < len(desc_list) else 0) or 0.0

        valor_bruto = precio * cant
        desc_valor = round(valor_bruto * desc_pct / 100, 2)
        base_imponible = valor_bruto - desc_valor
        imp_valor = round(base_imponible * tax_pct / 100, 2)

        subtotal_bruto += valor_bruto
        total_descuentos += desc_valor
        total_impuestos += imp_valor

        lineas.append({
            "cod_producto":         cod_producto[i],
            "cantidad":             cant,
            "precio_unitario":      precio,
            "subtotal":             base_imponible,
            "descuento_porcentaje": desc_pct,
            "descuento_valor":      desc_valor,
            "impuesto_porcentaje":  tax_pct,
            "impuesto_valor":       imp_valor,
        })

    total_descuentos = round(total_descuentos + valor_descuento_factura, 2)
    total = round(subtotal_bruto - total_descuentos + total_impuestos, 2)
    subtotal_neto = round(subtotal_bruto - total_descuentos, 2)

    session_user = request.session.get("user", {})
    cod_usuario = session_user.get("cod_usuario", 1)
    cod_empresa = session_user.get("cod_empresa", 1)

    invoice_id = create_invoice(
        cod_cliente=cod_cliente, cod_usuario=cod_usuario, cod_empresa=cod_empresa,
        cod_metodo_pago=cod_metodo_pago, cod_pago=cod_pago, fecha=fecha,
        total=total, subtotal=subtotal_neto,
        total_descuentos=round(total_descuentos, 2),
        total_impuestos=round(total_impuestos, 2),
        tipo_factura=tipo_factura,
        observaciones=observaciones,
        fecha_vencimiento=fecha_vencimiento or None,
    )

    for linea in lineas:
        create_invoice_detail(
            cod_factura=invoice_id,
            cod_producto=linea["cod_producto"],
            cantidad=linea["cantidad"],
            precio_unitario=linea["precio_unitario"],
            subtotal=linea["subtotal"],
            descuento_porcentaje=linea["descuento_porcentaje"],
            descuento_valor=linea["descuento_valor"],
            impuesto_porcentaje=linea["impuesto_porcentaje"],
            impuesto_valor=linea["impuesto_valor"],
        )

    return RedirectResponse(url=f"/invoice/{invoice_id}", status_code=303)


@router.get("/{invoice_id}", name="view_invoice")
def view_invoice(request: Request, invoice_id: int):
    inv = get_invoice_by_id(invoice_id)
    if not inv:
        return RedirectResponse(url="/invoice", status_code=302)
    details = get_invoice_details(invoice_id)
    pagos = get_all_invoice_payments()
    return templates.TemplateResponse(request, "invoice/view.html", {
        "invoice": inv,
        "details": details,
        "pagos_factura": pagos,
    })


@router.post("/{invoice_id}/status", name="update_invoice_status")
def update_status_post(invoice_id: int, cod_pago: int = Form(...)):
    update_invoice_status(invoice_id, cod_pago)
    return RedirectResponse(url=f"/invoice/{invoice_id}", status_code=303)


@router.get("/{invoice_id}/pdf", name="invoice_pdf")
def invoice_pdf(invoice_id: int):
    inv = get_invoice_by_id(invoice_id)
    if not inv:
        return RedirectResponse(url="/invoice", status_code=302)
    details = get_invoice_details(invoice_id)
    pdf_bytes = generate_invoice_pdf(inv, details)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="factura_{invoice_id}.pdf"'},
    )


@router.get("/delete/{invoice_id}", name="delete_invoice")
def delete_invoice_get(invoice_id: int):
    delete_invoice(invoice_id)
    return RedirectResponse(url="/invoice", status_code=302)


# ── Endpoints AJAX para el formulario de nueva factura ──────────────────────

@router.get("/api/customers/search", name="api_customers_search")
def api_customers_search(q: str = ""):
    results = get_many(
        "SELECT customer_id, full_name, document_number, document_type FROM customers "
        "WHERE full_name LIKE %s OR document_number LIKE %s ORDER BY full_name LIMIT 10",
        (f"%{q}%", f"%{q}%"),
    )
    return JSONResponse(content=results)


@router.get("/api/products/search", name="api_products_search")
def api_products_search(q: str = ""):
    results = get_many(
        "SELECT p.cod_producto, p.sku, p.nombre, p.precio_unitario, "
        "i.porcentaje AS tax_porcentaje "
        "FROM productos p LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto "
        "WHERE p.activo = 1 AND (p.sku LIKE %s OR p.nombre LIKE %s) "
        "ORDER BY p.nombre LIMIT 10",
        (f"%{q}%", f"%{q}%"),
    )
    for r in results:
        r["precio_unitario"] = float(r["precio_unitario"])
        r["tax_porcentaje"] = float(r["tax_porcentaje"] or 0)
    return JSONResponse(content=results)


@router.get("/api/products/{product_id}/discounts", name="api_product_discounts")
def api_product_discounts(product_id: int):
    results = get_many(
        "SELECT d.cod_descuento, d.descripcion, d.porcentaje "
        "FROM descuentos d "
        "JOIN producto_descuento pd ON d.cod_descuento = pd.cod_descuento "
        "WHERE pd.cod_producto = %s",
        (product_id,),
    )
    return JSONResponse(content=results)


@router.get("/api/discounts", name="api_invoice_discounts")
def api_invoice_discounts():
    results = get_many(
        "SELECT cod_descuento, descripcion, porcentaje FROM descuentos "
        "WHERE aplica_a_factura = 1 ORDER BY descripcion"
    )
    return JSONResponse(content=results)
