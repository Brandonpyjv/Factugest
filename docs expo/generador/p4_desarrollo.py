"""
Sustentación, secciones IV y V. Desarrollo e implementación (diapositivas 31 a 39).

Las dos diapositivas de herramientas conservan la tabla y los logotipos del borrador,
porque las tecnologías que allí aparecen siguen siendo las que el proyecto usa. Solo
se actualizan las descripciones y se llena la fila que había quedado vacía.

Se agregan dos diapositivas que la plantilla no traía, la de resultados y la de
referencias. Se crean duplicando una existente, de modo que heredan el fondo, el
logotipo y la línea inferior sin tener que rehacerlos.
"""
import ppt
from e4_cap6b import PRUEBAS_AUTOMATICAS, RESULTADOS, SEGUNDOS


def _escribir_tabla(diapositiva, filas, columna_desde=1):
    """Reescribe las celdas de la tabla que ya está en la diapositiva."""
    for forma in diapositiva.shapes:
        if forma.has_table:
            tabla = forma.table
            for indice, valores in enumerate(filas, start=1):
                if indice >= len(tabla.rows):
                    break
                for salto, texto in enumerate(valores):
                    celda = tabla.cell(indice, columna_desde + salto)
                    celda.text_frame.clear()
                    parrafo = celda.text_frame.paragraphs[0]
                    run = parrafo.add_run()
                    run.text = texto
                    run.font.size = ppt.Pt(15)
                    run.font.bold = salto == 0
                    run.font.color.rgb = ppt.AZUL if salto == 0 else ppt.TINTA
                    run.font.name = ppt.FUENTE
            return tabla
    return None


def herramientas_backend(d):
    """Diapositiva 32. Se conservan la tabla y los logotipos."""
    ppt.titulo(d, "Herramientas de Backend, Base de Datos y Web")
    for forma in d.shapes:
        if not forma.has_text_frame or forma.top is None or forma.top <= ppt.LIMITE_TITULO:
            continue
        texto = forma.text_frame.text
        nuevo = None
        if "FastAPI" in texto or "Lenguaje y framework" in texto:
            nuevo = ("Lenguaje y framework del servidor. Valida los datos de entrada desde "
                     "los tipos declarados y publica el contrato de la API automáticamente."
                     if "Lenguaje" in texto else None)
        elif "MySQL" in texto or "Base de datos relacional" in texto:
            nuevo = ("Gestor relacional con veintisiete tablas en dos zonas, con acceso "
                     "mediante consultas SQL explícitas."
                     if "Base de datos" in texto else None)
        elif "HTML" in texto or "Tecnologías estándar" in texto:
            nuevo = ("Plantillas Jinja2 con Bootstrap y Chart.js para el panel y sus "
                     "gráficas." if "Tecnologías" in texto else None)
        elif "Entorno de desarrollo" in texto:
            nuevo = "Entorno de desarrollo usado para escribir, depurar y mantener el código."
        if nuevo:
            marco = forma.text_frame
            marco.clear()
            run = marco.paragraphs[0].add_run()
            run.text = nuevo
            run.font.size = ppt.Pt(15)
            run.font.color.rgb = ppt.TINTA
            run.font.name = ppt.FUENTE


def herramientas_apoyo(d):
    """Diapositiva 33. Se llena además la cuarta fila, que estaba vacía."""
    # Los rótulos del borrador eran cuadros flotantes encima de la tabla, no celdas.
    # Sin retirarlos, el texto nuevo se superpone al viejo.
    ppt.limpiar(d, tablas=False)
    ppt.titulo(d, "Herramientas de Apoyo, Pruebas y Control de Versiones")
    _escribir_tabla(d, [
        ["Claude AI", "Asistente empleado para revisar código, contrastar decisiones de "
                      "diseño y redactar documentación."],
        ["Postman", "Cliente con el que se probaron las nueve operaciones de la API antes "
                    "de integrarlas."],
        ["Git y GitHub", "Control de versiones y alojamiento remoto para el trabajo "
                         "colaborativo del equipo."],
        ["pytest", f"Ejecuta las {PRUEBAS_AUTOMATICAS} pruebas automatizadas del proyecto en "
                   f"{SEGUNDOS} segundos."],
    ])


def pruebas(d):
    """Diapositiva 35."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Pruebas del Sistema")
    ppt.parrafo(d, f"{PRUEBAS_AUTOMATICAS} pruebas automatizadas en {SEGUNDOS} segundos, más pruebas "
                   "funcionales sobre la interfaz.",
                0.85, 1.4, 11.6, 0.8, tamano=ppt.Pt(20), color=ppt.AZUL, negrita=True)
    ppt.parrafo(d, "Qué se comprueba", 0.9, 2.4, 5.4, 0.4, tamano=ppt.Pt(20), color=ppt.AZUL,
                negrita=True)
    ppt.vinetas(d, [
        "Que la aritmética tributaria arroje los mismos valores en la web y en la API.",
        "Que un fallo a mitad de una emisión no deje rastro ni gaste un consecutivo.",
        "Que los documentos lleven la identidad de la empresa emisora.",
        "Que el control de acceso impida a cada rol lo que no le corresponde.",
    ], 0.9, 3.0, 5.4, tamano=ppt.Pt(16), separacion=0.82)

    ppt.parrafo(d, "Qué quedó fuera", 6.9, 2.4, 5.5, 0.4, tamano=ppt.Pt(20), color=ppt.AZUL,
                negrita=True)
    ppt.vinetas(d, [
        "La carga sostenida, que exige una infraestructura de producción.",
        "La validación contra los servicios en producción de la DIAN, que depende de la "
        "habilitación del proveedor.",
    ], 6.9, 3.0, 5.5, tamano=ppt.Pt(16), separacion=1.3)
    ppt.parrafo(d, "Comprobar qué pasa cuando algo falla pesa tanto como comprobar que funciona.",
                0.85, 6.1, 11.6, 0.7, tamano=ppt.Pt(17))


def evidencia(d, requisito, caso, antes, despues, cierre):
    """Una prueba funcional, con el formulario a la izquierda y el resultado a la derecha."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Evidencia de Pruebas")
    ppt.parrafo(d, f"{requisito}. {caso}", 0.85, 1.35, 11.6, 0.4,
                tamano=ppt.Pt(19), color=ppt.AZUL, negrita=True)
    ppt.parrafo(d, "Formulario diligenciado", 0.9, 1.9, 5.4, 0.3, tamano=ppt.Pt(15),
                color=ppt.GRIS)
    ppt.imagen_ajustada(d, ppt.CAPTURAS / antes, 0.9, 2.25, 5.5, 3.3)
    ppt.parrafo(d, "Resultado obtenido", 6.9, 1.9, 5.4, 0.3, tamano=ppt.Pt(15),
                color=ppt.GRIS)
    ppt.imagen_ajustada(d, ppt.CAPTURAS / despues, 6.9, 2.25, 5.5, 3.3)
    ppt.parrafo(d, cierre, 0.85, 5.85, 11.6, 0.7, tamano=ppt.Pt(18))
    ppt.pie(d, "Las cuatro evidencias constan en el capítulo 6 del documento de grado.")


