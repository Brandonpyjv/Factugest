"""
Motor de formato APA 7 para los entregables del documento de grado de FactuGest.

Todo lo que el `InstructivoSBS.APA-1` exige está aplicado aquí y en ningún otro
lugar: márgenes, interlineado, sangría, paginación, niveles de título y la forma
de las tablas y las figuras. Los generadores de cada documento escriben contenido
y no tocan formato.

**Por qué un motor y no formato a mano.** El documento se escribe por capítulos,
en sesiones distintas, y al final se ensambla. Si cada capítulo aplicara su propio
formato, el ensamble traería tres interlineados y dos tipografías, y corregir eso
sobre ochenta páginas cuesta más que escribirlas. Aquí el formato se decide una
vez y se hereda.

**Las tablas y las figuras se numeran solas.** El contador vive en el documento,
no en quien escribe: intercalar una figura nueva en el capítulo 3 no obliga a
renumerar a mano las treinta que vienen después. Al ensamblar (T16) los contadores
se arrastran de un capítulo al siguiente con `continuar_desde()`.
"""
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.image.image import Image
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Emu, Inches, Pt, RGBColor

# --- Constantes del instructivo -------------------------------------------------

FUENTE = "Times New Roman"
TAMANO = Pt(12)
TAMANO_TABLA = Pt(10)
MARGEN = Cm(2.54)
SANGRIA = Cm(1.27)
INTERLINEADO = 2.0          # doble
NEGRO = RGBColor(0, 0, 0)

# Carta (8,5" x 11") menos 2,54 cm por lado: lo que puede ocupar una figura.
ANCHO_UTIL = Inches(8.5 - 2 * 1.0)


# --- Utilidades de bajo nivel (XML de Word) ------------------------------------

def _campo(parrafo, instruccion):
    """Inserta un campo de Word (PAGE, TOC...) que Word recalcula al abrir."""
    run = parrafo.add_run()
    inicio = OxmlElement("w:fldChar")
    inicio.set(qn("w:fldCharType"), "begin")
    texto = OxmlElement("w:instrText")
    texto.set(qn("xml:space"), "preserve")
    texto.text = instruccion
    separador = OxmlElement("w:fldChar")
    separador.set(qn("w:fldCharType"), "separate")
    marcador = OxmlElement("w:t")
    marcador.text = " "
    fin = OxmlElement("w:fldChar")
    fin.set(qn("w:fldCharType"), "end")
    for nodo in (inicio, texto, separador, marcador, fin):
        run._r.append(nodo)
    return run


def _borde(elemento, lado, valor="single", medida=6):
    """Pone o quita un borde. `valor='nil'` lo quita."""
    borde = OxmlElement(f"w:{lado}")
    borde.set(qn("w:val"), valor)
    if valor != "nil":
        borde.set(qn("w:sz"), str(medida))
        borde.set(qn("w:space"), "0")
        borde.set(qn("w:color"), "000000")
    elemento.append(borde)


def _bordes_tabla(tabla):
    """Las tres líneas horizontales del instructivo: superior, inferior y la del encabezado.

    APA no usa cuadrícula. Una tabla con todas sus líneas se lee como una hoja de
    cálculo pegada; sin ellas, los datos se leen como datos.
    """
    propiedades = tabla._tbl.tblPr
    marco = OxmlElement("w:tblBorders")
    _borde(marco, "top")
    _borde(marco, "bottom")
    for lado in ("left", "right", "insideH", "insideV"):
        _borde(marco, lado, "nil")
    propiedades.append(marco)

    for celda in tabla.rows[0].cells:          # la línea bajo el encabezado
        propiedades_celda = celda._tc.get_or_add_tcPr()
        marco_celda = OxmlElement("w:tcBorders")
        _borde(marco_celda, "bottom")
        propiedades_celda.append(marco_celda)


def _repetir_encabezado(tabla):
    """Repite la fila de títulos en cada página que la tabla ocupe.

    Una tabla de ochenta requisitos cruza cinco páginas, y a partir de la segunda
    las columnas quedan sin rótulo: quien la lee tiene que devolverse a la primera
    para saber cuál es el actor y cuál la prioridad.
    """
    propiedades = tabla.rows[0]._tr.get_or_add_trPr()
    encabezado = OxmlElement("w:tblHeader")
    encabezado.set(qn("w:val"), "true")
    propiedades.append(encabezado)


