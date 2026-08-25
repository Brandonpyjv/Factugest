"""
Sustentación, sección III. Diseño (diapositivas 23 a 30).

Las figuras son las mismas del documento de grado, no versiones hechas aparte para
la presentación. Si el jurado compara la diapositiva con el capítulo 5, encuentra el
mismo diagrama.

La única salvedad es la base de datos. En el documento va el modelo físico completo,
en página apaisada, y aquí va el modelo conceptual, porque veintisiete tablas
proyectadas no se leen desde la tercera fila del salón.
"""
import casos_de_uso as catalogo
import esquema
import ppt
from e3_documentacion import DETALLE


def casos_de_uso(d):
    """Diapositiva 24."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Casos de Uso")
    ppt.parrafo(d, f"El análisis identificó {len(catalogo.todos())} casos de uso agrupados en "
                   "los ocho módulos del sistema, con seis actores. Dos de ellos no son "
                   "personas, ya que uno es el sistema externo que consume la API y el otro "
                   "es quien recibe el documento emitido.",
                0.85, 1.4, 11.6, 0.9, tamano=ppt.Pt(18))
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "DCU-00 general.png", 2.4, 2.35, 8.5, 3.9)
    ppt.pie(d, "Diagrama general de casos de uso. Elaboración propia.")


def casos_de_uso_tabla(d):
    """Diapositiva 25. La ficha del caso central, resumida."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Documentación de Casos de Uso")
    precondiciones, flujo, _, postcondiciones, excepciones = DETALLE["CU-08"]
    ppt.tabla(d,
              ["CU-08", "Emitir factura de venta"],
              [["Actores", "Sistema cliente, Cajero"],
               ["Precondición", "El cliente tiene llave válida, resolución vigente y cupo "
                                "disponible en el mes"],
               ["Pasos 1 a 4", "Recibe los datos, valida la petición, comprueba el cupo y "
                               "reserva el consecutivo autorizado"],
               ["Pasos 5 a 8", "Calcula los totales, guarda el documento, genera el CUFE, el "
                               "PDF y el XML, y responde"],
               ["Paso 9", "Agenda el envío al comprador, ya fuera de la transacción"],
               ["Postcondición", "Existe un documento con número único y CUFE, y el consumo "
                                 "del mes aumentó en uno"],
               ["Excepción", "Si el cupo está agotado responde 403 antes de reservar el "
                             "consecutivo"]],
              x=0.75, y=1.65, ancho=11.85, alto=4.3,
              anchos=[2.5, 9.35], tamano=ppt.Pt(16))
    ppt.parrafo(d, "El cupo se valida en el paso 3, antes de reservar el número en el paso 4, "
                   "porque rechazar después de haber tomado uno gastaría un consecutivo de "
                   "una resolución autorizada en un documento que nunca existió.",
                0.75, 6.05, 11.85, 0.9, tamano=ppt.Pt(17))


def scrum(d):
    """Diapositiva 26."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Metodología de Desarrollo")
    ppt.parrafo(d, "Scrum, con ocho sprints de dos semanas entre noviembre de 2025 y marzo "
                   "de 2026. Cada sprint cerró con un módulo utilizable y no con una parte "
                   "de varios.",
                0.85, 1.4, 11.6, 0.8, tamano=ppt.Pt(18))
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "FIG-scrum.png", 1.6, 2.25, 10.1, 3.5)
    ppt.parrafo(d, "El alcance del proyecto cambió durante el desarrollo, y ese cambio se "
                   "incorporó reordenando el backlog sin desechar lo construido.",
                0.85, 6.0, 11.6, 0.6, tamano=ppt.Pt(19), color=ppt.AZUL, negrita=True)


def mockup_panel(d):
    """Diapositiva 27."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Mockup del Panel de Control")
    ppt.imagen_ajustada(d, ppt.CAPTURAS / "Mockup panel de control.png",
                        1.5, 1.45, 10.3, 4.5)
    ppt.parrafo(d, "El tablero se separó en dos secciones y se ordenaron de modo que el "
                   "servicio prestado aparezca antes que su cobro, porque es lo que la "
                   "empresa hace. Un tablero que abriera con las ventas describiría un "
                   "comercio y no un proveedor de facturación.",
                0.85, 6.05, 11.6, 0.9, tamano=ppt.Pt(17))


