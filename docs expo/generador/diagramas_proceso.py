"""
Diagramas de proceso del documento: el ciclo Scrum y el instrumento de encuesta.

Se dibujan por código, igual que los de casos de uso, para que puedan rehacerse
cuando cambie lo que representan sin depender de una herramienta externa ni de
volver a maquetar una imagen a mano.
"""
import textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

TINTA = "#26364A"
ACENTO = "#1F5FA8"
SUAVE = "#E9EFF7"
BORDE = "#8FA6C4"
GRIS = "#5A6B80"


def _caja(ejes, x, y, ancho, alto, texto, relleno=SUAVE, borde=TINTA, tamano=8.5,
          negrita=False, ajuste=22):
    ejes.add_patch(FancyBboxPatch(
        (x - ancho / 2, y - alto / 2), ancho, alto,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        facecolor=relleno, edgecolor=borde, linewidth=1.2, zorder=2))
    # Se ajusta línea por línea: `textwrap.wrap` sobre el texto completo se come los
    # saltos que quien escribe puso a propósito para separar el rótulo del detalle.
    lineas = [corta for entera in texto.split("\n") for corta in textwrap.wrap(entera, ajuste)]
    ejes.text(x, y, "\n".join(lineas), ha="center", va="center",
              fontsize=tamano, color=TINTA, zorder=3,
              weight="bold" if negrita else "normal")


def _flecha(ejes, desde, hasta, curva=0.0, color=GRIS, etiqueta=None):
    ejes.add_patch(FancyArrowPatch(
        desde, hasta, connectionstyle=f"arc3,rad={curva}",
        arrowstyle="-|>", mutation_scale=13, linewidth=1.2, color=color, zorder=1))
    if etiqueta:
        medio = ((desde[0] + hasta[0]) / 2, (desde[1] + hasta[1]) / 2)
        ejes.text(medio[0], medio[1] + 0.18, etiqueta, ha="center", va="bottom",
                  fontsize=7.5, color=color, style="italic", zorder=4,
                  bbox=dict(facecolor="white", edgecolor="none", pad=1.2))


def ciclo_scrum(destino):
    """El ciclo de Scrum con los valores reales del proyecto.

    Se rotula con la duración de sprint y los artefactos que el proyecto usó, no
    con el esquema genérico: un diagrama que podría ilustrar cualquier proyecto no
    aporta nada al documento de este.
    """
    figura, ejes = plt.subplots(figsize=(11, 5.6))
    ejes.set_xlim(0, 14)
    ejes.set_ylim(0, 7.2)
    ejes.axis("off")

    _caja(ejes, 1.9, 3.6, 3.0, 1.5, "Product backlog\n82 requisitos priorizados",
          relleno="#FFFFFF", negrita=True, ajuste=26)
    _caja(ejes, 5.6, 5.6, 2.9, 1.1, "Planificación del sprint", ajuste=24)
    _caja(ejes, 5.6, 3.6, 2.9, 1.2, "Sprint backlog\nlo comprometido para 2 semanas",
          ajuste=26)

    # El sprint, como contenedor
    ejes.add_patch(FancyBboxPatch(
        (7.6, 1.5), 4.9, 4.4, boxstyle="round,pad=0.03,rounding_size=0.15",
        facecolor="#F5F8FC", edgecolor=ACENTO, linewidth=1.4, zorder=0))
    ejes.text(10.05, 5.6, "SPRINT — 2 semanas", ha="center", va="center",
              fontsize=9.5, color=ACENTO, weight="bold", zorder=3)

    _caja(ejes, 10.05, 4.6, 3.9, 0.85, "Reunión diaria de seguimiento",
          relleno="#FFFFFF", borde=BORDE, ajuste=34)
    _caja(ejes, 10.05, 3.5, 3.9, 0.95, "Desarrollo, revisión de código y pruebas",
          relleno="#FFFFFF", borde=BORDE, ajuste=34)
    _caja(ejes, 10.05, 2.3, 3.9, 0.95, "Incremento: módulo funcionando",
          relleno=SUAVE, borde=ACENTO, negrita=True, ajuste=34)

    _caja(ejes, 5.6, 1.35, 2.9, 1.1, "Revisión y retrospectiva", ajuste=24)

    _flecha(ejes, (3.4, 4.0), (4.6, 5.05))
    _flecha(ejes, (5.6, 5.05), (5.6, 4.25))
    _flecha(ejes, (7.05, 3.6), (7.9, 3.6))
    _flecha(ejes, (10.05, 4.15), (10.05, 4.0))
    _flecha(ejes, (10.05, 3.0), (10.05, 2.8))
    _flecha(ejes, (8.1, 2.3), (7.05, 1.5), curva=0.15)
    _flecha(ejes, (4.15, 1.5), (2.3, 2.85), curva=0.15,
            etiqueta="lo aprendido vuelve al backlog")

    ejes.text(7.0, 0.45,
              "Cada sprint terminó con un módulo utilizable, no con una parte de varios: "
              "así el avance se pudo mostrar y corregir.",
              ha="center", va="center", fontsize=8, color=GRIS, style="italic")

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino
