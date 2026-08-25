"""
Sustentación, sección I. Formulación del proyecto (diapositivas 1 a 10).

El texto sale del documento de grado, resumido para caber en pantalla pero sin
cambiar lo que dice. Que la sustentación y el documento coincidan palabra por
palabra es lo que evita que el jurado encuentre dos versiones del mismo proyecto.

Las cifras de la justificación son las de la encuesta y viven en `encuesta.py`, de
modo que no puedan discrepar de las que aparecen en el capítulo 3.
"""
import encuesta
import ppt
from pptx.enum.text import PP_ALIGN


def _porcentaje(cantidad):
    return f"{encuesta.porcentaje(cantidad)}%"


def portada_sena(d):
    """Diapositiva 1. Solo se actualizan los integrantes, el resto es de la plantilla."""
    for forma in d.shapes:
        if forma.has_text_frame and "INTEGRANTES" in forma.text_frame.text.upper():
            marco = forma.text_frame
            marco.clear()
            lineas = ["INTEGRANTES:", "", "BRANDON ARLEY RESTREPO GÉLVEZ",
                      "JOHAN SEBASTIÁN ACOSTA SÁNCHEZ", "WILMER JESÚS CONTRERAS RANGEL",
                      "", "Ficha 3115426"]
            for indice, linea in enumerate(lineas):
                parrafo = marco.paragraphs[0] if indice == 0 else marco.add_paragraph()
                parrafo.alignment = PP_ALIGN.CENTER
                run = parrafo.add_run()
                run.text = linea
                run.font.size = ppt.SECUNDARIO
                run.font.bold = linea.startswith(("INTEGRANTES", "BRANDON", "JOHAN", "WILMER"))
                run.font.color.rgb = ppt.AZUL if linea.startswith("INTEGRANTES") else ppt.TINTA
                run.font.name = ppt.FUENTE
            return


def portada_proyecto(d):
    """Diapositiva 2. Se corrige el subtítulo, que describía el proyecto anterior."""
    for forma in d.shapes:
        if forma.has_text_frame and "Plataforma" in forma.text_frame.text:
            marco = forma.text_frame
            marco.clear()
            run = marco.paragraphs[0].add_run()
            run.text = ("Plataforma web de facturación electrónica que emite por cuenta de "
                        "terceros mediante una API de integración.")
            run.font.size = ppt.CUERPO
            run.font.color.rgb = ppt.TINTA
            run.font.name = ppt.FUENTE
            return


def problema(d):
    """Diapositiva 4."""
    ppt.limpiar(d)
    ppt.titulo(d, "Planteamiento del Problema")
    ppt.parrafo(d, "La facturación electrónica es obligatoria en Colombia, pero la mayoría "
                   "de las mipymes todavía no la ha adoptado.",
                0.7, 1.55, 11.9, 0.9, tamano=ppt.DESTACADO, color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "La mayoría de estas empresas ya opera con un software propio, sea un punto de "
        "venta, un sistema contable o una aplicación hecha a la medida años atrás.",
        "La oferta habitual del mercado exige reemplazar esa herramienta, migrar la "
        "información, capacitar de nuevo al personal e interrumpir la operación mientras "
        "dura el cambio.",
        "El problema no es tecnológico sino de reemplazo, porque estas empresas no rechazan "
        "facturar electrónicamente sino abandonar el sistema con el que ya trabajan.",
    ], 0.9, 3.05, 11.4, separacion=1.25)
    ppt.pie(d, "Fuente: elaboración propia con base en la encuesta aplicada a "
               f"{encuesta.MUESTRA} empresas.")


def justificacion(d):
    """Diapositiva 5. Se conservan las tres tarjetas y se llenan con datos de la encuesta."""
    ppt.limpiar(d)
    ppt.titulo(d, "Justificación del Proyecto")

    tarjetas = [
        (_porcentaje(37), "ESTÁN OBLIGADAS",
         "de las empresas consultadas debe facturar electrónicamente ante la DIAN.", 0.84),
        (_porcentaje(17), "CAMBIAR DE SOFTWARE",
         "señaló el reemplazo de su herramienta como la principal barrera para adoptarla.",
         4.95),
        (_porcentaje(38), "SÍ LO HARÍAN",
         "facturaría electrónicamente si no tuviera que cambiar de software.", 9.07),
    ]
    for cifra, rotulo, detalle, x in tarjetas:
        ppt.parrafo(d, cifra, x, 2.55, 3.42, 0.7, tamano=ppt.Pt(40), color=ppt.AZUL,
                    negrita=True)
        ppt.parrafo(d, rotulo, x, 3.32, 3.42, 0.3, tamano=ppt.Pt(14), color=ppt.AMARILLO,
                    negrita=True)
        ppt.parrafo(d, detalle, x, 3.68, 3.3, 1.2, tamano=ppt.Pt(15), color=ppt.TINTA)

    ppt.parrafo(d, "FactuGest permite cumplir la obligación sin reemplazar el software con "
                   "el que la empresa ya trabaja.",
                0.93, 5.36, 11.5, 0.6, tamano=ppt.DESTACADO, color=ppt.AZUL, negrita=True)
    ppt.pie(d, f"Fuente: encuesta aplicada a {encuesta.MUESTRA} empresas de Cúcuta durante "
               "la fase de análisis.")


