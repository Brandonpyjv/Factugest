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


PAQUETES = [
    ("Clientes API", ["Registrar cliente", "Generar y rotar llave", "Cambiar estado"]),
    ("Documentos electrónicos", ["Emitir factura", "Emitir notas", "Generar PDF y XML"]),
    ("Consumo y planes", ["Validar cupo", "Facturar mensualidad", "Cobrar excedentes"]),
    ("Facturación propia", ["Emitir factura propia", "Gestionar clientes", "Registrar pagos"]),
    ("Reportes y tablero", ["Consultar tablero", "Generar reporte", "Exportar reporte"]),
    ("Configuración", ["Empresas emisoras", "Impuestos y descuentos", "Marca de la empresa"]),
    ("Seguridad y auditoría", ["Iniciar sesión", "Asignar rol", "Consultar auditoría"]),
    ("Integración API REST", ["Autenticar por llave", "Emitir por API", "Consultar y descargar"]),
]


def diagrama_conceptual(destino):
    """Los ocho módulos como paquetes, con sus casos principales y los actores."""
    figura, ejes = plt.subplots(figsize=(11.8, 7.2))
    ejes.set_xlim(0, 15.8)
    ejes.set_ylim(0, 9.2)
    ejes.axis("off")

    ejes.add_patch(FancyBboxPatch((2.6, 0.35), 10.5, 8.52,
                                  boxstyle="round,pad=0.03,rounding_size=0.12",
                                  facecolor="#FBFCFE", edgecolor=TINTA, linewidth=1.4,
                                  zorder=0))
    ejes.text(7.85, 8.55, "FACTUGEST", ha="center", va="center", fontsize=11.5,
              color=TINTA, weight="bold", zorder=3)

    ancho, alto = 4.9, 1.75
    for indice, (nombre, casos) in enumerate(PAQUETES):
        columna, fila = indice % 2, indice // 2
        x = 2.9 + columna * (ancho + 0.3)
        y = 6.47 - fila * (alto + 0.14)
        ejes.add_patch(FancyBboxPatch((x, y), ancho, alto,
                                      boxstyle="round,pad=0.02,rounding_size=0.08",
                                      facecolor=SUAVE, edgecolor=ACENTO, linewidth=1.1,
                                      zorder=1))
        ejes.text(x + 0.22, y + alto - 0.34, nombre, fontsize=8.8, weight="bold",
                  color=ACENTO, va="center", zorder=3)
        for orden, caso in enumerate(casos):
            ejes.text(x + 0.34, y + alto - 0.76 - orden * 0.38, f"○  {caso}",
                      fontsize=7.8, color=TINTA, va="center", zorder=3)

    for x, y, nombre in [(1.35, 7.0, "Administrador"), (1.35, 4.4, "Cajero"),
                         (1.35, 1.9, "Supervisor"), (14.45, 7.0, "Sistema cliente"),
                         (14.45, 4.4, "Jefe de tienda"), (14.45, 1.9, "Comprador")]:
        _figura_actor(ejes, x, y, nombre)
        destino_x = 2.6 if x < 7 else 13.1
        ejes.plot([x + (0.5 if x < 7 else -0.5), destino_x], [y, y],
                  color=GRIS, linewidth=0.9, zorder=0)

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


def _figura_actor(ejes, x, y, nombre):
    escala = 0.16
    ejes.add_patch(plt.Circle((x, y + escala * 2.1), escala * 0.75, fill=False,
                              ec=TINTA, lw=1.3, zorder=3))
    ejes.plot([x, x], [y + escala * 1.35, y - escala * 0.6], color=TINTA, lw=1.3, zorder=3)
    ejes.plot([x - escala, x + escala], [y + escala * 0.9] * 2, color=TINTA, lw=1.3, zorder=3)
    ejes.plot([x - escala * 0.85, x, x + escala * 0.85],
              [y - escala * 1.9, y - escala * 0.6, y - escala * 1.9],
              color=TINTA, lw=1.3, zorder=3)
    ejes.text(x, y - escala * 2.9, "\n".join(textwrap.wrap(nombre, 16)), ha="center",
              va="top", fontsize=8, color=TINTA, weight="bold")


