import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT


def generate_invoice_pdf(invoice: dict, details: list) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=1.5 * cm, leftMargin=1.5 * cm,
                            topMargin=1.5 * cm, bottomMargin=1.5 * cm)

    styles = getSampleStyleSheet()
    primary = colors.HexColor('#4e73df')
    dark = colors.HexColor('#2d3748')
    light_gray = colors.HexColor('#f8f9fc')
    mid_gray = colors.HexColor('#e3e6f0')

    style_title = ParagraphStyle('title', parent=styles['Normal'], fontSize=22, textColor=primary,
                                  fontName='Helvetica-Bold', spaceAfter=2)
    style_subtitle = ParagraphStyle('subtitle', parent=styles['Normal'], fontSize=9, textColor=colors.gray,
                                     fontName='Helvetica')
    style_header = ParagraphStyle('header', parent=styles['Normal'], fontSize=8, textColor=colors.white,
                                   fontName='Helvetica-Bold')
    style_normal = ParagraphStyle('normal', parent=styles['Normal'], fontSize=8, textColor=dark,
                                   fontName='Helvetica', leading=12)
    style_bold = ParagraphStyle('bold', parent=styles['Normal'], fontSize=8, textColor=dark,
                                 fontName='Helvetica-Bold')
    style_right = ParagraphStyle('right', parent=styles['Normal'], fontSize=9, alignment=TA_RIGHT,
                                  fontName='Helvetica-Bold', textColor=dark)
    style_total = ParagraphStyle('total', parent=styles['Normal'], fontSize=13, alignment=TA_RIGHT,
                                  fontName='Helvetica-Bold', textColor=primary)

    story = []

    # ─── ENCABEZADO ─────────────────────────────────────────────────────────────
    empresa_nombre = invoice.get('empresa_nombre', 'Factugest')
    empresa_nit = invoice.get('empresa_nit', '')
    empresa_dv = invoice.get('empresa_dv', '')
    nit_str = f"NIT: {empresa_nit}{('-' + empresa_dv) if empresa_dv else ''}"
    empresa_dir = invoice.get('empresa_direccion', '')
    empresa_ciudad = invoice.get('empresa_ciudad', '')
    empresa_tel = invoice.get('empresa_telefono', '')
    empresa_correo = invoice.get('empresa_correo', '')
    empresa_regimen = (invoice.get('empresa_regimen') or '').replace('_', ' ').title()

    tipo_factura = invoice.get('tipo_factura', 'FV')
    tipo_map = {'FV': 'FACTURA ELECTRÓNICA DE VENTA', 'NC': 'NOTA CRÉDITO ELECTRÓNICA', 'ND': 'NOTA DÉBITO ELECTRÓNICA'}
    tipo_label = tipo_map.get(tipo_factura, 'FACTURA ELECTRÓNICA')

    fecha_val = invoice.get('fecha', '')
    fecha_str = fecha_val.strftime('%d/%m/%Y %H:%M') if hasattr(fecha_val, 'strftime') else str(fecha_val)
    vencimiento = invoice.get('fecha_vencimiento')
    venc_str = vencimiento.strftime('%d/%m/%Y') if hasattr(vencimiento, 'strftime') else (str(vencimiento) if vencimiento else '')

    header_data = [
        [Paragraph(empresa_nombre, style_title),
         Paragraph(f'<b>{tipo_label}</b>', ParagraphStyle('inv', parent=styles['Normal'],
                                                           fontSize=13, textColor=primary,
                                                           fontName='Helvetica-Bold', alignment=TA_RIGHT))],
        [Paragraph(nit_str, style_subtitle),
         Paragraph(f'N° <b>{invoice.get("cod_factura", "")}</b>',
                   ParagraphStyle('no', parent=styles['Normal'], fontSize=10,
                                   fontName='Helvetica-Bold', alignment=TA_RIGHT, textColor=dark))],
        [Paragraph(f'{empresa_dir} · {empresa_ciudad}', style_subtitle),
         Paragraph(f'Fecha: {fecha_str}',
                   ParagraphStyle('fecha', parent=styles['Normal'], fontSize=8,
                                   fontName='Helvetica', alignment=TA_RIGHT, textColor=colors.gray))],
        [Paragraph(f'Tel: {empresa_tel} · {empresa_correo}', style_subtitle),
         Paragraph(f'Vence: {venc_str}' if venc_str else '',
                   ParagraphStyle('venc', parent=styles['Normal'], fontSize=8,
                                   fontName='Helvetica', alignment=TA_RIGHT, textColor=colors.gray))],
        [Paragraph(empresa_regimen, style_subtitle), ''],
    ]

    header_table = Table(header_data, colWidths=[10 * cm, 8.5 * cm])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
        ('TOPPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(header_table)
    story.append(HRFlowable(width='100%', thickness=2, color=primary, spaceAfter=8))

    # ─── DATOS CLIENTE / PAGO ───────────────────────────────────────────────────
    estado_map = {
        'paid': ('Pagado', colors.HexColor('#1cc88a')),
        'pending': ('Pendiente', colors.HexColor('#f6c23e')),
        'partially paid': ('Pago Parcial', colors.HexColor('#36b9cc')),
        'overdue': ('Vencido', colors.HexColor('#e74a3b')),
        'cancelled': ('Cancelado', colors.HexColor('#858796')),
        'disputed': ('En Disputa', colors.HexColor('#5a5c69')),
        'refunded': ('Reembolsado', colors.HexColor('#4e73df')),
    }
    estado_raw = (invoice.get('estado_pago') or '').lower()
    estado_label, estado_color = estado_map.get(estado_raw, (estado_raw.capitalize(), colors.gray))

    cliente_regimen = (invoice.get('cliente_regimen') or '').replace('_', ' ').title()

    info_data = [
        [Paragraph('<b>FACTURADO A</b>', ParagraphStyle('sec', parent=styles['Normal'], fontSize=7,
                                                          textColor=primary, fontName='Helvetica-Bold')),
         Paragraph('<b>INFORMACIÓN DE PAGO</b>', ParagraphStyle('sec', parent=styles['Normal'], fontSize=7,
                                                                  textColor=primary, fontName='Helvetica-Bold'))],
        [Paragraph(invoice.get('cliente_nombre', ''), style_bold),
         Paragraph(f'Método: {invoice.get("metodo_pago_nombre", "")}', style_normal)],
        [Paragraph(f'{invoice.get("document_type", "")} {invoice.get("document_number", "")}', style_normal),
         Paragraph(f'Estado: <b>{estado_label}</b>', style_bold)],
        [Paragraph(cliente_regimen, style_normal),
         Paragraph(f'Cajero: {invoice.get("usuario_nombre", "")}', style_normal)],
        [Paragraph(invoice.get('cliente_email', '') or '', style_normal), ''],
        [Paragraph(invoice.get('cliente_address', '') or '', style_normal), ''],
    ]

    info_table = Table(info_data, colWidths=[9.25 * cm, 9.25 * cm])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), light_gray),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 0.5, mid_gray),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 12))

    # ─── TABLA DE PRODUCTOS ─────────────────────────────────────────────────────
    style_header_sm = ParagraphStyle('header_sm', parent=styles['Normal'], fontSize=7, textColor=colors.white,
                                      fontName='Helvetica-Bold')
    style_normal_sm = ParagraphStyle('normal_sm', parent=styles['Normal'], fontSize=7.5, textColor=dark,
                                      fontName='Helvetica', leading=11)
    style_right_sm = ParagraphStyle('right_sm', parent=styles['Normal'], fontSize=7.5, alignment=TA_RIGHT,
                                     fontName='Helvetica', textColor=dark)

    col_headers = [
        Paragraph('PRODUCTO / SERVICIO', style_header_sm),
        Paragraph('SKU', style_header_sm),
        Paragraph('CANT.', style_header_sm),
        Paragraph('P. UNIT.', style_header_sm),
        Paragraph('DESC %', style_header_sm),
        Paragraph('BASE GRAV.', style_header_sm),
        Paragraph('IVA', style_header_sm),
    ]
    rows = [col_headers]

    for d in details:
        sub = float(d.get('subtotal', 0))
        desc_pct = float(d.get('descuento_porcentaje', 0))
        imp_pct = float(d.get('impuesto_porcentaje', 0))
        imp_val = float(d.get('impuesto_valor', 0))
        imp_str = f"${imp_val:,.2f}\n({imp_pct:.0f}%)" if imp_val else "Exento"
        desc_str = f"{desc_pct:.2f}%" if desc_pct else "—"
        rows.append([
            Paragraph(str(d.get('producto_nombre', '')), style_normal_sm),
            Paragraph(str(d.get('sku', '')), style_normal_sm),
            Paragraph(str(d.get('cantidad', '')), style_right_sm),
            Paragraph(f"${float(d.get('precio_unitario', 0)):,.2f}", style_right_sm),
            Paragraph(desc_str, style_right_sm),
            Paragraph(f"${sub:,.2f}", style_right_sm),
            Paragraph(imp_str, style_right_sm),
        ])

    col_widths = [5.8 * cm, 2 * cm, 1.3 * cm, 2.5 * cm, 1.5 * cm, 2.5 * cm, 2.9 * cm]
    prod_table = Table(rows, colWidths=col_widths, repeatRows=1)
    prod_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, light_gray]),
        ('GRID', (0, 0), (-1, -1), 0.3, mid_gray),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(prod_table)
    story.append(Spacer(1, 10))

    # ─── TOTALES DIAN ────────────────────────────────────────────────────────────
    total = float(invoice.get('total', 0))
    subtotal_neto = float(invoice.get('subtotal', 0))
    total_desc = float(invoice.get('total_descuentos', 0))
    total_imp = float(invoice.get('total_impuestos', 0))
    subtotal_bruto = subtotal_neto + total_desc

    totals_data = [
        ['', Paragraph('Subtotal bruto:', style_right), Paragraph(f'${subtotal_bruto:,.2f}', style_right)],
        ['', Paragraph('(-) Descuentos:', style_right), Paragraph(f'${total_desc:,.2f}', style_right)],
        ['', Paragraph('Base gravable:', style_right), Paragraph(f'${subtotal_neto:,.2f}', style_right)],
        ['', Paragraph('(+) Impuestos:', style_right), Paragraph(f'${total_imp:,.2f}', style_right)],
        ['', Paragraph('<b>TOTAL A PAGAR:</b>', style_total), Paragraph(f'<b>${total:,.2f}</b>', style_total)],
    ]
    totals_table = Table(totals_data, colWidths=[10 * cm, 4 * cm, 4.5 * cm])
    totals_table.setStyle(TableStyle([
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LINEABOVE', (1, 4), (-1, 4), 1.5, primary),
        ('BACKGROUND', (1, 4), (-1, 4), light_gray),
    ]))
    story.append(totals_table)

    # ─── OBSERVACIONES ──────────────────────────────────────────────────────────
    obs = invoice.get('observaciones')
    if obs:
        story.append(Spacer(1, 8))
        story.append(Paragraph(
            f'<b>Observaciones:</b> {obs}',
            ParagraphStyle('obs', parent=styles['Normal'], fontSize=8, textColor=dark, fontName='Helvetica')
        ))

    # ─── PIE ────────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width='100%', thickness=0.5, color=mid_gray))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        'Documento generado electrónicamente por <b>Factugest</b> · Este documento es válido como soporte de pago.',
        ParagraphStyle('footer', parent=styles['Normal'], fontSize=7,
                        textColor=colors.gray, alignment=TA_CENTER)
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.read()
