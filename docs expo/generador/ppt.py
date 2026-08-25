"""
Motor de las diapositivas de sustentación.

Trabaja **sobre el archivo del cliente**, `Diapositivas factugest.pptx`, porque su
diseño, su fondo y sus colores son los que exige el centro de formación. Aquí no se
crea una presentación nueva ni se toca la plantilla: se limpia el contenido viejo de
cada diapositiva y se escribe el nuevo encima, conservando intactos el fondo, el
logo, la marca de agua, la barra del título y la línea inferior.

**Qué se conserva y qué se reemplaza.** Todo lo que dibuja la identidad visual son
imágenes o autoformas colocadas en posiciones fijas, y de ahí sale la regla que usa
`limpiar()`: se borran los cuadros de texto que caen por debajo de la zona del
título, junto con los iconos pequeños que acompañaban a esos textos, y no se toca
nada más.

**Tamaños de letra.** El borrador venía con cuerpo de 10 a 14 puntos, que es tamaño
de documento y proyectado no se lee. Aquí el cuerpo arranca en 20 y los textos
destacados en 24, según la decisión tomada con el cliente.
"""
import copy
import subprocess
import time
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu, Inches, Pt

BASE = Path(__file__).resolve().parent.parent
EXPOSICION = BASE / "carpeta exposicion"
ORIGEN = EXPOSICION / "Diapositivas factugest.pptx"
DESTINO = EXPOSICION / "FactuGest - Sustentación.pptx"

DIAGRAMAS = BASE / "entregables" / "diagramas"
CAPTURAS = BASE / "documento para que te guies claude"

# Colores tomados de la propia plantilla.
AZUL = RGBColor(0x1F, 0x3B, 0x73)
TINTA = RGBColor(0x33, 0x37, 0x3D)
GRIS = RGBColor(0x6B, 0x72, 0x80)
AMARILLO = RGBColor(0xF5, 0xA6, 0x23)
FILA_CLARA = RGBColor(0xFF, 0xFF, 0xFF)
FILA_ALTERNA = RGBColor(0xEF, 0xF3, 0xF9)

# Tamaños. El cuerpo no baja de 20 puntos.
TITULO = Pt(27)
DESTACADO = Pt(24)
CUERPO = Pt(20)
SECUNDARIO = Pt(16)
PIE = Pt(13)

FUENTE = "Arial"

# La zona del título llega hasta esta altura; por debajo empieza el contenido.
LIMITE_TITULO = Inches(1.25)
# Los iconos de viñeta del borrador miden menos que esto.
ICONO = Inches(0.45)


def abrir():
    return Presentation(ORIGEN)


def _es_decoracion(forma):
    """La marca de agua y la línea inferior, que van en todas las diapositivas."""
    if forma.width is None:
        return False
    marca_de_agua = abs(forma.width - Inches(5.5)) < Inches(0.1) and         abs(forma.left - Inches(3.92)) < Inches(0.1)
    linea_inferior = forma.width > Inches(13)
    return marca_de_agua or linea_inferior


def limpiar(diapositiva, imagenes=False, tablas=True):
    """Quita el contenido viejo sin tocar el fondo ni la decoración.

    Siempre se borran los cuadros de texto y las tablas que están por debajo de la
    zona del título, junto con los iconos pequeños que los acompañaban, porque un
    icono de viñeta sin su texto queda flotando en mitad de la diapositiva.

    Con `imagenes=True` se borran además las imágenes de contenido, como las
    tarjetas del borrador, y se conservan únicamente la marca de agua y la línea
    inferior, que son parte del diseño de la plantilla.
    """
    for forma in list(diapositiva.shapes):
        if forma.top is None or forma.top <= LIMITE_TITULO:
            continue
        es_texto = forma.has_text_frame and not forma.has_table
        es_imagen = forma.shape_type == 13
        icono = es_imagen and forma.width is not None and forma.width < ICONO
        sobra = (es_texto or (tablas and forma.has_table) or icono or
                 (imagenes and es_imagen and not _es_decoracion(forma)))
        if sobra:
            forma._element.getparent().remove(forma._element)


def titulo(diapositiva, texto):
    """Reescribe el título conservando su cuadro, su posición y su formato."""
    for forma in diapositiva.shapes:
        if (forma.has_text_frame and forma.top is not None
                and forma.top <= LIMITE_TITULO and forma.text_frame.text.strip()):
            marco = forma.text_frame
            marco.paragraphs[0].runs[0].text = texto
            for extra in marco.paragraphs[0].runs[1:]:
                extra.text = ""
            # El cuadro del borrador medía seis pulgadas, y un título algo más largo
            # se partía en dos líneas y caía encima de la barra amarilla.
            forma.width = Inches(11.4)
            return forma
    return _cuadro(diapositiva, texto, 0.62, 0.52, 11.5, 0.6, TITULO, AZUL, negrita=True)


