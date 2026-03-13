from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse, Response
from typing import List, Optional
from services.invoice_service import (get_all_invoices_detailed, get_invoice_by_id,
                                       get_invoice_details, create_invoice,
                                       create_invoice_detail, update_invoice_status, delete_invoice)
from services.customer_service import get_all_customers
from services.branches import get_all_branches
from services.payment_methods_service import get_all_payment_methods
from services.invoice_payments_service import get_all_invoice_payments
from services.products_service import get_all_products_detailed
from services.taxes import get_all_invoice_taxes
from services.pdf_service import generate_invoice_pdf
from templates_config import templates
from database import get_one

router = APIRouter(prefix="/invoice")


@router.get("", name="invoice")
def invoice(request: Request):
    data = get_all_invoices_detailed()
    return templates.TemplateResponse(request, "invoice/index.html", {"all_invoices": data})


@router.get("/new", name="new_invoice")
def new_invoice(request: Request):
    return templates.TemplateResponse(request, "invoice/form.html", {
        "customers": get_all_customers(),
        "empresas": get_all_branches(),
        "metodos_pago": get_all_payment_methods(),
        "pagos_factura": get_all_invoice_payments(),
        "productos": get_all_products_detailed(),
        "invoice": None,
    })


@router.post("/new", name="create_invoice")
async def create_invoice_post(
    request: Request,
    cod_cliente: int = Form(...),
    cod_empresa: int = Form(...),
    fecha: str = Form(...),
    fecha_vencimiento: str = Form(""),
    cod_metodo_pago: int = Form(...),
    cod_pago: int = Form(...),
    tipo_factura: str = Form("FV"),
    observaciones: str = Form(""),
    cod_producto: List[int] = Form(...),
    precio_unitario: List[float] = Form(...),
    cantidad: List[int] = Form(...),
    descuento_porcentaje: List[float] = Form(None),
):
    # Calcular totales con impuestos por producto
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
        tax_pct = float(prod['tax_pct'] or 0) if prod else 0
        precio = float(precio_unitario[i])
        cant = int(cantidad[i])
        desc_pct = float(desc_list[i] if i < len(desc_list) else 0) or 0.0

        valor_bruto = precio * cant
        desc_valor = round(valor_bruto * desc_pct / 100, 2)
        base_imponible = valor_bruto - desc_valor
        imp_valor = round(base_imponible * tax_pct / 100, 2)
        sub = base_imponible

        subtotal_bruto += valor_bruto
        total_descuentos += desc_valor
        total_impuestos += imp_valor

        lineas.append({
            'cod_producto': cod_producto[i],
            'cantidad': cant,
            'precio_unitario': precio,
            'subtotal': sub,
            'descuento_porcentaje': desc_pct,
            'descuento_valor': desc_valor,
            'impuesto_porcentaje': tax_pct,
            'impuesto_valor': imp_valor,
        })

    total = round(subtotal_bruto - total_descuentos + total_impuestos, 2)
    subtotal_neto = round(subtotal_bruto - total_descuentos, 2)

    invoice_id = create_invoice(
        cod_cliente=cod_cliente, cod_usuario=1, cod_empresa=cod_empresa,
        cod_metodo_pago=cod_metodo_pago, cod_pago=cod_pago, fecha=fecha,
        total=total, subtotal=subtotal_neto,
        total_descuentos=round(total_descuentos, 2),
        total_impuestos=round(total_impuestos, 2),
        tipo_factura=tipo_factura,
        observaciones=observaciones,
        fecha_vencimiento=fecha_vencimiento or None
    )

    for l in lineas:
        create_invoice_detail(
            cod_factura=invoice_id,
            cod_producto=l['cod_producto'],
            cantidad=l['cantidad'],
            precio_unitario=l['precio_unitario'],
            subtotal=l['subtotal'],
            descuento_porcentaje=l['descuento_porcentaje'],
            descuento_valor=l['descuento_valor'],
            impuesto_porcentaje=l['impuesto_porcentaje'],
            impuesto_valor=l['impuesto_valor'],
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
        headers={"Content-Disposition": f'inline; filename="factura_{invoice_id}.pdf"'}
    )


@router.get("/delete/{invoice_id}", name="delete_invoice")
def delete_invoice_get(invoice_id: int):
    delete_invoice(invoice_id)
    return RedirectResponse(url="/invoice", status_code=302)