def mockup_factura(d):
    """Diapositiva 28."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Mockup de Crear Nueva Factura")
    ppt.imagen_ajustada(d, ppt.CAPTURAS / "Mockup crear nueva factura.png",
                        2.6, 1.45, 8.1, 4.5)
    ppt.parrafo(d, "Organizado en tres momentos, a quién se le factura, qué se le factura y "
                   "cómo paga, con el resumen de totales siempre a la vista. Responde a que "
                   "el registro de una venta toma pocos segundos y una pantalla que obligue a "
                   "ir y volver termina siendo rechazada.",
                0.85, 6.05, 11.6, 0.9, tamano=ppt.Pt(17))


def base_de_datos(d):
    """Diapositiva 29."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Diseño de la Base de Datos")
    # A la izquierda el modelo y a la derecha lo que hay que entender de él. Ocupando
    # todo el ancho, el diagrama se encoge por su altura y deja media diapositiva vacía.
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "FIG-mer.png", 0.7, 1.5, 7.9, 4.6)
    ppt.parrafo(d, "Dos zonas que no se mezclan", 8.9, 1.7, 3.9, 0.5, tamano=ppt.Pt(20),
                color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "La zona comercial guarda lo que el proveedor vende, con sus planes, sus clientes y "
        "sus facturas.",
        "La zona de middleware guarda lo que emite por cuenta de terceros.",
        "Una tabla puente registra qué mes de qué cliente ya fue cobrado.",
    ], 8.9, 2.6, 3.9, tamano=ppt.Pt(15), separacion=1.2)
    ppt.parrafo(d, "Si un documento emitido para un cliente se guardara en la zona comercial, "
                   "el tablero lo contaría como ingreso propio del proveedor.",
                0.7, 6.25, 11.9, 0.7, tamano=ppt.Pt(17))
    ppt.pie(d, "Modelo entidad-relación conceptual. El modelo físico completo consta en el "
               "documento de grado.")


def diccionario(d):
    """Diapositiva 30."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Diccionario de Datos")
    ppt.parrafo(d, "Tabla documentos, la que guarda cada documento emitido por cuenta de "
                   "terceros", 0.85, 1.35, 11.6, 0.4, tamano=ppt.Pt(19), color=ppt.AZUL,
                negrita=True)
    interesan = ["cod_documento", "id_publico", "cod_cliente_api", "cod_empresa", "tipo",
                 "numero", "cufe", "estado", "referencia_externa", "total"]
    columnas = {c[0]: c for c in esquema.columnas("documentos")}
    descripciones = {
        "cod_documento": "Identificador interno del documento",
        "id_publico": "Identificador que ve el cliente, sin exponer la clave interna",
        "cod_cliente_api": "Cliente integrado por cuenta del cual se emitió",
        "cod_empresa": "Empresa emisora con cuya resolución se numeró",
        "tipo": "Factura de venta, nota crédito o nota débito",
        "numero": "Número completo del documento, con su prefijo",
        "cufe": "Código único de facturación electrónica",
        "estado": "Resultado ante la administración tributaria",
        "referencia_externa": "Identificador de la venta en el sistema del cliente",
        "total": "Valor final del documento",
    }
    filas = []
    for nombre in interesan:
        _, tipo, nulo, clave, _ = columnas[nombre]
        filas.append([nombre, tipo, clave, descripciones[nombre]])
    ppt.tabla(d, ["Campo", "Tipo", "Clave", "Descripción"], filas,
              x=0.75, y=1.85, ancho=11.85, alto=4.1,
              anchos=[2.7, 1.9, 1.5, 5.75], tamano=ppt.Pt(14))
    ppt.parrafo(d, "La referencia externa es la que hace idempotente el reintento, y sobre el "
                   "número hay un índice único por emisor y tipo.",
                0.75, 6.1, 11.85, 0.6, tamano=ppt.Pt(17), color=ppt.GRIS)


def escribir(presentacion):
    s = presentacion.slides
    casos_de_uso(s[23])
    casos_de_uso_tabla(s[24])
    scrum(s[25])
    mockup_panel(s[26])
    mockup_factura(s[27])
    base_de_datos(s[28])
    diccionario(s[29])


if __name__ == "__main__":
    import p1_formulacion
    import p2_analisis
    p = ppt.abrir()
    p1_formulacion.escribir(p)
    p2_analisis.escribir(p)
    escribir(p)
    print("Guardado:", ppt.guardar(p))
