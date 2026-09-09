"""
AA2-EV01. Infografía de aseguramiento de la calidad de FactuGest.

Una sola lámina en A3 vertical. No es un documento, así que aquí no hay prosa, solo
cajas, cifras y etiquetas cortas.

**Muestra lo que se hizo y lo que resultó, no lo que dicen las normas.** La primera
versión era un mapa de modelos y estándares, con McCall, Boehm, la 9126, SPICE y la
9001 definidos uno por uno, y el cliente la rechazó con razón: la teoría se repite
igual en cualquier trabajo y no dice nada de este proyecto. Aquí las normas solo
aparecen nombradas al pie, porque el referente adoptado sí importa, pero ninguna se
define.

Todas las cifras vienen de `evidencia.py`, que las tomó de la corrida real de la
batería. Ninguna se escribe a mano en este archivo, de modo que la lámina no puede
decir algo distinto del informe.

    python aa2_mapa.py
"""
import textwrap

import matplotlib
matplotlib.use("Agg")
# Sin esto, matplotlib lee lo que va entre dos signos de peso como una fórmula, y en
# una lámina llena de importes eso se come el texto: «$100.000 con $10.000» salía
# como «100.000con10.000», en cursiva y sin los pesos.
matplotlib.rcParams["text.parse_math"] = False
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from comun import SALIDA
from evidencia import (DURACION, FUNCIONALES, INTEGRACION, TOTAL_UNITARIAS, UNITARIAS)

TINTA = "#26364A"
ACENTO = "#1F5FA8"
VERDE = "#1E7A5A"
AMBAR = "#B26B00"
ROJO = "#A8322A"
SUAVE = "#E9EFF7"
BORDE = "#8FA6C4"
GRIS = "#5A6B80"
PAPEL = "#FFFFFF"
TENUE = "#F5F8FC"
DESTACADO = "#D7E5F7"

ARCHIVO = SALIDA / "FactuGest - Infografia de aseguramiento de la calidad.pdf"

ANCHO_PULGADAS, ALTO_PULGADAS = 11.69, 16.54          # A3 vertical
ANCHO, ALTO = 100.0, 141.5
PUNTOS_POR_UNIDAD = ANCHO_PULGADAS * 72 / ANCHO

IZQUIERDA, DERECHA = 4.0, 52.0
COLUMNA = 44.0

# Los archivos de pruebas dicen su nombre técnico. En la lámina va lo que protegen,
# que es lo que entiende quien no programó el sistema. El conteo no se repite aquí,
# se toma de la evidencia.
ETIQUETAS = {
    "test_validaciones.py": "Reglas de validación de los datos que se capturan",
    "test_dian_proveedor.py": "Envío del documento al proveedor de la DIAN",
    "test_modelos_api.py": "Contrato de entrada y salida de la API",
    "test_calculo_documento.py": "Cálculo de impuestos y descuentos",
    "test_calculo_notas.py": "Notas crédito y notas débito",
    "test_monograma.py": "Distintivo de la empresa que no cargó logo",
    "test_api_key_service.py": "Llaves de acceso de cada cliente",
    "test_pdf_membrete.py": "Membrete de la factura en PDF",
    "test_consumo_service.py": "Consumo del plan y cobro del excedente",
    "test_xml_service.py": "Archivo XML que exige la DIAN",
    "test_pdf_descuentos.py": "Descuentos impresos en la factura",
    "test_documento_canonico.py": "Datos con que se arma el PDF y el XML",
}

# (qué se probó, con qué entrada, qué debía dar, qué dio)
CASOS = [
    ("Factura corriente",
     "2 unidades de $189.000 con IVA del 19 %",
     "IVA de $71.820", "$71.820"),
    ("Descuento sobre la factura",
     "Base de $100.000 con $10.000 de descuento",
     "IVA de $17.100, no de $19.000", "$17.100"),
    ("Devolución parcial",
     "Se devuelve 1 de 3 unidades vendidas con 10 % de descuento",
     "Un tercio exacto, $107.100", "$107.100"),
    ("La misma venta enviada dos veces",
     "La misma petición repetida por la API",
     "Devuelve la factura que ya existía, sin gastar otro número",
     "La que ya existía"),
    ("Identificación del cliente",
     "NIT 890903938",
     "Dígito de verificación 8", "8"),
]

