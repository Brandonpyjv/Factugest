"""
El distintivo que usa una empresa que no ha cargado un logo.

Casi ningún negocio pequeño tiene un archivo de logo a mano, y pedirle uno para
poder facturar sería poner un trámite delante de un documento fiscal. Así que
cuando no hay logo se dibuja un monograma: las dos iniciales del nombre sobre el
color de la empresa, como el distintivo de un contacto.

Tres decisiones:

**No se guarda como archivo.** Se dibuja al momento, en el PDF y en la pantalla.
Un archivo generado habría que regenerarlo cada vez que cambien el nombre o el
color, y el día que no se regenere quedará un monograma que dice algo distinto de
lo que dice el membrete.

**El color no es aleatorio: es el de la empresa.** Cada emisor ya tiene
`color_marca` para el documento, así que el monograma sale del mismo sitio y el
resultado se ve pensado en vez de improvisado. Y si no tiene color, se deriva del
nombre —siempre el mismo para el mismo nombre—, no al azar: un distintivo que
cambia de color cada vez que se abre la factura no es un distintivo.

**Un logo cargado siempre manda.** Esto es lo que se usa mientras no lo haya.
"""
import unicodedata

# Palabras que no aportan iniciales: la forma jurídica y los conectores. Sin esto
# «Droguería La Salud S.A.S.» daría «DL», que no identifica nada.
_IGNORADAS = {
    "sas", "sa", "ltda", "eu", "sca", "scs", "spa", "inc", "cia", "compania",
    "de", "del", "la", "las", "el", "los", "y", "e", "en", "para", "por",
}

# Colores legibles con texto blanco encima, para cuando la empresa no eligió el
# suyo. Se escoge por el nombre, no al azar.
_PALETA = ["#334155", "#7a1f1f", "#1f5b4e", "#5b3a7a", "#8a5a12",
           "#1f4f7a", "#6b2d4f", "#3f6b1f"]


def _sin_tildes(texto: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", texto)
                   if unicodedata.category(c) != "Mn")


def iniciales(nombre: str) -> str:
    """Las dos primeras letras significativas del nombre.

        «Droguería La Salud S.A.S.»    → DS
        «Siste Soluciones S.A.S.»      → SS
        «Transportes del Norte S.A.S.» → TN
        «FactuGest S.A.S.»             → FG   (una sola palabra: dos letras de ella)
    """
    limpio = _sin_tildes(str(nombre or "")).replace(".", " ").replace(",", " ")
    # Se descartan las letras sueltas: al partir los puntos, «S.A.S.» se convierte
    # en tres palabras de una letra y «FactuGest S.A.S.» daría «FS» en vez de «FG».
    palabras = [p for p in limpio.split()
                if len(p) > 1 and p.lower() not in _IGNORADAS
                and any(c.isalpha() for c in p)]

    if not palabras:
        return "?"
    if len(palabras) == 1:
        # Un nombre de una sola palabra da sus dos primeras letras: «FactuGest» → FG.
        # Si viene en camello, se aprovechan las dos mayúsculas: «FactuGest» → FG.
        palabra = palabras[0]
        mayusculas = [c for c in palabra if c.isupper()]
        if len(mayusculas) >= 2:
            return (mayusculas[0] + mayusculas[1]).upper()
        return palabra[:2].upper()

    return (palabras[0][0] + palabras[1][0]).upper()


def color(nombre: str, color_marca: str = None) -> str:
    """El color del monograma: el de la empresa, o uno estable derivado del nombre."""
    elegido = str(color_marca or "").strip().lower()
    if len(elegido) == 7 and elegido.startswith("#"):
        return elegido

    # Suma de los códigos del nombre: el mismo nombre da siempre el mismo color.
    semilla = sum(ord(c) for c in _sin_tildes(str(nombre or "")).upper())
    return _PALETA[semilla % len(_PALETA)]