def _filas_enteras(tabla):
    """Impide que una fila se parta entre dos páginas.

    Sin esto, un requisito puede quedar con su código al pie de una página y su
    descripción al comienzo de la siguiente, o dejar un renglón suelto bajo la línea
    de cierre de la tabla.
    """
    for fila in tabla.rows:
        propiedades = fila._tr.get_or_add_trPr()
        entera = OxmlElement("w:cantSplit")
        entera.set(qn("w:val"), "true")
        propiedades.append(entera)


def _anchos_fijos(tabla, anchos_cm):
    """Fija el ancho de cada columna, en centímetros.

    Word ignora los anchos mientras la tabla esté en ajuste automático, así que hay
    que declarar el diseño fijo y repetir el ancho en **todas** las celdas de la
    columna: el ancho vive en la celda, no en la columna.
    """
    disposicion = OxmlElement("w:tblLayout")
    disposicion.set(qn("w:type"), "fixed")
    tabla._tbl.tblPr.append(disposicion)

    for indice, centimetros in enumerate(anchos_cm):
        for fila in tabla.rows:
            fila.cells[indice].width = Cm(centimetros)


def _quitar_fuente_del_tema(estilo):
    """Desata un estilo de la fuente del tema de Word y lo fija en la del documento.

    Los estilos de título traen `asciiTheme="majorHAnsi"`, que apunta a la fuente de
    títulos del tema —Calibri Light en la plantilla de Word—. Ese atributo tiene
    prioridad sobre el nombre de fuente, así que pedir Times New Roman no basta:
    hasta que no se quita, los títulos salen en otra tipografía distinta del cuerpo.
    """
    fuentes = estilo.element.rPr.rFonts
    for atributo in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        fuentes.attrib.pop(qn(f"w:{atributo}"), None)
    for atributo in ("ascii", "hAnsi", "eastAsia", "cs"):
        fuentes.set(qn(f"w:{atributo}"), FUENTE)


def inicial_minuscula(texto):
    """Baja solo la primera letra de un nombre propio de módulo o de caso.

    `lower()` sobre la cadena completa destruye las siglas: «Integración mediante
    API REST» quedaría como «integración mediante api rest» en el título de la
    tabla, y ese título es lo que después aparece en el índice de tablas.
    """
    return texto[0].lower() + texto[1:] if texto else texto


def _sin_espacio_extra(formato):
    formato.space_before = Pt(0)
    formato.space_after = Pt(0)


# --- El documento ---------------------------------------------------------------