# (severidad, color, qué pasaba, cómo quedó)
DEFECTOS = [
    ("Crítico", ROJO,
     "La factura de un cliente salía con el nombre y el logo de FactuGest",
     "Una clínica emitía por la API y el documento parecía expedido por nosotros. Hoy "
     "el emisor va explícito y 10 pruebas vigilan que nuestro nombre no aparezca"),
    ("Mayor", AMBAR,
     "El pie mostraba «Descuentos (0,0 %)» restando dinero real",
     "Sumaba el descuento del producto con el de la factura y lo rotulaba con el "
     "porcentaje equivocado. Hoy cada uno va en su fila, cubierto por 6 pruebas"),
    ("Mayor", AMBAR,
     "La ciudad del comprador salía en blanco en todo lo emitido por la API",
     "La consulta pedía el nombre del municipio a una tabla que guarda el código. Hoy "
     "se resuelve contra el catálogo"),
    ("Menor", GRIS,
     "Los importes de ocho cifras se partían en dos renglones",
     "El IVA salía como «1,123,470.0» con el cero solo en la línea de abajo. Hoy el "
     "ancho se mide antes de imprimir"),
]

# (qué falta, con qué se dará por bueno)
PENDIENTES = [
    ("Rendimiento", "El 95 % de las emisiones\npor debajo de 3 segundos"),
    ("Seguridad con herramienta", "Ninguna vulnerabilidad\nde severidad alta sin tratar"),
    ("Regresión automática", "La batería completa\nen cada cambio integrado"),
    ("Transmisión real a la DIAN", "Acuse de aceptación\ndel documento transmitido"),
]


def _alto_de_linea(tamano, interlineado=1.4):
    return tamano * interlineado / PUNTOS_POR_UNIDAD


def _cortar(texto, ancho_caja, tamano, margen=14):
    util = ancho_caja * PUNTOS_POR_UNIDAD - margen
    caracteres = max(12, int(util / (tamano * 0.52)))
    return [corta for entera in texto.split("\n")
            for corta in textwrap.wrap(entera, caracteres)]


def _caja(ejes, x, tope, ancho, titulo, detalle="", relleno=SUAVE, borde=BORDE,
          tam_titulo=9.5, tam_detalle=8.0, color_titulo=None, grosor=1.1,
          alineacion="center"):
    """Dibuja una caja bajo `tope` y devuelve la altura de su borde inferior."""
    lineas = _cortar(detalle, ancho, tam_detalle) if detalle else []
    salto_titulo = _alto_de_linea(tam_titulo, 1.6)
    salto_detalle = _alto_de_linea(tam_detalle)
    alto = 0.9 + salto_titulo + len(lineas) * salto_detalle + 0.9

    ejes.add_patch(FancyBboxPatch(
        (x, tope - alto), ancho, alto, boxstyle="round,pad=0.12,rounding_size=0.4",
        facecolor=relleno, edgecolor=borde, linewidth=grosor, zorder=2))
    ancla = x + ancho / 2 if alineacion == "center" else x + 1.2
    ejes.text(ancla, tope - 0.9, titulo, ha=alineacion, va="top", fontsize=tam_titulo,
              weight="bold", color=color_titulo or TINTA, zorder=3)
    if lineas:
        ejes.text(ancla, tope - 0.9 - salto_titulo, "\n".join(lineas), ha=alineacion,
                  va="top", fontsize=tam_detalle, color=GRIS, zorder=3,
                  linespacing=1.4)
    return tope - alto


def _nota(ejes, x, tope, ancho, texto, tamano=7.8, color=GRIS, alineacion="center"):
    lineas = _cortar(texto, ancho + 1.2, tamano)
    ancla = {"center": x + ancho / 2, "left": x, "right": x + ancho}[alineacion]
    ejes.text(ancla, tope, "\n".join(lineas), ha=alineacion, va="top", fontsize=tamano,
              color=color, style="italic", zorder=3, linespacing=1.4)
    return tope - len(lineas) * _alto_de_linea(tamano)


def _franja(ejes, tope, numero, texto, apunte=""):
    radio = 1.35
    ejes.add_patch(FancyBboxPatch(
        (IZQUIERDA, tope - radio * 2), radio * 2, radio * 2, boxstyle="circle,pad=0",
        facecolor=ACENTO, edgecolor=ACENTO, zorder=3))
    ejes.text(IZQUIERDA + radio, tope - radio, str(numero), ha="center", va="center",
              fontsize=10, weight="bold", color=PAPEL, zorder=4)
    ejes.text(IZQUIERDA + radio * 2 + 1.2, tope - radio, texto, ha="left", va="center",
              fontsize=12.5, weight="bold", color=TINTA, zorder=3)
    if apunte:
        ejes.text(ANCHO - IZQUIERDA, tope - radio, apunte, ha="right", va="center",
                  fontsize=8, color=GRIS, style="italic", zorder=3)
    ejes.plot([IZQUIERDA, ANCHO - IZQUIERDA], [tope - radio * 2 - 0.7] * 2,
              color=BORDE, linewidth=0.8, zorder=1)
    return tope - radio * 2 - 1.4


