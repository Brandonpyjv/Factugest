"""
Revisión final de los entregables.

Comprueba sobre el `.docx` lo que el instructivo APA exige y sobre el PDF lo que
solo se ve cuando Word arma las páginas. Se ejecuta después de regenerar, y su
salida es la lista de verificación del documento.

    python verificar.py                  # los cuatro entregables
    python verificar.py "ruta.docx"      # uno solo
"""
import re
import sys
from pathlib import Path

import pymupdf
from docx import Document
from docx.shared import Cm, Pt

ENTREGABLES = Path(__file__).resolve().parent.parent / "entregables"

# Los dos puntos son correctos en glosarios, etiquetas de dato y títulos de obras.
PERMITIDOS = re.compile(
    r"(Palabras clave|Keywords|Nota|Influencia|Interés|Middleware|Auditoría|Emisor|"
    r"Consecutivo|Excedente|Idempotencia|Trazabilidad|Bootstrap|Python|Pydantic|Uvicorn|"
    r"PyCharm|bcrypt|pytest|Swagger|CUFE|API|Rol|Cupo|Plan de suscripción|Tablero|"
    r"Factura electrónica|Nota crédito|Nota débito|Resolución de facturación|"
    r"Adquiriente|Proveedor tecnológico|Arquitectura|Jinja|MySQL|ReportLab|Chart|"
    r"software|Scrum|Guía de Scrum|routes|services|templates|static|tests|base|main|"
    r"migrate|Ingeniería del software|Git|OpenAPI|num2words|qrcode|Pillow|"
    r"itsdangerous|mysql-connector|FastAPI|Resolución \d+|Universal Business Language|"
    r"Test-driven development|The art of software testing)")


def _bien(texto):
    return f"  [OK]    {texto}"


def _mal(texto):
    return f"  [FALLA] {texto}"


def revisar_docx(ruta):
    """Lo que se comprueba sobre el archivo de Word."""
    d = Document(ruta)
    lineas = []

    seccion = d.sections[0]
    margenes = [seccion.top_margin, seccion.bottom_margin,
                seccion.left_margin, seccion.right_margin]
    correcto = all(abs(m.cm - 2.54) < 0.02 for m in margenes)
    lineas.append((_bien if correcto else _mal)(
        f"Márgenes de 2,54 cm — {[round(m.cm, 2) for m in margenes]}"))

    normal = d.styles["Normal"]
    lineas.append((_bien if normal.font.name == "Times New Roman" else _mal)(
        f"Fuente Times New Roman — {normal.font.name}"))
    lineas.append((_bien if normal.font.size == Pt(12) else _mal)(
        f"Tamaño de 12 puntos — {normal.font.size.pt}"))
    lineas.append((_bien if normal.paragraph_format.line_spacing == 2.0 else _mal)(
        f"Interlineado doble — {normal.paragraph_format.line_spacing}"))

    cuerpo = [p for p in d.paragraphs
              if p.style.name == "Normal" and len(p.text) > 120
              and p.paragraph_format.first_line_indent is not None]
    con_sangria = [p for p in cuerpo
                   if abs(p.paragraph_format.first_line_indent.cm - 1.27) < 0.02]
    lineas.append((_bien if len(con_sangria) > len(cuerpo) * 0.6 else _mal)(
        f"Sangría de 1,27 cm en el cuerpo — {len(con_sangria)} de {len(cuerpo)} párrafos"))

    encabezado = d.sections[0].header.paragraphs[0]
    tiene_numero = ">PAGE<" in encabezado._p.xml or "PAGE" in encabezado._p.xml
    lineas.append((_bien if tiene_numero else _mal)("Número de página en el encabezado"))
    lineas.append((_bien if encabezado.alignment == 2 else _mal)(
        "Encabezado alineado a la derecha"))

    rotulos = [p.text for p in d.paragraphs if re.fullmatch(r"(Tabla|Figura) \d+", p.text)]
    tablas = [r for r in rotulos if r.startswith("Tabla")]
    figuras = [r for r in rotulos if r.startswith("Figura")]
    for nombre, serie in (("tablas", tablas), ("figuras", figuras)):
        numeros = [int(r.split()[1]) for r in serie]
        seguidos = numeros == list(range(1, len(numeros) + 1))
        lineas.append((_bien if seguidos else _mal)(
            f"Numeración correlativa de {nombre} — {len(numeros)} rotuladas"))
    return lineas