def _cuadro(diapositiva, texto, x, y, ancho, alto, tamano, color, negrita=False,
            alineacion=PP_ALIGN.LEFT):
    forma = diapositiva.shapes.add_textbox(Inches(x), Inches(y), Inches(ancho), Inches(alto))
    marco = forma.text_frame
    marco.word_wrap = True
    parrafo = marco.paragraphs[0]
    parrafo.alignment = alineacion
    run = parrafo.add_run()
    run.text = texto
    run.font.size = tamano
    run.font.bold = negrita
    run.font.color.rgb = color
    run.font.name = FUENTE
    return forma


def parrafo(diapositiva, texto, x, y, ancho, alto=0.8, tamano=CUERPO, color=TINTA,
            negrita=False, alineacion=PP_ALIGN.LEFT):
    return _cuadro(diapositiva, texto, x, y, ancho, alto, tamano, color, negrita, alineacion)


def vinetas(diapositiva, elementos, x, y, ancho, tamano=CUERPO, separacion=0.92):
    """Lista de puntos, cada uno con la idea completa y escrita de corrido.

    **Cada punto es una sola frase seguida.** No se parte en un rótulo destacado y
    un detalle detrás, ni se resaltan en negrita las primeras palabras. Ese formato
    de «concepto en negrita, punto, explicación» es el que delata que el texto se
    generó en lugar de redactarse, y en una diapositiva se nota más que en un
    documento porque las tres viñetas se ven a la vez.

    Cada elemento es un texto. Si alguien pasa una tupla, es señal de que está
    volviendo al formato anterior, y por eso se rechaza.
    """
    formas = []
    for indice, elemento in enumerate(elementos):
        if not isinstance(elemento, str):
            raise TypeError(
                "Cada viñeta es una frase completa. El formato de rótulo destacado más "
                "detalle quedó descartado por decisión del cliente.")
        forma = diapositiva.shapes.add_textbox(Inches(x), Inches(y + indice * separacion),
                                               Inches(ancho), Inches(separacion))
        marco = forma.text_frame
        marco.word_wrap = True
        run = marco.paragraphs[0].add_run()
        run.text = elemento
        run.font.color.rgb = TINTA
        run.font.size = tamano
        run.font.name = FUENTE
        formas.append(forma)
    return formas


def imagen(diapositiva, ruta, x, y, ancho=None, alto=None):
    """Inserta una imagen. Con solo uno de los dos lados, conserva la proporción."""
    return diapositiva.shapes.add_picture(
        str(ruta), Inches(x), Inches(y),
        width=Inches(ancho) if ancho else None,
        height=Inches(alto) if alto else None)


def imagen_ajustada(diapositiva, ruta, x, y, ancho_max, alto_max):
    """Encaja la imagen dentro del rectángulo dado, centrada y sin deformarla."""
    from PIL import Image as Pil
    with Pil.open(ruta) as im:
        proporcion = im.height / im.width
    ancho = ancho_max
    alto = ancho * proporcion
    if alto > alto_max:
        alto = alto_max
        ancho = alto / proporcion
    return imagen(diapositiva, ruta, x + (ancho_max - ancho) / 2,
                  y + (alto_max - alto) / 2, ancho=ancho)


def tabla(diapositiva, encabezados, filas, x, y, ancho, alto, anchos=None,
          tamano=SECUNDARIO):
    """Tabla con el encabezado en el azul de la plantilla y el cuerpo en blanco."""
    forma = diapositiva.shapes.add_table(len(filas) + 1, len(encabezados),
                                         Inches(x), Inches(y), Inches(ancho), Inches(alto))
    t = forma.table
    if anchos:
        for indice, medida in enumerate(anchos):
            t.columns[indice].width = Inches(medida)

    # Sin esto la tabla toma el estilo del tema de PowerPoint, que es verde y no
    # tiene nada que ver con los colores de la plantilla del centro de formación.
    for columna, texto in enumerate(encabezados):
        celda = t.cell(0, columna)
        celda.text = str(texto)
        _formato_celda(celda, tamano, blanco=True, negrita=True)
        _pintar(celda, AZUL)
    for fila, datos in enumerate(filas, start=1):
        for columna, texto in enumerate(datos):
            celda = t.cell(fila, columna)
            celda.text = "" if texto is None else str(texto)
            _formato_celda(celda, tamano)
            _pintar(celda, FILA_CLARA if fila % 2 else FILA_ALTERNA)
    return forma


