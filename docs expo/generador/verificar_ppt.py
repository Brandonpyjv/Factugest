"""
Revisión final de la presentación.

Comprueba sobre el `.pptx` lo que se acordó con el cliente y lo que hace que una
diapositiva se lea proyectada. Se ejecuta después de regenerar.

    python verificar_ppt.py
"""
import re
import sys
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu, Inches, Pt

EXPOSICION = Path(__file__).resolve().parent.parent / "carpeta exposicion"
ARCHIVO = EXPOSICION / "FactuGest - Sustentación.pptx"

MINIMO_CUERPO = 13      # el pie y la numeración van a 13, el cuerpo desde 15
# Con ideas completas y de corrido, tres viñetas ya suman noventa palabras. El tope
# alto es deliberado: la alternativa sería volver a las frases telegráficas.
MAXIMO_PALABRAS = 120
LIENZO_ANCHO = Inches(13.333)
LIENZO_ALTO = Inches(7.5)


def _texto_de(diapositiva, con_tablas=True):
    """El texto de la diapositiva. Las tablas se pueden dejar fuera del conteo.

    A una tabla no se le aplica el límite de palabras, porque nadie la lee entera:
    quien la mira busca su fila. El límite es para la prosa, que sí se lee de
    corrido y es la que satura una diapositiva.
    """
    partes = []
    for forma in diapositiva.shapes:
        if forma.has_text_frame:
            partes.append(forma.text_frame.text)
        if forma.has_table and con_tablas:
            for fila in forma.table.rows:
                for celda in fila.cells:
                    partes.append(celda.text)
    return " ".join(partes)


def _tamanos(diapositiva):
    salida = []
    marcos = [f.text_frame for f in diapositiva.shapes if f.has_text_frame]
    for forma in diapositiva.shapes:
        if forma.has_table:
            marcos += [c.text_frame for f in forma.table.rows for c in f.cells]
    for marco in marcos:
        for parrafo in marco.paragraphs:
            for run in parrafo.runs:
                if run.font.size and run.text.strip():
                    salida.append((round(run.font.size.pt), run.text.strip()[:38]))
    return salida


def revisar():
    presentacion = Presentation(ARCHIVO)
    fallas = []
    total = len(presentacion.slides)
    print(f"{ARCHIVO.name} · {total} diapositivas\n")

    pequenas, largas, desbordes, vacias, sin_numero = [], [], [], [], []
    guiones, puntos, dos_puntos = [], [], []

    for numero, diapositiva in enumerate(presentacion.slides, start=1):
        texto = _texto_de(diapositiva)

        for tamano, muestra in _tamanos(diapositiva):
            if tamano < MINIMO_CUERPO:
                pequenas.append((numero, tamano, muestra))

        palabras = len(_texto_de(diapositiva, con_tablas=False).split())
        if palabras > MAXIMO_PALABRAS:
            largas.append((numero, palabras))
        if palabras < 3 and not any(f.shape_type == 13 for f in diapositiva.shapes):
            vacias.append(numero)

        for forma in diapositiva.shapes:
            if forma.left is None or forma.width is None:
                continue
            derecha = forma.left + forma.width
            abajo = (forma.top or 0) + (forma.height or 0)
            # La decoración de la plantilla sangra a propósito por los bordes, así que
            # a las imágenes se les tolera; al texto no.
            margen = Inches(0.5) if forma.shape_type == 13 else Inches(0.05)
            if derecha > LIENZO_ANCHO + margen or abajo > LIENZO_ALTO + margen:
                desbordes.append(numero)

        if "—" in texto:
            guiones.append(numero)
        if "·" in texto:
            puntos.append(numero)
        sospechoso = [m for m in re.findall(r"\w{4,}: [a-záéíóúñ]\w+", texto)
                      if not m.startswith(("Fuente", "Preguntas", "Nota"))]
        if sospechoso:
            dos_puntos.append((numero, sospechoso[:2]))

        if numero >= 3 and not re.search(rf"\b{numero} / {total}\b", texto):
            sin_numero.append(numero)

    def informe(titulo, problemas, detalle=""):
        if problemas:
            fallas.append(titulo)
            print(f"  [FALLA] {titulo} — {problemas[:6]}{detalle}")
        else:
            print(f"  [OK]    {titulo}")

    informe(f"Letra de al menos {MINIMO_CUERPO} puntos", pequenas)
    informe(f"Menos de {MAXIMO_PALABRAS} palabras de prosa por diapositiva", largas)
    informe("Sin diapositivas vacías", vacias)
    informe("Todo dentro del lienzo", sorted(set(desbordes)))
    informe("Sin guion largo", guiones)
    informe("Sin punto medio", puntos)
    informe("Sin «afirmación breve: explicación»", dos_puntos)
    informe("Numeración en todas salvo las portadas", sin_numero)

    print(f"\n{'Todo en orden.' if not fallas else f'{len(fallas)} comprobaciones fallaron.'}")
    return len(fallas)


if __name__ == "__main__":
    sys.exit(1 if revisar() else 0)