class DocumentoAPA:
    """Un documento en Word con el formato del instructivo ya puesto."""

    def __init__(self):
        self.doc = Document()
        self.n_tabla = 0
        self.n_figura = 0
        self._salto_pendiente = False
        self._configurar_pagina()
        self._configurar_estilos()
        self._numerar_paginas()

    # -- configuración inicial --

    def _configurar_pagina(self):
        for seccion in self.doc.sections:
            self._margenes(seccion)

    @staticmethod
    def _margenes(seccion):
        seccion.top_margin = MARGEN
        seccion.bottom_margin = MARGEN
        seccion.left_margin = MARGEN
        seccion.right_margin = MARGEN

    def _configurar_estilos(self):
        normal = self.doc.styles["Normal"]
        normal.font.name = FUENTE
        normal.font.size = TAMANO
        normal.font.color.rgb = NEGRO
        _quitar_fuente_del_tema(normal)

        formato = normal.paragraph_format
        formato.line_spacing = INTERLINEADO
        formato.alignment = WD_ALIGN_PARAGRAPH.LEFT
        _sin_espacio_extra(formato)

        self._configurar_titulos()

    def _configurar_titulos(self):
        """Reviste los estilos de título de Word con la apariencia del instructivo.

        Se reutilizan los estilos `Heading 1..3` en vez de dar formato suelto a cada
        párrafo porque son los que el campo TOC reconoce: con formato suelto la tabla
        de contenido sale con el mensaje de que no encontró entradas. Word los trae
        en azul y con otra tipografía, así que se reescriben enteros: centrado y
        negrita el 1, izquierda y negrita el 2, negrita cursiva el 3, todos en Times
        New Roman de 12 puntos y en negro.
        """
        apariencia = {
            1: (WD_ALIGN_PARAGRAPH.CENTER, False),
            2: (WD_ALIGN_PARAGRAPH.LEFT, False),
            3: (WD_ALIGN_PARAGRAPH.LEFT, True),
        }
        for nivel, (alineacion, cursiva) in apariencia.items():
            estilo = self.doc.styles[f"Heading {nivel}"]
            estilo.base_style = self.doc.styles["Normal"]
            estilo.font.name = FUENTE
            estilo.font.size = TAMANO
            estilo.font.bold = True
            estilo.font.italic = cursiva
            estilo.font.color.rgb = NEGRO
            _quitar_fuente_del_tema(estilo)

            formato = estilo.paragraph_format
            formato.alignment = alineacion
            formato.line_spacing = INTERLINEADO
            formato.first_line_indent = Cm(0)
            formato.keep_with_next = True          # que no quede solo al pie
            _sin_espacio_extra(formato)

    def _numerar_paginas(self):
        """Arábigos en la esquina superior derecha, desde la portada.

        Solo se escribe en la primera sección. Las que se agreguen después nacen
        encadenadas a ella y heredan el encabezado, de modo que la numeración sigue
        corrida al cambiar a una página apaisada. Escribirlo otra vez en cada
        sección no crearía un encabezado nuevo: agregaría un segundo campo al mismo,
        y el número saldría dos veces en todo el documento.
        """
        seccion = self.doc.sections[0]
        seccion.header.is_linked_to_previous = False
        parrafo = seccion.header.paragraphs[0]
        parrafo.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        parrafo.paragraph_format.line_spacing = 1.0
        _campo(parrafo, "PAGE")
        for run in parrafo.runs:
            run.font.name = FUENTE
            run.font.size = TAMANO

    def continuar_desde(self, n_tabla=0, n_figura=0):
        """Arranca los contadores donde los dejó el capítulo anterior (ensamble T16)."""
        self.n_tabla = n_tabla
        self.n_figura = n_figura

    # -- texto --

    def parrafo(self, texto="", sangria=True, alineacion=None, cursiva=False,
                negrita=False, interlineado=INTERLINEADO):
        p = self.doc.add_paragraph()
        formato = p.paragraph_format
        formato.line_spacing = interlineado
        formato.alignment = alineacion or WD_ALIGN_PARAGRAPH.LEFT
        formato.first_line_indent = SANGRIA if sangria else Cm(0)
        _sin_espacio_extra(formato)
        self._aplicar_salto(p)
        if texto:
            run = p.add_run(texto)
            run.italic = cursiva
            run.bold = negrita
        return p

    def titulo(self, texto, nivel=1, nueva_pagina=False, en_indice=True):
        """Niveles 1 a 3 del instructivo.

        1: centrado y en negrita. 2: a la izquierda, en negrita. 3: a la izquierda,
        negrita cursiva y con punto final. Se mantiene el tamaño del cuerpo: APA no
        agranda los títulos, los distingue por peso y posición.

        `en_indice=False` da el mismo aspecto sin usar el estilo de título, para lo
        que no debe aparecer en la tabla de contenido —empezando por el rótulo de la
        tabla de contenido misma—.
        """
        if nueva_pagina:
            self.salto_pagina()
        if nivel == 3 and not texto.rstrip().endswith("."):
            texto = texto.rstrip() + "."

        alineacion = WD_ALIGN_PARAGRAPH.CENTER if nivel == 1 else WD_ALIGN_PARAGRAPH.LEFT
        if not en_indice:
            return self.parrafo(texto, sangria=False, alineacion=alineacion,
                                negrita=True, cursiva=(nivel == 3))

        p = self.doc.add_paragraph(texto, style=f"Heading {min(nivel, 3)}")
        self._aplicar_salto(p)
        return p

    def vinetas(self, elementos, sangria=True):
        """Lista con viñetas.

        Un elemento puede ser un texto o un par `(término, definición)`; en ese caso
        el término va en negrita, que es como se lee un glosario: la vista salta de
        término en término sin tener que leer cada definición para encontrar el que
        busca.
        """
        for elemento in elementos:
            p = self.doc.add_paragraph(style="List Bullet")
            formato = p.paragraph_format
            formato.line_spacing = INTERLINEADO
            formato.left_indent = SANGRIA if sangria else Cm(0)
            _sin_espacio_extra(formato)
            partes = elemento if isinstance(elemento, tuple) else (elemento,)
            for indice, parte in enumerate(partes):
                run = p.add_run(f"{parte}: " if indice == 0 and len(partes) > 1 else parte)
                run.bold = (indice == 0 and len(partes) > 1)
                run.font.name = FUENTE
                run.font.size = TAMANO
        return self

    def numerada(self, elementos):
        for elemento in elementos:
            p = self.doc.add_paragraph(style="List Number")
            formato = p.paragraph_format
            formato.line_spacing = INTERLINEADO
            formato.left_indent = SANGRIA
            _sin_espacio_extra(formato)
            run = p.add_run(elemento)
            run.font.name = FUENTE
            run.font.size = TAMANO
        return self

    def cita_larga(self, texto, fuente=None):
        """Cita de más de 40 palabras: bloque con sangría de 1,27 cm y sin comillas."""
        cuerpo = texto if not fuente else f"{texto} ({fuente})"
        p = self.parrafo(cuerpo, sangria=False)
        p.paragraph_format.left_indent = SANGRIA
        return p

    def salto_pagina(self):
        """Manda lo siguiente a una página nueva.

        No inserta un párrafo con un salto dentro: ese párrafo ocupa un renglón, y
        cuando el texto anterior termina justo al final de la página, el renglón cae
        en la siguiente y el salto empuja el contenido una más allá, dejando una
        página en blanco. En vez de eso se anota la intención y la marca la recibe el
        primer párrafo que se escriba después, que es lo que Word entiende como
        «empezar en página nueva».
        """
        self._salto_pendiente = True

    def _aplicar_salto(self, parrafo):
        if self._salto_pendiente:
            parrafo.paragraph_format.page_break_before = True
            self._salto_pendiente = False

    # -- tablas y figuras --

    def tabla(self, nombre, encabezados, filas, nota=None, anchos=None):
        """Tabla con el rótulo `Tabla N` encima y su nombre en cursiva debajo.

        `anchos` es una lista de anchos por columna, en centímetros. Vale la pena
        darlos siempre que una columna lleve texto largo: repartido en partes
        iguales, el ancho sobra en la columna del código y falta en la de la
        descripción, que termina cayendo en una columna de dos palabras por línea.
        El ancho útil de la página es de 16,5 cm.
        """
        self.n_tabla += 1

        rotulo = self.parrafo(sangria=False)
        rotulo.add_run(f"Tabla {self.n_tabla}").bold = True
        self.parrafo(nombre, sangria=False, cursiva=True)

        t = self.doc.add_table(rows=1, cols=len(encabezados))
        t.style = "Table Grid"          # base; los bordes se reemplazan enseguida
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = anchos is None

        for celda, titulo in zip(t.rows[0].cells, encabezados):
            self._escribir_celda(celda, titulo, negrita=True)
        for fila in filas:
            celdas = t.add_row().cells
            for celda, valor in zip(celdas, fila):
                self._escribir_celda(celda, "" if valor is None else str(valor))

        _bordes_tabla(t)
        _repetir_encabezado(t)
        _filas_enteras(t)
        if anchos:
            _anchos_fijos(t, anchos)

        if nota:
            p = self.parrafo(sangria=False, interlineado=1.0)
            p.add_run("Nota. ").italic = True
            run = p.add_run(nota)
            run.font.size = TAMANO_TABLA
            p.runs[0].font.size = TAMANO_TABLA
        self.parrafo()
        return t

    def _escribir_celda(self, celda, texto, negrita=False):
        """Escribe una celda. Los saltos de línea del texto se respetan.

        Hacen falta para las fichas de casos de uso: los pasos de una secuencia van
        uno por renglón dentro de la misma celda, y sin esto quedarían todos
        seguidos en un párrafo corrido.
        """
        p = celda.paragraphs[0]
        formato = p.paragraph_format
        formato.line_spacing = 1.0
        _sin_espacio_extra(formato)
        for indice, linea in enumerate(str(texto).split("\n")):
            run = p.add_run()
            if indice:
                run.add_break()
            run.add_text(linea)
            run.font.name = FUENTE
            run.font.size = TAMANO_TABLA
            run.bold = negrita

    def figura(self, titulo, ruta, nota=None, ancho=None):
        """Figura con el rótulo `Figura N` encima, el título en cursiva y su nota.

        La imagen se reduce si no cabe entre márgenes; nunca se agranda, porque
        estirar una captura de pantalla solo la vuelve borrosa.
        """
        self.n_figura += 1

        rotulo = self.parrafo(sangria=False)
        rotulo.add_run(f"Figura {self.n_figura}").bold = True
        self.parrafo(titulo, sangria=False, cursiva=True)

        p = self.parrafo(sangria=False, alineacion=WD_ALIGN_PARAGRAPH.CENTER)
        p.add_run().add_picture(str(ruta), width=ancho or self._ancho_de(ruta))

        if nota:
            p = self.parrafo(sangria=False, interlineado=1.0)
            p.add_run("Nota. ").italic = True
            run = p.add_run(nota)
            run.font.size = TAMANO_TABLA
            p.runs[0].font.size = TAMANO_TABLA
        self.parrafo()

    @staticmethod
    def _ancho_de(ruta):
        imagen = Image.from_file(str(ruta))
        natural = Inches(imagen.px_width / (imagen.horz_dpi or 96))
        return min(natural, ANCHO_UTIL)

    # -- piezas del documento --

    def portada(self, titulo, subtitulo, integrantes, grado, institucion, ciudad, anio):
        """Portada centrada, sin sangría y sin numeración visible distinta."""
        def centrado(texto, negrita=False, cursiva=False):
            self.parrafo(texto, sangria=False, alineacion=WD_ALIGN_PARAGRAPH.CENTER,
                         negrita=negrita, cursiva=cursiva)

        centrado(titulo, negrita=True)
        if subtitulo:
            centrado(subtitulo)
        self.parrafo()
        centrado("Presentado por:")
        for integrante in integrantes:
            centrado(integrante)
        self.parrafo()
        centrado(grado)
        self.parrafo()
        for linea in institucion:
            centrado(linea)
        self.parrafo()
        centrado(ciudad)
        centrado(str(anio))
        self.salto_pagina()

    def tabla_contenido(self, titulo="Tabla de contenido"):
        """Índice automático de Word.

        Se inserta como campo, no como lista escrita a mano: la paginación real solo
        se conoce cuando Word arma las páginas, así que un índice escrito a mano
        estaría mal desde el primer cambio. Word lo llena al abrir el archivo (o con
        clic derecho › Actualizar campos).
        """
        self.titulo(titulo, nivel=1, en_indice=False)
        p = self.parrafo(sangria=False)
        _campo(p, r'TOC \o "1-3" \h \z \u')
        self.salto_pagina()

    def seccion_horizontal(self):
        """Abre una sección apaisada y devuelve el ancho útil que queda.

        El modelo físico de la base tiene veintisiete tablas: reducido al ancho de
        una página vertical, los nombres de las columnas dejan de leerse, y un
        diagrama que no se lee no es evidencia de nada. Al terminar la figura se
        llama a `seccion_vertical()` para que el resto del documento siga como venía.
        """
        seccion = self.doc.add_section(WD_SECTION.NEW_PAGE)
        seccion.orientation = 1                       # WD_ORIENT.LANDSCAPE
        seccion.page_width, seccion.page_height = seccion.page_height, seccion.page_width
        self._margenes(seccion)
        return Emu(seccion.page_width - 2 * MARGEN)

    def seccion_vertical(self):
        seccion = self.doc.add_section(WD_SECTION.NEW_PAGE)
        seccion.orientation = 0                       # WD_ORIENT.PORTRAIT
        if seccion.page_width > seccion.page_height:
            seccion.page_width, seccion.page_height = seccion.page_height, seccion.page_width
        self._margenes(seccion)
        return seccion

    def guardar(self, ruta):
        self.doc.save(str(ruta))
        return ruta
