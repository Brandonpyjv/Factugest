"""
Aritmética tributaria de un documento electrónico.

Este módulo es deliberadamente puro: no abre conexiones, no lee sesión y no
sabe de dónde vienen las líneas. Esa independencia es lo que permite que la
misma implementación alimente el formulario web —donde los precios y el IVA
salen de nuestra tabla `productos`— y la API de integración, donde el sistema
externo envía sus propios ítems con sus propias tarifas.

Es también el único lugar del proyecto donde vive el prorrateo del IVA sobre el
descuento global, que es la regla más fácil de implementar mal.
"""


def _num(valor, defecto=0.0) -> float:
    try:
        return float(valor)
    except (TypeError, ValueError):
        return defecto


def calcular_linea(linea: dict) -> dict:
    """Calcula una línea y devuelve una copia con los valores derivados.

    Espera `cantidad`, `precio_unitario` y, opcionalmente,
    `descuento_porcentaje` e `impuesto_porcentaje`. Las claves de entrada se
    devuelven tal como llegaron —incluidas las ajenas al cálculo, como
    cod_producto o sku— y solo se agregan las derivadas: quien llama sigue
    viendo los tipos que envió.
    """
    cantidad = _num(linea.get("cantidad"))
    precio = _num(linea.get("precio_unitario"))
    desc_pct = _num(linea.get("descuento_porcentaje"))
    imp_pct = _num(linea.get("impuesto_porcentaje"))

    valor_bruto = precio * cantidad
    descuento_valor = round(valor_bruto * desc_pct / 100, 2)
    base_gravable = valor_bruto - descuento_valor
    impuesto_valor = round(base_gravable * imp_pct / 100, 2)

    return {
        **linea,
        "valor_bruto": valor_bruto,
        "descuento_valor": descuento_valor,
        # `subtotal` es el nombre que usa la columna en detalle_factura.
        "subtotal": base_gravable,
        "impuesto_valor": impuesto_valor,
    }


def calcular_documento(lineas, descuento_global: float = 0.0) -> dict:
    """Calcula las líneas y los totales de un documento.

    `descuento_global` es un valor en pesos, no un porcentaje: es un descuento
    sobre el total de la factura, aparte de los descuentos por línea.

    Devuelve las líneas ya calculadas y los cinco totales que van a la cabecera:
    subtotal_bruto, total_descuentos, subtotal (base gravable neta),
    total_impuestos y total.
    """
    calculadas = [calcular_linea(l) for l in lineas]

    subtotal_bruto = sum(l["valor_bruto"] for l in calculadas)
    total_descuentos = sum(l["descuento_valor"] for l in calculadas)
    total_impuestos = sum(l["impuesto_valor"] for l in calculadas)

    descuento_global = _num(descuento_global)

    # El descuento global también reduce la base gravable, así que el IVA ya
    # calculado por línea queda de más. Se recorta en la misma proporción en
    # que el descuento reduce la base: sin esto la factura cobraría IVA sobre
    # un dinero que el cliente nunca pagó.
    base_neta_lineas = subtotal_bruto - total_descuentos
    if base_neta_lineas > 0 and descuento_global > 0:
        proporcion = descuento_global / base_neta_lineas
        total_impuestos = round(total_impuestos - round(total_impuestos * proporcion, 2), 2)

    total_descuentos = round(total_descuentos + descuento_global, 2)
    subtotal = round(subtotal_bruto - total_descuentos, 2)
    total = round(subtotal + total_impuestos, 2)

    return {
        "lineas": calculadas,
        "subtotal_bruto": round(subtotal_bruto, 2),
        "total_descuentos": total_descuentos,
        "subtotal": subtotal,
        "total_impuestos": round(total_impuestos, 2),
        "total": total,
    }


# ── Notas ───────────────────────────────────────────────────────────────────
#
# Una nota no se calcula de cero: se calcula *sobre* un documento que ya existe.
# Por eso reciben las líneas del original y no una lista nueva — así una
# devolución no puede cobrar un precio distinto del que se facturó.
#
# Los importes salen **positivos**. El signo de una nota lo lleva su tipo: una
# nota crédito de $100 es de $100, y es el hecho de ser NC lo que dice que resta.
# Guardarla en negativo obliga a poner un `abs()` en cada sitio que la muestre y
# deja el XML con cantidades que la DIAN no admite.


