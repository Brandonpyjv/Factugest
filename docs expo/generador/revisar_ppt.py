"""
Convierte una presentación a PDF con PowerPoint y la renderiza a imágenes.

Igual que `revisar.py` para los documentos, pero para las diapositivas. Hace falta
por la misma razón, porque lo que python-pptx escribe solo se ve como quedará
cuando PowerPoint compone la diapositiva con su fondo y su plantilla.

    python revisar_ppt.py "../carpeta exposicion/archivo.pptx"        # todas
    python revisar_ppt.py "../carpeta exposicion/archivo.pptx" 1 4 12  # solo esas
"""
import sys
from pathlib import Path

import pymupdf
import win32com.client

PPT_A_PDF = 32          # ppSaveAsPDF


def a_pdf(ruta_pptx):
    ruta_pptx = Path(ruta_pptx).resolve()
    ruta_pdf = ruta_pptx.with_suffix(".pdf")
    powerpoint = win32com.client.Dispatch("PowerPoint.Application")
    try:
        presentacion = powerpoint.Presentations.Open(str(ruta_pptx), WithWindow=False)
        presentacion.SaveAs(str(ruta_pdf), PPT_A_PDF)
        total = presentacion.Slides.Count
        presentacion.Close()
    finally:
        powerpoint.Quit()
    return ruta_pdf, total


def a_imagenes(ruta_pdf, paginas=None, escala=1.3):
    pdf = pymupdf.open(ruta_pdf)
    salida = []
    indices = [p - 1 for p in paginas] if paginas else range(pdf.page_count)
    for indice in indices:
        if indice >= pdf.page_count:
            continue
        imagen = pdf[indice].get_pixmap(matrix=pymupdf.Matrix(escala, escala))
        destino = Path(ruta_pdf).with_name(f"{Path(ruta_pdf).stem}_d{indice + 1}.png")
        imagen.save(destino)
        salida.append(destino)
    pdf.close()
    return salida


if __name__ == "__main__":
    pptx = sys.argv[1]
    solo = [int(n) for n in sys.argv[2:]] or None
    pdf, total = a_pdf(pptx)
    print(f"PDF: {pdf}  ({total} diapositivas)")
    for imagen in a_imagenes(pdf, solo):
        print(f"   {imagen}")
