"""
Encuesta de elicitación: instrumento, datos y figuras.

Los datos viven aquí y en ningún otro lugar. El capítulo 3 toma de este módulo
tanto las gráficas como las cifras que menciona en el texto, de modo que el tamaño
de la muestra y los porcentajes no puedan discrepar entre una sección y otra: una
cifra que cambia entre el análisis y la gráfica es lo primero que delata un dato
mal llevado.

**Sobre el color.** Cada gráfica presenta una sola distribución, así que el color
no codifica identidad: hay un tono de acento para la barra que sostiene el hallazgo
y un tono recesivo para el resto. La pareja `#1F5FA8` / `#5C93D6` pasa las seis
comprobaciones de la guía de visualización —banda de luminosidad, croma, separación
para daltonismo, separación en visión normal y contraste contra el fondo—. La
identidad de cada barra la lleva su rótulo, no su color.
"""
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ACENTO = "#1F5FA8"
RECESIVO = "#5C93D6"
TINTA = "#26364A"
SECUNDARIA = "#5A6B80"
LINEA = "#D5DDE7"

MUESTRA = 45          # empresas encuestadas. Cámbiese aquí y en ningún otro sitio.

# (pregunta abreviada, [(opción, respuestas)], índice de la barra destacada)
RESULTADOS = [
    ("¿Su empresa está obligada a facturar electrónicamente?",
     [("Sí", 37), ("No", 5), ("No lo sé", 3)], 0),

    ("¿Emite facturación electrónica actualmente?",
     [("Sí", 17), ("No", 21), ("Está en proceso", 7)], 1),

    ("¿Con qué software administra hoy sus ventas?",
     [("Punto de venta", 18), ("Sistema contable", 10), ("Hojas de cálculo", 9),
      ("Aplicación propia", 6), ("Ninguno", 2)], 0),

    ("Principal dificultad para adoptarla",
     [("Cambiar de software", 17), ("El costo", 13), ("No saber cómo hacerlo", 9),
      ("Capacitar al personal", 4), ("Ninguna", 2)], 0),

    ("¿Cambiaría el software con el que trabaja hoy?",
     [("Sí", 8), ("No", 26), ("Tal vez", 11)], 1),

    ("¿Le interesaría facturar sin cambiar de software?",
     [("Sí", 38), ("Tal vez", 5), ("No", 2)], 0),
]

# Preguntas que no van a la gráfica pero sí se citan en el análisis.
VOLUMEN = [("Menos de 50", 14), ("De 50 a 150", 18), ("De 151 a 400", 9), ("Más de 400", 4)]
PAGO = [("Menos de $50.000", 11), ("$50.000 a $100.000", 19),
        ("$100.001 a $200.000", 12), ("Más de $200.000", 3)]
CORRECCIONES = [("Nunca", 12), ("Rara vez", 24), ("Con frecuencia", 9)]
SOPORTE_ALTO = 39     # respondieron 4 o 5 sobre la importancia del soporte
REPORTES_SI = 36      # respondieron que sí les interesarían reportes


def porcentaje(cantidad):
    return round(cantidad * 100 / MUESTRA)


def _barras(ejes, titulo, opciones, destacada):
    etiquetas = [o for o, _ in opciones]
    valores = [v for _, v in opciones]
    posiciones = range(len(valores))

    for posicion, valor in zip(posiciones, valores):
        color = ACENTO if posicion == destacada else RECESIVO
        # Extremo redondeado y anclado en el cero, como marca la guía de marcas.
        ejes.add_patch(FancyBboxPatch(
            (0, posicion - 0.28), max(valor, 0.35), 0.56,
            boxstyle="round,pad=0,rounding_size=0.55",
            facecolor=color, edgecolor="white", linewidth=1.2, zorder=2,
            mutation_aspect=0.12))
        ejes.text(valor + max(valores) * 0.035, posicion,
                  f"{valor}  ({porcentaje(valor)} %)", va="center", ha="left",
                  fontsize=7.6, color=TINTA, zorder=3)

    ejes.set_yticks(list(posiciones))
    ejes.set_yticklabels(["\n".join(textwrap.wrap(e, 18)) for e in etiquetas], fontsize=7.6,
                         color=TINTA)
    # Aire arriba para que el título no quede pegado a la primera barra.
    ejes.set_ylim(len(valores) - 0.5, -0.95)
    ejes.set_xlim(0, max(valores) * 1.34)
    ejes.set_xticks([])
    for lado in ("top", "right", "bottom"):
        ejes.spines[lado].set_visible(False)
    ejes.spines["left"].set_color(LINEA)
    ejes.tick_params(axis="y", length=0)
    ejes.set_title("\n".join(textwrap.wrap(titulo, 44)), fontsize=8.6, color=TINTA,
                   loc="left", pad=8, weight="bold")


def grafica_resultados(destino):
    # Cada fila se alta en proporción a cuántas opciones tiene: con altura igual, los
    # paneles de tres respuestas quedan con la mitad del cuadro en blanco y sus barras
    # se leen como si midieran más que las de al lado.
    alturas = [max(len(RESULTADOS[fila * 2][1]), len(RESULTADOS[fila * 2 + 1][1]))
               for fila in range(3)]
    figura, ejes = plt.subplots(3, 2, figsize=(11, 8.6),
                                gridspec_kw={"height_ratios": alturas})
    for cuadro, (titulo, opciones, destacada) in zip(ejes.flat, RESULTADOS):
        _barras(cuadro, titulo, opciones, destacada)
    figura.suptitle(f"Resultados de la encuesta aplicada a {MUESTRA} empresas",
                    fontsize=11, color=TINTA, weight="bold", y=0.985)
    figura.tight_layout(rect=(0, 0, 1, 0.965), h_pad=3.2, w_pad=4.0)

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


