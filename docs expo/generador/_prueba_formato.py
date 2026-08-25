"""
Prueba del motor APA: genera un documento corto con todos los elementos que el
instructivo regula, para abrirlo en Word y verificar el formato antes de escribir
ochenta páginas encima.

    python "docs expo/generador/_prueba_formato.py"
"""
from pathlib import Path

from apa import DocumentoAPA

BASE = Path(__file__).resolve().parent.parent
IMAGENES = BASE / "documento para que te guies claude"
SALIDA = BASE / "entregables" / "_prueba_formato_apa.docx"

d = DocumentoAPA()

d.portada(
    titulo="FACTUGEST",
    subtitulo="Plataforma web de facturación electrónica para micro, pequeñas y "
              "medianas empresas de Colombia",
    integrantes=["(pendiente: nombres de los integrantes)"],
    grado="Trabajo de grado presentado como requisito para optar al título de:\n"
          "Tecnólogo en Análisis y Desarrollo de Software",
    institucion=["SERVICIO NACIONAL DE APRENDIZAJE — SENA",
                 "Centro de la Industria, la Empresa y los Servicios (CIES)",
                 "Tecnólogo en Análisis y Desarrollo de Software"],
    ciudad="CÚCUTA, NORTE DE SANTANDER",
    anio=2026,
)

d.tabla_contenido()

d.titulo("Prueba de formato", nivel=1)
d.parrafo(
    "Este documento no hace parte de los entregables. Existe para verificar en Word "
    "que el motor de formato aplica lo que el instructivo exige: márgenes de 2,54 cm "
    "en los cuatro lados, Times New Roman de 12 puntos, interlineado doble, sangría "
    "de primera línea de 1,27 cm y numeración de páginas en la esquina superior "
    "derecha desde la portada."
)
d.parrafo(
    "Este segundo párrafo permite comprobar dos cosas a la vez: que la sangría de "
    "primera línea se repite y que entre párrafos no se agrega espacio adicional, "
    "porque en un texto a doble espacio ese espacio extra sobra."
)

d.titulo("1.1 Un título de nivel 2", nivel=2)
d.parrafo(
    "Los títulos no se escriben con mayúscula sostenida y conservan el tamaño del "
    "cuerpo del texto. Se distinguen por su peso y su posición, no por ser más "
    "grandes."
)

d.titulo("1.1.1 Un título de nivel 3", nivel=3)
d.parrafo(
    "El de nivel 3 va en negrita cursiva y termina en punto. El motor le agrega el "
    "punto si quien escribe lo olvida."
)

d.parrafo("Una lista con viñetas:", sangria=False)
d.vinetas([
    "Emisión de facturas de venta, notas crédito y notas débito.",
    "API REST de integración autenticada con llave por cliente.",
    "Control de consumo contra el cupo del plan contratado.",
])

d.parrafo("Una cita de más de cuarenta palabras, en bloque y sin comillas:", sangria=False)
d.cita_larga(
    "La facturación electrónica es en Colombia un requisito de obligatorio "
    "cumplimiento para los sujetos definidos por la administración tributaria, y su "
    "incumplimiento compromete la deducibilidad de costos y gastos, dificulta las "
    "relaciones comerciales con clientes que exigen soporte válido y expone al "
    "contribuyente a sanciones.",
    fuente="Autor, 2024, p. 12",
)

d.tabla(
    "Planes de suscripción de FactuGest",
    ["Plan", "Precio mensual", "Documentos incluidos"],
    [
        ["Básico", "$ 89.000", "150"],
        ["Pro", "$ 189.000", "400"],
        ["Ilimitado", "$ 390.000", "Sin cupo"],
    ],
    nota="Elaboración propia. Los precios corresponden al catálogo de servicios del "
         "sistema. El documento emitido por encima del cupo se cobra aparte.",
)

d.figura(
    "Estructura del proyecto FactuGest",
    IMAGENES / "estructura del proyecto.png",
    nota="Organización de carpetas del repositorio. Elaboración propia.",
)

SALIDA.parent.mkdir(parents=True, exist_ok=True)
d.guardar(SALIDA)
print(f"Generado: {SALIDA}")
print(f"Tablas: {d.n_tabla} · Figuras: {d.n_figura}")