def objetivo_general(d):
    """Diapositiva 6."""
    ppt.limpiar(d)
    ppt.titulo(d, "Objetivo General")
    ppt.parrafo(d, "Desarrollar FactuGest, una plataforma web de facturación electrónica que "
                   "opere como proveedor tecnológico para micro, pequeñas y medianas "
                   "empresas de Colombia, permitiéndoles emitir facturas de venta, notas "
                   "crédito y notas débito conforme a la normativa de la DIAN a través de "
                   "una API de integración que se conecta con los sistemas que ya utilizan.",
                1.4, 2.5, 10.6, 3.0, tamano=ppt.DESTACADO, color=ppt.AZUL, negrita=True,
                alineacion=PP_ALIGN.CENTER)


def objetivos_especificos(d):
    """Diapositiva 7. Se retiran las tres tarjetas, porque los objetivos son cinco."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Objetivos Específicos")
    ppt.vinetas(d, [
        "1. Implementar el módulo de emisión de documentos electrónicos con su cálculo "
        "tributario, su consecutivo autorizado, su CUFE, su PDF y su XML bajo UBL 2.1.",
        "2. Construir una API REST de integración con autenticación por llave, control de cupo "
        "y una forma única de error documentada en OpenAPI.",
        "3. Desarrollar el módulo de clientes API y planes de suscripción, con la generación y "
        "rotación de llaves y el control del consumo mensual.",
        "4. Implementar un panel de control y un módulo de reportes exportables a CSV y a PDF.",
        "5. Establecer el esquema de seguridad con autenticación, roles jerárquicos y registro "
        "de auditoría de las operaciones de escritura.",
    ], 0.9, 1.75, 11.4, tamano=ppt.CUERPO, separacion=1.05)


def alcance(d):
    """Diapositiva 8."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Alcance")
    ppt.parrafo(d, "Lo que el sistema hace", 0.9, 1.6, 5.4, 0.4, tamano=ppt.Pt(22),
                color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "Emite facturas de venta, notas crédito y notas débito por cuenta de terceros.",
        "Expone una API que el software del cliente consume para emitir sus documentos.",
        "Administra los clientes integrados, sus llaves y sus planes.",
        "Controla el consumo mensual y factura la mensualidad del servicio.",
        "Consolida la operación en un tablero y siete reportes exportables.",
    ], 0.9, 2.2, 5.4, tamano=ppt.Pt(17), separacion=0.86)

    ppt.parrafo(d, "Lo que queda fuera de esta versión", 6.9, 1.6, 5.5, 0.4,
                tamano=ppt.Pt(22), color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "La transmisión a los servicios de producción de la DIAN, pendiente de la "
        "habilitación del proveedor.",
        "La integración con pasarelas de pago, porque el recaudo se registra a mano.",
        "El cliente móvil, que quedó fuera de esta versión.",
        "La prueba de carga sostenida, que exige infraestructura de producción.",
    ], 6.9, 2.2, 5.5, tamano=ppt.Pt(17), separacion=1.05)


def riesgos(d):
    """Diapositiva 9. Trae dos bloques, y cada uno con su propio rótulo."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Riesgos")
    ppt.vinetas(d, [
        "Que la empresa no cuente con personal técnico capaz de consumir la interfaz de "
        "integración.",
        "Que un servicio externo, como el correo del comprador, no esté disponible en el "
        "momento de emitir.",
        "Que la empresa desconfíe de delegar su facturación en un tercero, que es una "
        "decisión que excede lo técnico.",
    ], 0.9, 1.55, 11.4, tamano=ppt.Pt(18), separacion=0.82)

    ppt.parrafo(d, "Restricciones", 0.62, 4.23, 5.0, 0.5, tamano=ppt.TITULO, color=ppt.AZUL,
                negrita=True)
    ppt.vinetas(d, [
        "La habilitación como proveedor ante la DIAN es un trámite que no controla el equipo.",
        "Cada documento necesita una resolución de facturación vigente con su prefijo y su "
        "rango autorizados.",
        "La operación requiere conexión a internet en los dos extremos, el del proveedor y el "
        "del sistema integrado.",
    ], 0.9, 5.05, 11.4, tamano=ppt.Pt(18), separacion=0.78)


def cronograma(d):
    """Diapositiva 10.

    Va en diagrama de Gantt y no en el cuadro de cuatro filas que traía antes. El
    cuadro decía en qué meses ocurrió cada fase, pero para saber si dos se solapaban
    había que restar fechas mentalmente; en el Gantt eso se ve de una mirada, que es
    para lo que sirve un cronograma. Los periodos son exactamente los mismos.
    """
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Cronograma de Actividades")
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "FIG-cronograma.png", 0.55, 1.5, 12.25, 4.5)
    ppt.parrafo(d, "El proyecto se desarrolló en dieciséis meses, y la fase de análisis ocupó "
                   "cuatro de ellos porque de ahí salió el hallazgo que cambió la solución.",
                0.75, 6.15, 11.85, 0.7, tamano=ppt.Pt(18), color=ppt.TINTA)
    ppt.pie(d, "Elaboración propia.", y=6.85)


def escribir(presentacion):
    diapositivas = presentacion.slides
    portada_sena(diapositivas[0])
    portada_proyecto(diapositivas[1])
    problema(diapositivas[3])
    justificacion(diapositivas[4])
    objetivo_general(diapositivas[5])
    objetivos_especificos(diapositivas[6])
    alcance(diapositivas[7])
    riesgos(diapositivas[8])
    cronograma(diapositivas[9])


if __name__ == "__main__":
    p = ppt.abrir()
    escribir(p)
    print("Guardado:", ppt.guardar(p))