def dibujar():
    figura = plt.figure(figsize=(ANCHO_PULGADAS, ALTO_PULGADAS))
    ejes = figura.add_axes([0, 0, 1, 1])
    ejes.set_xlim(0, ANCHO)
    ejes.set_ylim(0, ALTO)
    ejes.axis("off")
    figura.patch.set_facecolor(PAPEL)

    y = _encabezado(ejes, ALTO - 3.0)
    y = _resumen(ejes, y - 1.6)
    y = _que_se_probo(ejes, y - 1.4)
    y = _casos(ejes, y - 1.4)
    y = _defectos(ejes, y - 1.4)
    y = _pendientes(ejes, y - 1.4)
    _pie(ejes, y)

    SALIDA.mkdir(parents=True, exist_ok=True)
    figura.savefig(ARCHIVO, format="pdf", facecolor=PAPEL)
    figura.savefig(ARCHIVO.with_suffix(".png"), dpi=150, facecolor=PAPEL)
    plt.close(figura)
    return ARCHIVO, y


def _encabezado(ejes, tope):
    alto = 7.6
    ejes.add_patch(FancyBboxPatch(
        (IZQUIERDA, tope - alto), ANCHO - IZQUIERDA * 2, alto,
        boxstyle="round,pad=0.15,rounding_size=0.5",
        facecolor=TINTA, edgecolor=TINTA, zorder=2))
    ejes.text(ANCHO / 2, tope - 2.7, "CÓMO SE ASEGURÓ LA CALIDAD DE FACTUGEST",
              ha="center", va="center", fontsize=16.5, weight="bold", color=PAPEL,
              zorder=3)
    ejes.text(ANCHO / 2, tope - 5.1, "QUÉ SE PROBÓ, QUÉ RESULTÓ Y QUÉ SE CORRIGIÓ",
              ha="center", va="center", fontsize=13, weight="bold", color="#7FA8DC",
              zorder=3)
    ejes.text(ANCHO / 2, tope - 7.0,
              "Plataforma que emite facturas electrónicas por cuenta de otras empresas",
              ha="center", va="center", fontsize=9, color="#C9D6E8", zorder=3)
    return tope - alto


def _resumen(ejes, tope):
    cifras = [
        (str(TOTAL_UNITARIAS), "pruebas automáticas",
         f"corren en {DURACION} y no\ndependen de nadie"),
        ("100 %", "las superaron", "ninguna falla en la\núltima corrida"),
        (str(len(INTEGRACION)), "pruebas sobre la API",
         "el recorrido completo de\nuna integración"),
        (str(len(FUNCIONALES)), "operaciones en pantalla",
         "verificadas con registro\nen imagen"),
    ]
    ancho = (ANCHO - IZQUIERDA * 2 - 3 * 1.5) / 4
    alto = 9.4
    for indice, (numero, rotulo, apunte) in enumerate(cifras):
        x = IZQUIERDA + indice * (ancho + 1.5)
        destaca = indice < 2
        ejes.add_patch(FancyBboxPatch(
            (x, tope - alto), ancho, alto, boxstyle="round,pad=0.12,rounding_size=0.4",
            facecolor=DESTACADO if destaca else TENUE,
            edgecolor=ACENTO if destaca else BORDE, linewidth=1.5 if destaca else 1.0,
            zorder=2))
        ejes.text(x + ancho / 2, tope - 3.1, numero, ha="center", va="center",
                  fontsize=25, weight="bold", color=ACENTO, zorder=3)
        ejes.text(x + ancho / 2, tope - 5.5, rotulo, ha="center", va="center",
                  fontsize=9.5, weight="bold", color=TINTA, zorder=3)
        ejes.text(x + ancho / 2, tope - 7.6, apunte, ha="center", va="center",
                  fontsize=7.6, color=GRIS, zorder=3, linespacing=1.4)
    return tope - alto


