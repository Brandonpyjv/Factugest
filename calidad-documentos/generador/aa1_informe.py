"""
AA1-EV01 — Informe de métodos y estándar de calidad. Ensamblador.

Mismo reparto que el documento de grado: cada capítulo vive en su módulo y expone
`escribir(d)`. Aquí solo se declara el orden, de modo que una sesión toque un
archivo y el ensamble sea esta lista.

Los módulos que todavía no existen se saltan y se avisan al final. Es a propósito:
así el informe se puede generar y revisar desde el primer capítulo, en vez de tener
que esperar a que estén los nueve para ver si el formato salió bien.

    python aa1_informe.py
"""
import importlib

from comun import guardar, nuevo_documento

ARCHIVO = "FactuGest - Informe de metodos y estandar de calidad.docx"

TITULO = "INFORME DE MÉTODOS Y ESTÁNDARES DE CALIDAD DEL SOFTWARE"
SUBTITULO = ("Marco de calidad adoptado y plan de pruebas de FactuGest, plataforma web de "
             "facturación electrónica para la emisión de documentos por cuenta de terceros")
EVIDENCIA = "Evidencia AA1-EV01"

# El orden de esta lista es el orden del informe.
CAPITULOS = [
    "aa1_cap1_marco",        # C3: qué es calidad, modelos y estándares, producto y proceso
    "aa1_cap2_adopcion",     # C4: estándar seleccionado y matriz ISO/IEC 25010
    "aa1_cap3_plan",         # C5: plan de pruebas
    "aa1_cap4_ejecutadas",   # C6: pruebas ejecutadas, con sus casos y resultados
    "aa1_cap5_planificadas", # C7: pruebas planificadas, resultados y conclusiones
    "aa1_cierre",            # C8: referencias y anexos
]


def _indice_de_dos_niveles(d):
    """Deja en el índice los capítulos y sus secciones, sin las subsecciones.

    Con los tres niveles el índice pasaba de una página, y el párrafo que Word deja
    al cerrar el campo se llevaba una hoja entera en blanco por delante del primer
    capítulo. Además, un índice de dos páginas para un informe de cuarenta deja de
    servir para lo que sirve un índice. Las subsecciones siguen numeradas en el
    cuerpo, que es donde se buscan.
    """
    for parrafo in d.doc.paragraphs:
        if "TOC" not in parrafo._p.xml:
            continue
        parrafo.paragraph_format.line_spacing = 1.0
        for instruccion in parrafo._p.iter():
            if instruccion.text and "TOC" in instruccion.text:
                instruccion.text = instruccion.text.replace('"1-3"', '"1-2"')


def construir():
    d = nuevo_documento(TITULO, SUBTITULO, EVIDENCIA)
    d.tabla_contenido()
    _indice_de_dos_niveles(d)

    escritos, pendientes = [], []
    for nombre in CAPITULOS:
        try:
            modulo = importlib.import_module(nombre)
        except ModuleNotFoundError:
            pendientes.append(nombre)
            continue
        modulo.escribir(d)
        escritos.append(nombre)

    ruta = guardar(d, ARCHIVO)
    return d, ruta, escritos, pendientes


if __name__ == "__main__":
    documento, salida, hechos, faltan = construir()
    print(f"Generado: {salida}")
    print(f"Capítulos escritos: {len(hechos)} de {len(CAPITULOS)}")
    print(f"Tablas: {documento.n_tabla}, figuras: {documento.n_figura}")
    if faltan:
        print("Pendientes: " + ", ".join(faltan))
