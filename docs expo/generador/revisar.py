"""
Convierte un .docx a PDF con Word y lo renderiza a imágenes, para revisar cómo
quedó de verdad y no como uno cree que quedó.

Hace falta porque los campos de Word —la paginación y la tabla de contenido— no
tienen valor hasta que Word abre el archivo: leer el .docx con python-docx muestra
el campo, no el número. Esto abre el documento, actualiza los campos, exporta a PDF
y saca un PNG por página.

    python revisar.py ../entregables/archivo.docx          # todas las páginas
    python revisar.py ../entregables/archivo.docx 1 2 3    # solo esas
"""
import sys
from pathlib import Path

import pymupdf
import win32com.client

WD_FORMATO_PDF = 17


def a_pdf(ruta_docx):
    """Abre en Word, actualiza los campos y exporta. Devuelve la ruta del PDF."""
    ruta_docx = Path(ruta_docx).resolve()
    ruta_pdf = ruta_docx.with_suffix(".pdf")

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        documento = word.Documents.Open(str(ruta_docx))
        # Dos veces: la primera arma el índice, la segunda corrige la paginación
        # que el propio índice desplazó al crecer.
        for _ in range(2):
            documento.Fields.Update()
            for tabla in documento.TablesOfContents:
                tabla.Update()
        documento.SaveAs(str(ruta_pdf), FileFormat=WD_FORMATO_PDF)
        paginas = documento.ComputeStatistics(2)      # wdStatisticPages
        documento.Close(SaveChanges=False)
    finally:
        word.Quit()
    return ruta_pdf, paginas


def a_imagenes(ruta_pdf, paginas=None, escala=1.6):
    pdf = pymupdf.open(ruta_pdf)
    salida = []
    indices = [p - 1 for p in paginas] if paginas else range(pdf.page_count)
    for indice in indices:
        if indice >= pdf.page_count:
            continue
        imagen = pdf[indice].get_pixmap(matrix=pymupdf.Matrix(escala, escala))
        destino = Path(ruta_pdf).with_name(f"{Path(ruta_pdf).stem}_p{indice + 1}.png")
        imagen.save(destino)
        salida.append(destino)
    pdf.close()
    return salida


if __name__ == "__main__":
    docx = sys.argv[1]
    solo = [int(n) for n in sys.argv[2:]] or None
    pdf, total = a_pdf(docx)
    print(f"PDF: {pdf}  ({total} páginas)")
    for imagen in a_imagenes(pdf, solo):
        print(f"   {imagen}")