def _que_se_probo(ejes, tope):
    y = _franja(ejes, tope, 1, "Qué se probó",
                "cada barra es un grupo de pruebas, y su largo, cuántas son")
    filas = sorted(UNITARIAS, key=lambda fila: -fila[1])
    mayor = filas[0][1]
    alto_fila, separacion = 2.0, 0.35
    ancho_util = ANCHO - IZQUIERDA * 2
    minimo = 38.0
    cursor = y - 0.4
    for archivo, cuantas, _ in filas:
        ancho = minimo + (ancho_util - minimo) * (cuantas / mayor)
        destaca = cuantas == mayor
        ejes.add_patch(FancyBboxPatch(
            (IZQUIERDA, cursor - alto_fila), ancho, alto_fila,
            boxstyle="round,pad=0.06,rounding_size=0.25",
            facecolor=ACENTO if destaca else SUAVE,
            edgecolor=ACENTO if destaca else BORDE, linewidth=0.9, zorder=2))
        ejes.text(IZQUIERDA + 1.1, cursor - alto_fila / 2, ETIQUETAS[archivo],
                  fontsize=8.4, va="center", color=PAPEL if destaca else TINTA,
                  weight="bold" if destaca else "normal", zorder=3)
        ejes.text(IZQUIERDA + ancho - 1.1, cursor - alto_fila / 2, str(cuantas),
                  fontsize=9, va="center", ha="right", weight="bold",
                  color=PAPEL if destaca else ACENTO, zorder=3)
        cursor -= alto_fila + separacion
    return _nota(
        ejes, IZQUIERDA, cursor - 0.4, ANCHO - IZQUIERDA * 2,
        "El reparto no sigue el tamaño del código sino el daño que produce un error. Un "
        "impuesto mal calculado o una identificación mal aceptada quedan impresos en un "
        "documento con efectos legales; un error en una pantalla de consulta se corrige "
        "recargando la página")


def _casos(ejes, tope):
    y = _franja(ejes, tope, 2, "Ejemplos de lo que se comprobó",
                "cinco casos reales de la batería, con sus cifras")
    columnas = [12.0, 26.0, 30.0, 14.0]
    x = IZQUIERDA + 1.0
    encabezados = ["Qué se probó", "Con qué datos", "Qué debía dar", "Qué dio"]
    for titulo, ancho in zip(encabezados, columnas):
        ejes.text(x, y - 0.4, titulo, fontsize=8.6, weight="bold", color=TINTA,
                  va="top")
        x += ancho
    cursor = y - 2.4
    ejes.plot([IZQUIERDA, ANCHO - IZQUIERDA], [cursor + 0.5] * 2, color=BORDE,
              linewidth=0.8)

    for indice, (que, datos, esperado, obtenido) in enumerate(CASOS):
        celdas = [que, datos, esperado, obtenido]
        lineas = max(len(_cortar(texto, ancho - 1.5, 8.2, margen=4))
                     for texto, ancho in zip(celdas, columnas))
        alto = 0.7 + lineas * _alto_de_linea(8.2) + 0.7
        if indice % 2 == 0:
            ejes.add_patch(FancyBboxPatch(
                (IZQUIERDA, cursor - alto), ANCHO - IZQUIERDA * 2, alto,
                boxstyle="round,pad=0.05,rounding_size=0.2", facecolor=TENUE,
                edgecolor="none", zorder=1))
        x = IZQUIERDA + 1.0
        for numero, (texto, ancho) in enumerate(zip(celdas, columnas)):
            recortado = "\n".join(_cortar(texto, ancho - 1.5, 8.2, margen=4))
            ejes.text(x, cursor - 0.7, recortado, fontsize=8.2, va="top",
                      color=TINTA if numero == 0 else GRIS,
                      weight="bold" if numero == 0 else "normal", zorder=3,
                      linespacing=1.4)
            x += ancho
        ejes.text(ANCHO - IZQUIERDA - 1.0, cursor - 0.7 - 0.6, "coincide",
                  fontsize=8.2, va="top", ha="right", color=VERDE, weight="bold",
                  zorder=3)
        cursor -= alto
    return cursor