def revisar_pdf(ruta):
    """Lo que solo se ve cuando Word arma las páginas."""
    d = pymupdf.open(ruta)
    lineas = []
    texto = " ".join(p.get_text() for p in d)

    vacias = [n for n, p in enumerate(d, 1)
              if len(p.get_text().strip()) < 6 and not p.get_images()]
    lineas.append((_bien if not vacias else _mal)(
        f"Sin páginas en blanco — {vacias if vacias else 'ninguna'}"))

    desbordes = []
    for n, p in enumerate(d, 1):
        apaisada = p.rect.width > p.rect.height
        ancho_max, alto_max = p.rect.width / 72 - 1.9, (7.4 if apaisada else 9.0)
        for imagen in p.get_images(full=True):
            for r in p.get_image_rects(imagen[0]):
                if r.width / 72 > ancho_max or r.height / 72 > alto_max:
                    desbordes.append(n)
    lineas.append((_bien if not desbordes else _mal)(
        f"Figuras dentro de los márgenes — {sorted(set(desbordes)) or 'todas'}"))

    huerfanos = []
    for n, p in enumerate(d, 1):
        renglones = [x.strip() for x in p.get_text().split("\n") if x.strip()]
        if renglones and re.fullmatch(r"(Tabla|Figura) \d+", renglones[-1]):
            huerfanos.append(n)
    lineas.append((_bien if not huerfanos else _mal)(
        f"Sin rótulos separados de su tabla o figura — {huerfanos or 'ninguno'}"))

    # Se captura el contexto anterior, porque el texto que se extrae de un PDF corta a
    # media palabra y un fragmento suelto no deja ver si el término es una entrada de
    # glosario —donde los dos puntos son correctos— o una explicación.
    sospechosos = [m.strip() for m in
                   re.findall(r".{0,45}: [a-záéíóúñ][a-záéíóúñ]+", texto)
                   if not PERMITIDOS.search(m)]
    lineas.append((_bien if not sospechosos else _mal)(
        f"Sin «afirmación breve: explicación» — {sospechosos[:6] or 'ninguno'}"))

    # El guion largo no lo escribe casi nadie a mano, y su presencia delata que el
    # texto no se redactó sino que se generó. En su lugar van comas, paréntesis o punto.
    rayas = [n for n, p in enumerate(d, 1) if "—" in p.get_text()]
    lineas.append((_bien if not rayas else _mal)(
        f"Sin guion largo, páginas {rayas[:8] if rayas else 'ninguna'}"))

    # El punto medio como separador es del mismo tipo, un signo que casi nadie teclea.
    puntos = [n for n, p in enumerate(d, 1) if "·" in p.get_text()]
    lineas.append((_bien if not puntos else _mal)(
        f"Sin punto medio, páginas {puntos[:8] if puntos else 'ninguna'}"))

    # La página del índice se busca, no se supone: el documento de grado lo lleva en
    # la tercera hoja porque abre con cubierta y portada, y un entregable suelto que
    # solo lleva portada lo tiene en la segunda.
    indice = next((p.get_text() for p in d if "Tabla de contenido" in p.get_text()), "")
    if indice:
        lleno = "No table of contents" not in indice and bool(re.search(r"\.{5,}\s*\d+", indice))
        lineas.append((_bien if lleno else _mal)("Tabla de contenido con paginación real"))

    lineas.append(_bien(f"Total de páginas — {d.page_count}"))
    d.close()
    return lineas


def revisar(ruta):
    ruta = Path(ruta)
    print(f"\n{ruta.name}")
    resultado = revisar_docx(ruta)
    pdf = ruta.with_suffix(".pdf")
    if pdf.exists():
        resultado += revisar_pdf(pdf)
    else:
        resultado.append(_mal("No existe el PDF; ejecuta revisar.py primero"))
    for linea in resultado:
        print(linea)
    return sum(1 for l in resultado if "[FALLA]" in l)


if __name__ == "__main__":
    archivos = ([Path(a) for a in sys.argv[1:]] or
                sorted(ENTREGABLES.glob("FactuGest*.docx")))
    fallas = sum(revisar(a) for a in archivos)
    print(f"\n{'Todo en orden.' if not fallas else f'{fallas} comprobaciones fallaron.'}")
    sys.exit(1 if fallas else 0)