CAPAS = [
    ("Presentación", "#E3ECF8", [
        ("Navegador web\nPlantillas Jinja2, Bootstrap y Chart.js", 3.6),
        ("Sistema cliente\nPunto de venta, ERP o aplicación propia", 3.6),
    ]),
    ("Rutas", "#EDF2F9", [
        ("routes/ con 24 routers de la aplicación web", 3.6),
        ("routes/api/v1/ con 9 operaciones de integración", 3.6),
    ]),
    ("Lógica de negocio", "#DCE9F7", [
        ("services/ con 33 servicios de cálculo tributario, numeración, emisión, consumo, "
         "reportes, PDF y XML", 7.6),
    ]),
    ("Datos", "#EDF2F9", [
        ("Zona comercial\nfacturas, clientes y servicios", 2.45),
        ("Puente\nfacturas_plan", 2.45),
        ("Zona middleware\ndocumentos y clientes API", 2.45),
    ]),
]


def diagrama_estructural(destino):
    """La arquitectura por capas, con dos entradas sobre una sola lógica y una base en dos zonas."""
    figura, ejes = plt.subplots(figsize=(10.5, 7.6))
    ejes.set_xlim(0, 10.5)
    ejes.set_ylim(0, 9.2)
    ejes.axis("off")

    y = 7.9
    centros = []
    for nombre, color, cajas in CAPAS:
        ejes.text(0.15, y - 0.45, nombre, fontsize=9, weight="bold", color=ACENTO,
                  rotation=90, ha="center", va="center")
        x = 0.75
        fila = []
        for texto, ancho in cajas:
            _caja(ejes, x + ancho / 2, y - 0.45, ancho, 1.02, texto, relleno=color,
                  borde=BORDE, tamano=7.8, ajuste=46)
            fila.append((x + ancho / 2, y - 0.45))
            x += ancho + 0.35
        centros.append(fila)
        y -= 1.62

    # Presentación → rutas → servicios → datos
    for origen, destino_caja in zip(centros[0], centros[1]):
        _flecha(ejes, (origen[0], origen[1] - 0.51), (destino_caja[0], destino_caja[1] + 0.51))
    for origen in centros[1]:
        _flecha(ejes, (origen[0], origen[1] - 0.51), (centros[2][0][0], centros[2][0][1] + 0.51))
    for destino_caja in centros[3]:
        _flecha(ejes, (centros[2][0][0], centros[2][0][1] - 0.51),
                (destino_caja[0], destino_caja[1] + 0.51))

    ejes.text(5.25, 0.55,
              "Las dos entradas comparten la misma capa de servicios, de modo que una regla "
              "tributaria se implementa una vez\ny rige por igual para la aplicación web y "
              "para la API de integración.",
              ha="center", va="center", fontsize=8, color=GRIS, style="italic")

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


CUADRANTES = {
    # (columna, fila) con fila 1 arriba: (rótulo, qué exige, color, interesados)
    (0, 1): ("SATISFACER", "Alto interés · Baja influencia", "#DCE9F7",
             ["Contadores de las empresas", "Siste Soluciones\n(empresa colaboradora)"]),
    (1, 1): ("INVOLUCRAR", "Alto interés · Alta influencia", "#BBD4EE",
             ["Empresas clientes integradas", "Equipo de desarrollo",
              "Instructores y jurados"]),
    (0, 0): ("MONITOREAR", "Bajo interés · Baja influencia", "#F0F3F7",
             ["Compradores", "Gremios y cámaras de comercio"]),
    (1, 0): ("COMUNICAR", "Bajo interés · Alta influencia", "#DCE9F7",
             ["DIAN", "Proveedores de software\n(punto de venta y ERP)"]),
}