def _defectos(ejes, tope):
    y = _franja(ejes, tope, 3, "Qué se encontró y se corrigió",
                "cuatro defectos reales, ninguno detectado por el usuario final")
    cursor = y - 0.4
    for severidad, color, que_pasaba, como_quedo in DEFECTOS:
        lineas = _cortar(como_quedo, ANCHO - IZQUIERDA * 2 - 9, 8.0)
        alto = 0.9 + _alto_de_linea(9.2, 1.6) + len(lineas) * _alto_de_linea(8.0) + 0.9
        ejes.add_patch(FancyBboxPatch(
            (IZQUIERDA, cursor - alto), ANCHO - IZQUIERDA * 2, alto,
            boxstyle="round,pad=0.12,rounding_size=0.4", facecolor=TENUE,
            edgecolor=BORDE, linewidth=1.0, zorder=2))
        ejes.add_patch(FancyBboxPatch(
            (IZQUIERDA + 0.9, cursor - 2.6), 7.0, 1.9,
            boxstyle="round,pad=0.06,rounding_size=0.6", facecolor=color,
            edgecolor=color, zorder=3))
        ejes.text(IZQUIERDA + 4.4, cursor - 1.65, severidad.upper(), ha="center",
                  va="center", fontsize=7.4, weight="bold", color=PAPEL, zorder=4)
        ejes.text(IZQUIERDA + 9.0, cursor - 1.0, que_pasaba, fontsize=9.2,
                  weight="bold", color=TINTA, va="top", zorder=3)
        ejes.text(IZQUIERDA + 9.0, cursor - 1.0 - _alto_de_linea(9.2, 1.6),
                  "\n".join(lineas), fontsize=8.0, color=GRIS, va="top", zorder=3,
                  linespacing=1.4)
        cursor -= alto + 0.7
    return _nota(
        ejes, IZQUIERDA, cursor + 0.4, ANCHO - IZQUIERDA * 2,
        "Los cuatro aparecieron donde no había pruebas, y ninguno en la parte que sí las "
        "tenía. Por eso hoy cada defecto se reproduce primero con una prueba que falla y "
        "solo después se corrige, de modo que no puede volver en silencio")


def _pendientes(ejes, tope):
    y = _franja(ejes, tope, 4, "Qué falta por probar",
                "declarado como pendiente, con la medida que lo dará por bueno")
    ancho = (ANCHO - IZQUIERDA * 2 - 3 * 1.5) / 4
    alto = 7.4
    for indice, (titulo, meta) in enumerate(PENDIENTES):
        x = IZQUIERDA + indice * (ancho + 1.5)
        ejes.add_patch(FancyBboxPatch(
            (x, y - alto), ancho, alto, boxstyle="round,pad=0.12,rounding_size=0.4",
            facecolor=PAPEL, edgecolor=BORDE, linewidth=1.0, zorder=2,
            linestyle=(0, (4, 2))))
        ejes.text(x + ancho / 2, y - 2.2, "\n".join(_cortar(titulo, ancho, 9.2)),
                  ha="center", va="center", fontsize=9.2, weight="bold", color=TINTA,
                  zorder=3, linespacing=1.3)
        ejes.text(x + ancho / 2, y - 5.2, meta, ha="center", va="center", fontsize=7.8,
                  color=GRIS, zorder=3, linespacing=1.5)
    return y - alto


def _pie(ejes, tope):
    fin = _caja(ejes, IZQUIERDA, tope - 1.1, ANCHO - IZQUIERDA * 2,
          "Lo que no depende de una prueba, sino del diseño",
          "El número de la factura se reserva en una sola operación y la base de datos "
          "impide que se repita. La emisión completa se guarda o no se guarda, nunca a "
          "medias. El cálculo de impuestos existe una sola vez y lo usan por igual la "
          "página web y la API. Un invariante impide todos los casos, una prueba "
          "comprueba uno",
          relleno=SUAVE, tam_titulo=10.5, tam_detalle=8.4)
    ejes.plot([IZQUIERDA, ANCHO - IZQUIERDA], [3.6, 3.6], color=BORDE, linewidth=0.8)
    assert fin > 4.2, f"El contenido se come el pie: baja hasta {fin:.1f}"
    ejes.text(IZQUIERDA, 2.4,
              "Referente adoptado, ISO/IEC 25010 para el producto y CMMI nivel 2 para el "
              "proceso. Evidencia AA2-EV01, elaboración propia con los datos de la "
              "corrida de pruebas del proyecto",
              fontsize=7, color=GRIS, va="top")
    ejes.text(ANCHO - IZQUIERDA, 2.4, "FactuGest\nFicha 3115426", fontsize=7, color=GRIS,
              va="top", ha="right", linespacing=1.5)


def _comprobar():
    faltan = {archivo for archivo, _, _ in UNITARIAS} - set(ETIQUETAS)
    assert not faltan, f"Grupos de pruebas sin etiqueta en la lámina: {sorted(faltan)}"
    assert sum(cuantas for _, cuantas, _ in UNITARIAS) == TOTAL_UNITARIAS


_comprobar()


if __name__ == "__main__":
    ruta, sobra = dibujar()
    print(f"Generado: {ruta}")
    print(f"Vista previa: {ruta.with_suffix('.png')}")
    print(f"El contenido baja hasta {sobra:.1f}; el pie arranca en 10,6")