def calcular_nota_credito(lineas_originales, devoluciones=None) -> dict:
    """Anulación total, o devolución parcial de unas cantidades.

    `devoluciones` es `{orden_de_la_linea: cantidad}`. Sin él se devuelve todo,
    que es la anulación.

    Lo devuelto se prorratea sobre la línea original: si de tres unidades se
    devuelve una, vuelve un tercio de su base, de su descuento y de su IVA. Sin
    prorratear el descuento, una devolución parcial le regresaría al comprador
    más dinero del que pagó por esa unidad.
    """
    lineas = []

    for orden, original in enumerate(lineas_originales, start=1):
        cantidad_original = _num(original.get("cantidad"))
        if devoluciones is None:
            cantidad = cantidad_original
        else:
            cantidad = _num(devoluciones.get(orden, 0))
        if cantidad <= 0:
            continue

        proporcion = (cantidad / cantidad_original) if cantidad_original else 0
        lineas.append({
            **original,
            "orden": orden,
            "cantidad": cantidad,
            "valor_bruto": round(_num(original.get("valor_bruto")) * proporcion, 2),
            "descuento_valor": round(_num(original.get("descuento_valor")) * proporcion, 2),
            "subtotal": round(_num(original.get("subtotal")) * proporcion, 2),
            "impuesto_valor": round(_num(original.get("impuesto_valor")) * proporcion, 2),
        })

    subtotal_bruto = round(sum(l["valor_bruto"] for l in lineas), 2)
    total_descuentos = round(sum(l["descuento_valor"] for l in lineas), 2)
    subtotal = round(sum(l["subtotal"] for l in lineas), 2)
    total_impuestos = round(sum(l["impuesto_valor"] for l in lineas), 2)

    return {
        "lineas": lineas,
        "subtotal_bruto": subtotal_bruto,
        "total_descuentos": total_descuentos,
        "subtotal": subtotal,
        "total_impuestos": total_impuestos,
        "total": round(subtotal + total_impuestos, 2),
    }


def tasa_promedio(subtotal: float, total_impuestos: float) -> float:
    """Qué porcentaje de IVA llevó un documento, visto en conjunto.

    Una factura puede mezclar líneas al 19 %, al 5 % y exentas. Un ajuste
    posterior —un flete, un interés— no pertenece a ninguna línea en particular,
    así que se le aplica la tarifa que el documento llevó en promedio. Es una
    aproximación, y es la que usa el sistema desde siempre; la alternativa sería
    pedirle al integrador que decida la tarifa del ajuste.
    """
    subtotal = _num(subtotal)
    if subtotal <= 0:
        return 0.0
    return round(_num(total_impuestos) / subtotal * 100, 4)


def calcular_nota_debito(valor: float, porcentaje_impuesto: float,
                         incluye_impuesto: bool = True) -> dict:
    """Un cargo adicional sobre un documento ya emitido.

    `incluye_impuesto` distingue las dos formas de pedirlo: «cóbrale $50.000 más»
    —donde el IVA va adentro y hay que descomponerlo— y «agrégale una base de
    $50.000», donde el IVA se suma encima. Confundirlas cambia lo que paga el
    comprador, así que el que integra tiene que decirlo explícitamente.
    """
    valor = _num(valor)
    tasa = _num(porcentaje_impuesto)

    if incluye_impuesto:
        base = round(valor / (1 + tasa / 100), 2)
        impuesto = round(valor - base, 2)
    else:
        base = round(valor, 2)
        impuesto = round(base * tasa / 100, 2)

    return {
        "lineas": [],
        "subtotal_bruto": base,
        "total_descuentos": 0.0,
        "subtotal": base,
        "total_impuestos": impuesto,
        "total": round(base + impuesto, 2),
        "impuesto_porcentaje": tasa,
    }