def matriz_stakeholders(destino):
    """Matriz de influencia e interés, con los interesados de FactuGest en sus cuadrantes."""
    figura, ejes = plt.subplots(figsize=(10, 6.6))
    ejes.set_xlim(-0.9, 10.2)
    ejes.set_ylim(-0.9, 7.2)
    ejes.axis("off")

    ancho, alto = 4.6, 3.2
    for (columna, fila), (rotulo, criterio, color, gente) in CUADRANTES.items():
        x0, y0 = 0.4 + columna * (ancho + 0.2), 0.4 + fila * (alto + 0.2)
        ejes.add_patch(FancyBboxPatch(
            (x0, y0), ancho, alto, boxstyle="round,pad=0.02,rounding_size=0.08",
            facecolor=color, edgecolor=ACENTO, linewidth=1.3, zorder=1))
        ejes.text(x0 + 0.28, y0 + alto - 0.42, rotulo, fontsize=10.5, weight="bold",
                  color=ACENTO, va="center", zorder=3)
        ejes.text(x0 + 0.28, y0 + alto - 0.82, criterio, fontsize=7.6, color=GRIS,
                  style="italic", va="center", zorder=3)
        for indice, nombre in enumerate(gente):
            ejes.text(x0 + 0.28, y0 + alto - 1.32 - indice * 0.62, f"-  {nombre}",
                      fontsize=8.6, color=TINTA, va="top", zorder=3)

    # Ejes rotulados por fuera, para que no compitan con el contenido del cuadrante.
    ejes.annotate("", xy=(9.8, -0.42), xytext=(0.4, -0.42),
                  arrowprops=dict(arrowstyle="-|>", color=TINTA, linewidth=1.3))
    ejes.text(5.1, -0.75, "INFLUENCIA", fontsize=9.5, weight="bold", color=TINTA,
              ha="center")
    ejes.text(0.4, -0.75, "baja", fontsize=8, color=GRIS, ha="left")
    ejes.text(9.8, -0.75, "alta", fontsize=8, color=GRIS, ha="right")

    ejes.annotate("", xy=(-0.42, 6.8), xytext=(-0.42, 0.4),
                  arrowprops=dict(arrowstyle="-|>", color=TINTA, linewidth=1.3))
    ejes.text(-0.72, 3.6, "INTERÉS", fontsize=9.5, weight="bold", color=TINTA,
              ha="center", va="center", rotation=90)
    ejes.text(-0.72, 0.4, "bajo", fontsize=8, color=GRIS, ha="center", va="bottom",
              rotation=90)
    ejes.text(-0.72, 6.8, "alto", fontsize=8, color=GRIS, ha="center", va="top",
              rotation=90)

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


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
    ejes.text(10.05, 5.6, "SPRINT DE 2 SEMANAS", ha="center", va="center",
              fontsize=9.5, color=ACENTO, weight="bold", zorder=3)

    _caja(ejes, 10.05, 4.6, 3.9, 0.85, "Reunión diaria de seguimiento",
          relleno="#FFFFFF", borde=BORDE, ajuste=34)
    _caja(ejes, 10.05, 3.5, 3.9, 0.95, "Desarrollo, revisión de código y pruebas",
          relleno="#FFFFFF", borde=BORDE, ajuste=34)
    _caja(ejes, 10.05, 2.3, 3.9, 0.95, "Incremento. Un módulo funcionando",
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
              "Cada sprint terminó con un módulo utilizable y no con una parte de varios, "
              "de modo que el avance se pudo mostrar y corregir.",
              ha="center", va="center", fontsize=8, color=GRIS, style="italic")

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


# (nombre, x, y, zona) — zona 'm' middleware, 'c' comercial, 'p' puente, 's' compartida
ENTIDADES = [
    ("EMPRESA\nEMISORA", 2.0, 8.3, "s"),
    ("CLIENTE API", 2.0, 5.9, "m"),
    ("PLAN", 2.0, 3.5, "m"),
    ("RECEPTOR", 2.0, 1.2, "m"),
    ("DOCUMENTO\nELECTRÓNICO", 7.0, 5.9, "m"),
    ("LÍNEA DE\nDOCUMENTO", 7.0, 3.5, "m"),
    ("EVENTO DEL\nDOCUMENTO", 7.0, 1.2, "m"),
    ("USUARIO", 12.2, 8.3, "s"),
    ("CLIENTE\nCOMERCIAL", 12.2, 5.9, "c"),
    ("FACTURA", 12.2, 3.5, "c"),
    ("DETALLE DE\nFACTURA", 12.2, 1.2, "c"),
    ("SERVICIO\nO PLAN", 16.6, 2.3, "c"),
]