def resultado_factura(d):
    """Resultado de la prueba de emisión, con lo que el sistema produjo."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Resultado Obtenido de la Emisión")
    ppt.parrafo(d, "La prueba fue satisfactoria. La factura quedó emitida y disponible para "
                   "su descarga.",
                0.85, 1.4, 11.6, 0.7, tamano=ppt.Pt(21), color=ppt.AZUL, negrita=True)
    ppt.tabla(d,
              ["Lo que se comprobó", "Resultado"],
              [["Numeración", "El documento tomó el siguiente consecutivo autorizado de la "
                              "resolución del emisor"],
               ["Cálculo", "Las bases, los descuentos y los impuestos coinciden con los "
                           "valores esperados"],
               ["Código único", "Se generó el CUFE y quedó asociado al documento"],
               ["Archivos", "La representación gráfica y el archivo XML quedaron disponibles "
                            "para descarga"],
               ["Registro", "La operación quedó anotada en el rastro de auditoría"]],
              x=0.9, y=2.3, ancho=11.5, alto=3.2,
              anchos=[3.1, 8.4], tamano=ppt.Pt(16))
    ppt.parrafo(d, "El consecutivo se reserva dentro de la misma transacción que guarda el "
                   "documento, de modo que un fallo a mitad no deja una factura incompleta ni "
                   "gasta un número de la resolución.",
                0.9, 5.75, 11.5, 0.9, tamano=ppt.Pt(17))


def resultados(d):
    """Diapositiva nueva, entre la evidencia y las referencias."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Resultados Obtenidos")
    ppt.tabla(d,
              ["Objetivo", "Resultado", "Estado"],
              [[objetivo, resultado, estado] for objetivo, resultado, estado in RESULTADOS],
              x=0.75, y=1.55, ancho=11.85, alto=4.4,
              anchos=[3.0, 7.3, 1.55], tamano=ppt.Pt(13))
    ppt.parrafo(d, "Un punto de venta en operación que no emitía facturación electrónica "
                   "quedó expidiendo documentos válidos sin cambiar la forma en que registra "
                   "sus ventas.",
                0.75, 6.1, 11.85, 0.8, tamano=ppt.Pt(19), color=ppt.AZUL, negrita=True)


def referencias(d):
    """Diapositiva nueva. La plantilla no traía una, y APA la recomienda."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Referencias")
    ppt.vinetas(d, [
        "Dirección de Impuestos y Aduanas Nacionales. (2020). Resolución 000042 de 2020. "
        "DIAN.",
        "Estatuto Tributario Nacional. Art. 616-1. Factura o documento equivalente. Decreto "
        "624 de 1989.",
        "Fielding, R. T. (2000). Architectural styles and the design of network-based "
        "software architectures. University of California, Irvine.",
        "Organization for the Advancement of Structured Information Standards. (2013). "
        "Universal Business Language Version 2.1. OASIS.",
        "Schwaber, K., y Sutherland, J. (2020). La Guía de Scrum. Scrum.org.",
        "Sommerville, I. (2011). Ingeniería de software (9.ª ed.). Pearson Educación.",
    ], 0.85, 1.55, 11.6, tamano=ppt.Pt(15), separacion=0.82)
    ppt.pie(d, "Las trece referencias del trabajo constan en el documento de grado, en estilo "
               "APA séptima edición.")


def escribir(presentacion):
    s = presentacion.slides
    herramientas_backend(s[31])
    herramientas_apoyo(s[32])
    pruebas(s[34])
    evidencia(s[35], "RF 4.2", "Registro de un cliente",
              "registro de nuevo cliente.png", "registro de nuevo cliente emitido.png",
              "El cliente quedó registrado y disponible para facturarle, y la operación "
              "quedó anotada en el registro de auditoría.")

    # Cuatro diapositivas que la plantilla no traía, copiadas de una de contenido para
    # que hereden el fondo y la decoración.
    for posicion in (36, 37, 38, 39):
        ppt.duplicar(presentacion, 35, posicion=posicion)

    evidencia(presentacion.slides[36], "RF 4.1", "Emisión de una factura",
              "registro de nueva factura.png", "registro de nueva factura emitida.png",
              "La factura quedó emitida con su número consecutivo, su código único y sus "
              "totales calculados.")
    resultado_factura(presentacion.slides[37])
    resultados(presentacion.slides[38])
    referencias(presentacion.slides[39])


if __name__ == "__main__":
    import p1_formulacion
    import p2_analisis
    import p3_diseno
    p = ppt.abrir()
    p1_formulacion.escribir(p)
    p2_analisis.escribir(p)
    p3_diseno.escribir(p)
    escribir(p)
    ppt.numerar(p)
    print("Guardado:", ppt.guardar(p), "·", len(p.slides), "diapositivas")