def _pintar(celda, color):
    celda.fill.solid()
    celda.fill.fore_color.rgb = color


def _formato_celda(celda, tamano, blanco=False, negrita=False):
    celda.margin_left = Inches(0.08)
    celda.margin_right = Inches(0.08)
    celda.margin_top = Inches(0.03)
    celda.margin_bottom = Inches(0.03)
    for parrafo_celda in celda.text_frame.paragraphs:
        for run in parrafo_celda.runs:
            run.font.size = tamano
            run.font.bold = negrita
            run.font.name = FUENTE
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if blanco else TINTA


def pie(diapositiva, texto, x=0.62, y=6.85, ancho=11.0):
    """Línea de fuente o aclaración, en letra menor y gris."""
    return _cuadro(diapositiva, texto, x, y, ancho, 0.35, PIE, GRIS)


def numerar(presentacion, desde=3):
    """Escribe el número en cada diapositiva, salvo en las de portada.

    La plantilla no trae numeración, y sin ella nadie puede referirse a una
    diapositiva durante las preguntas del jurado.
    """
    total = len(presentacion.slides)
    for indice, diapositiva in enumerate(presentacion.slides, start=1):
        if indice < desde:
            continue
        # Pegado al borde inferior, porque a media pulgada más arriba se cruzaba con
        # las tablas que ocupan casi toda la diapositiva.
        _cuadro(diapositiva, f"{indice} / {total}", 11.9, 7.06, 1.2, 0.28,
                PIE, GRIS, alineacion=PP_ALIGN.RIGHT)


def guardar(presentacion, ruta=DESTINO):
    """Guarda, cerrando PowerPoint si dejó el archivo bloqueado.

    Convertir a PDF deja a veces una instancia abierta que retiene el archivo, y el
    guardado siguiente falla con un error de permisos que no tiene nada que ver con
    permisos. Antes que hacer que quien ejecuta esto lo adivine, se cierra y se
    reintenta una vez.
    """
    try:
        presentacion.save(str(ruta))
    except PermissionError:
        subprocess.run(["taskkill", "/F", "/IM", "POWERPNT.EXE"],
                       capture_output=True, check=False)
        time.sleep(1.0)
        presentacion.save(str(ruta))
    return ruta


def duplicar(presentacion, indice, posicion=None):
    """Copia una diapositiva completa, con su fondo y su decoración.

    Hace falta porque la plantilla no trae diapositiva de referencias y python-pptx
    no sabe duplicar. Se copia el XML de cada forma y se rehacen las relaciones,
    porque una imagen copiada apunta al identificador de relación de la diapositiva
    original y sin reasignarlo la imagen no aparece.
    """
    origen = presentacion.slides[indice]
    nueva = presentacion.slides.add_slide(origen.slide_layout)
    for forma in list(nueva.shapes):
        forma._element.getparent().remove(forma._element)

    equivalencias = {}
    for rid, relacion in origen.part.rels.items():
        # El layout ya lo puso `add_slide`, y la hoja de notas pertenece a una sola
        # diapositiva: si dos apuntan a la misma, PowerPoint no abre el archivo.
        if relacion.reltype.endswith(("slideLayout", "notesSlide")):
            continue
        if relacion.is_external:
            nuevo = nueva.part.relate_to(relacion.target_ref, relacion.reltype,
                                         is_external=True)
        else:
            nuevo = nueva.part.relate_to(relacion.target_part, relacion.reltype)
        equivalencias[rid] = nuevo

    for forma in origen.shapes:
        elemento = copy.deepcopy(forma._element)
        for nodo in elemento.iter():
            for atributo, valor in list(nodo.attrib.items()):
                if atributo.endswith("}id") or atributo.endswith("}embed"):
                    if valor in equivalencias:
                        nodo.set(atributo, equivalencias[valor])
        nueva.shapes._spTree.append(elemento)

    if posicion is not None:
        mover(presentacion, len(presentacion.slides) - 1, posicion)
    return nueva


def mover(presentacion, desde, hasta):
    """Cambia una diapositiva de sitio dentro de la presentación."""
    listado = presentacion.slides._sldIdLst
    diapositivas = list(listado)
    listado.remove(diapositivas[desde])
    listado.insert(hasta, diapositivas[desde])