# (desde, hasta, etiqueta, cardinalidad)
RELACIONES = [
    ("EMPRESA\nEMISORA", "DOCUMENTO\nELECTRÓNICO", "numera", "1:N"),
    ("CLIENTE API", "DOCUMENTO\nELECTRÓNICO", "emite", "1:N"),
    ("CLIENTE API", "PLAN", "contrata", "N:1"),
    ("RECEPTOR", "DOCUMENTO\nELECTRÓNICO", "recibe", "1:N"),
    ("DOCUMENTO\nELECTRÓNICO", "LÍNEA DE\nDOCUMENTO", "detalla", "1:N"),
    ("DOCUMENTO\nELECTRÓNICO", "EVENTO DEL\nDOCUMENTO", "registra", "1:N"),
    ("USUARIO", "FACTURA", "expide", "1:N"),
    ("CLIENTE\nCOMERCIAL", "FACTURA", "recibe", "1:N"),
    ("FACTURA", "DETALLE DE\nFACTURA", "detalla", "1:N"),
    ("SERVICIO\nO PLAN", "DETALLE DE\nFACTURA", "se factura en", "1:N"),
    ("CLIENTE API", "FACTURA", "se le cobra con", "1:N"),
]

COLOR_ZONA = {"m": "#DCE9F7", "c": "#E7F0E4", "p": "#F7E9DC", "s": "#EFEFF3"}


def modelo_conceptual(destino):
    """Modelo entidad-relación conceptual, con las dos zonas de la base diferenciadas."""
    figura, ejes = plt.subplots(figsize=(12.5, 7.6))
    ejes.set_xlim(0, 18.6)
    ejes.set_ylim(0, 10.9)
    ejes.axis("off")

    posicion = {}
    ancho, alto = 2.5, 1.15
    for nombre, x, y, zona in ENTIDADES:
        posicion[nombre] = (x, y)
        ejes.add_patch(FancyBboxPatch((x - ancho / 2, y - alto / 2), ancho, alto,
                                      boxstyle="round,pad=0.02,rounding_size=0.08",
                                      facecolor=COLOR_ZONA[zona], edgecolor=TINTA,
                                      linewidth=1.2, zorder=2))
        ejes.text(x, y, nombre, ha="center", va="center", fontsize=8.2, color=TINTA,
                  weight="bold", zorder=3)

    for desde, hasta, etiqueta, cardinalidad in RELACIONES:
        (x1, y1), (x2, y2) = posicion[desde], posicion[hasta]
        ejes.plot([x1, x2], [y1, y2], color=GRIS, linewidth=1.0, zorder=1)
        # A un tercio del trayecto y no en el centro, porque el punto medio de una
        # relación entre entidades alineadas cae justo encima de la que queda en medio.
        medio_x, medio_y = x1 + (x2 - x1) * 0.34, y1 + (y2 - y1) * 0.34
        ejes.text(medio_x, medio_y, f"{etiqueta}\n{cardinalidad}", ha="center", va="center",
                  fontsize=7.0, color=GRIS, style="italic", zorder=4,
                  bbox=dict(facecolor="white", edgecolor="none", pad=1.4))

    leyenda = [("Zona middleware. Lo que se emite por cuenta de terceros", "m"),
               ("Zona comercial. Lo que el proveedor vende", "c"),
               ("Entidades compartidas por las dos zonas", "s")]
    for indice, (texto, zona) in enumerate(leyenda):
        y = 10.6 - indice * 0.42
        ejes.add_patch(FancyBboxPatch((0.55, y - 0.13), 0.42, 0.26,
                                      boxstyle="round,pad=0.01,rounding_size=0.04",
                                      facecolor=COLOR_ZONA[zona], edgecolor=TINTA,
                                      linewidth=0.9, zorder=2))
        ejes.text(1.12, y, texto, fontsize=7.8, color=TINTA, va="center")

    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(figura)
    return destino


# --- Cronograma -----------------------------------------------------------------
# El cuadro de cuatro filas decía en qué meses ocurrió cada fase, pero no dejaba ver
# lo único que un cronograma tiene que mostrar: que las fases se solapan y cuánto
# dura cada una comparada con las demás. Los periodos son los mismos del cuadro, y
# las actividades son las que ese cuadro enumeraba dentro de cada fase.

MES_CERO = ("mar", 2025)          # primera columna del eje
MESES_TOTAL = 17                  # de marzo de 2025 a julio de 2026
REJILLA = "#D5DDE7"
ABREVIATURAS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun",
                "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]

# (fase, color, [(actividad, mes de inicio, duración en meses)])
FASES = [
    ("Análisis", "#A9C6E8", [
        ("Levantamiento de requisitos", 0, 3),
        ("Identificación de actores", 1, 2),
        ("Análisis del problema", 2, 2)]),
    ("Planeación", "#7BA6DA", [
        ("Diseño de la solución y arquitectura", 4, 2),
        ("Modelado de datos y casos de uso", 5, 2),
        ("Conformación del backlog", 6, 2)]),
    ("Ejecución", "#4C82C6", [
        ("Ocho sprints de dos semanas", 8, 5),
        ("Integración de módulos", 12, 2),
        ("Pruebas técnicas", 13, 2)]),
    ("Evaluación", "#1F5FA8", [
        ("Pruebas finales y corrección", 15, 1),
        ("Sustentación", 16, 1)]),
]


def cronograma_gantt(destino):
    """Diagrama de Gantt de las cuatro fases, con sus actividades mes a mes."""
    filas = sum(len(a) for _, _, a in FASES)
    figura, ejes = plt.subplots(figsize=(13.0, 5.6))
    ejes.set_xlim(-0.02, MESES_TOTAL + 1.3)
    ejes.set_ylim(-1.3, filas - 0.25)
    ejes.invert_yaxis()
    ejes.axis("off")

    # Rejilla de meses por debajo de las barras; sin ella no se puede leer dónde
    # empieza una actividad sin seguir la línea con el dedo hasta el eje.
    for mes in range(MESES_TOTAL + 1):
        grueso = mes == 10          # cambio de año, entre diciembre y enero
        ejes.plot([mes, mes], [-0.75, filas - 0.35], color=BORDE if grueso else REJILLA,
                  linewidth=1.1 if grueso else 0.7, zorder=0)

    for mes in range(MESES_TOTAL):
        indice = (ABREVIATURAS.index(MES_CERO[0].capitalize()) + mes) % 12
        ejes.text(mes + 0.5, -0.55, ABREVIATURAS[indice], ha="center", va="center",
                  fontsize=8.6, color=GRIS)
    ejes.text(5.0, -0.98, "2025", ha="center", va="center", fontsize=9.4, color=TINTA,
              weight="bold")
    ejes.text(13.5, -0.98, "2026", ha="center", va="center", fontsize=9.4, color=TINTA,
              weight="bold")

    fila = 0
    for nombre, color, actividades in FASES:
        primera, ultima = fila, fila + len(actividades) - 1
        # Banda de la fase en el canal izquierdo: agrupa sus actividades sin gastar
        # una fila de barra en repetir lo que la agrupación ya dice.
        ejes.add_patch(FancyBboxPatch(
            (-5.9, primera - 0.36), 0.16, (ultima - primera) + 0.72,
            boxstyle="round,pad=0.01,rounding_size=0.05",
            facecolor=color, edgecolor="none", clip_on=False, zorder=3))
        ejes.text(-6.07, (primera + ultima) / 2, nombre, ha="right", va="center",
                  fontsize=10.2, color=TINTA, weight="bold", clip_on=False)

        for actividad, inicio, duracion in actividades:
            ejes.text(-5.65, fila, actividad, ha="left", va="center", fontsize=9.0,
                      color=TINTA, clip_on=False)
            ejes.add_patch(FancyBboxPatch(
                (inicio + 0.06, fila - 0.24), duracion - 0.12, 0.48,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                facecolor=color, edgecolor=ACENTO, linewidth=0.8, zorder=2))
            meses = f"{duracion} mes" + ("es" if duracion > 1 else "")
            ejes.text(inicio + duracion + 0.16, fila, meses, ha="left", va="center",
                      fontsize=7.8, color=GRIS)
            fila += 1

    figura.subplots_adjust(left=0.33, right=0.985, top=0.98, bottom=0.02)
    Path(destino).parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(destino, dpi=200, facecolor="white")
    plt.close(figura)
    return destino


if __name__ == "__main__":
    salida = Path(__file__).resolve().parent.parent / "entregables" / "diagramas"
    print("Generado:", cronograma_gantt(salida / "FIG-cronograma.png"))