PREGUNTAS_FORMULARIO = [
    ("1. ¿Su empresa está obligada a facturar electrónicamente ante la DIAN?",
     ["Sí", "No", "No lo sé"], 0),
    ("2. ¿Emite facturación electrónica actualmente?",
     ["Sí", "No", "Está en proceso"], 1),
    ("3. ¿Con qué software administra hoy sus ventas?",
     ["Punto de venta", "Sistema contable", "Aplicación propia", "Hojas de cálculo"], 0),
    ("5. ¿Cuál ha sido la principal dificultad para adoptarla?",
     ["El costo", "Tener que cambiar de software", "No saber cómo hacerlo",
      "La capacitación del personal"], 1),
    ("6. ¿Cambiaría el software con el que trabaja hoy para poder facturar?",
     ["Sí", "No", "Tal vez"], 1),
    ("7. Si su software actual emitiera la factura automáticamente, ¿le interesaría?",
     ["Sí", "No", "Tal vez"], 0),
]

ANCHO_ENUNCIADO = 62
ALTO_LINEA = 0.40
AIRE_ENUNCIADO = 0.14   # entre el enunciado y su primera opción
ALTO_OPCION = 0.42
ALTO_SEPARADOR = 0.52


def _alto_formulario():
    """Cuánto mide el formulario, en unidades del lienzo.

    Se calcula en vez de fijarse: con un alto fijo, agregar una pregunta o alargar
    un enunciado empuja las últimas preguntas fuera del lienzo, y lo que se recorta
    no avisa —queda un formulario en el que las dos últimas preguntas aparecen sin
    sus opciones—.
    """
    alto = 1.9                              # encabezado
    for enunciado, opciones, _ in PREGUNTAS_FORMULARIO:
        alto += ALTO_LINEA * len(textwrap.wrap(enunciado, ANCHO_ENUNCIADO)) + AIRE_ENUNCIADO
        alto += ALTO_OPCION * len(opciones) + ALTO_SEPARADOR
    return alto + 0.9                       # pie


def formulario(destino):
    """Representación del formulario digital con el que se aplicó el instrumento."""
    alto = _alto_formulario()
    figura, ejes = plt.subplots(figsize=(7.6, 7.6 * alto / 10.0))
    ejes.set_xlim(0, 10)
    ejes.set_ylim(0, alto)
    ejes.axis("off")

    ejes.add_patch(FancyBboxPatch((0.3, alto - 1.55), 9.4, 1.3,
                                  boxstyle="round,pad=0.02,rounding_size=0.1",
                                  facecolor=ACENTO, edgecolor="none"))
    ejes.text(0.75, alto - 0.68, "FactuGest. Diagnóstico de facturación electrónica",
              fontsize=11, color="white", weight="bold", va="center")
    ejes.text(0.75, alto - 1.18,
              "Encuesta dirigida a micro, pequeñas y medianas empresas. Cúcuta, 2025",
              fontsize=8.2, color="#D8E4F4", va="center")

    y = alto - 2.0
    for enunciado, opciones, marcada in PREGUNTAS_FORMULARIO:
        lineas = textwrap.wrap(enunciado, ANCHO_ENUNCIADO)
        ejes.text(0.55, y, "\n".join(lineas), fontsize=8.6, color=TINTA, va="top",
                  weight="bold")
        y -= ALTO_LINEA * len(lineas) + AIRE_ENUNCIADO
        for indice, opcion in enumerate(opciones):
            elegido = indice == marcada
            ejes.add_patch(plt.Circle((0.85, y + 0.06), 0.11, facecolor="white",
                                      edgecolor=ACENTO if elegido else "#B7C4D4",
                                      linewidth=1.4, zorder=2))
            if elegido:
                ejes.add_patch(plt.Circle((0.85, y + 0.06), 0.055, facecolor=ACENTO,
                                          edgecolor="none", zorder=3))
            ejes.text(1.15, y + 0.06, opcion, fontsize=8.2, va="center",
                      color=TINTA if elegido else SECUNDARIA)
            y -= ALTO_OPCION
        y -= ALTO_SEPARADOR - 0.16
        ejes.plot([0.55, 9.45], [y, y], color=LINEA, linewidth=0.9)
        y -= 0.16

    ejes.text(0.55, 0.35,
              f"Respuestas recibidas: {MUESTRA}.    Preguntas 4 y 8 a 12 en la página "
              "siguiente del formulario",
              fontsize=7.8, color=SECUNDARIA, style="italic")

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


def grafica_contraste(destino):
    """Las preguntas 6 y 7, una al lado de la otra.

    Es el hallazgo que sostiene el proyecto, y en la sustentación se muestra solo,
    sin las otras cuatro gráficas. El panel completo del documento tiene seis
    distribuciones y proyectado no se distingue cuál es la que importa.
    """
    # Muy apaisada a propósito, para que en la diapositiva pueda ocupar todo el
    # ancho disponible sin que el alto la obligue a encogerse.
    figura, ejes = plt.subplots(1, 2, figsize=(12, 2.95))
    for cuadro, (titulo, opciones, destacada) in zip(ejes, RESULTADOS[4:6]):
        _barras(cuadro, titulo, opciones, destacada)
        cuadro.title.set_fontsize(11)
        for etiqueta in cuadro.get_yticklabels():
            etiqueta.set_fontsize(9.5)
    figura.tight_layout(w_pad=5.0)
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino
