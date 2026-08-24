"""
Sustentación, sección II. Análisis (diapositivas 11 a 22).

Las tablas de requisitos y de priorización se arman importando `e1_requisitos.py`,
igual que hace el capítulo 4 del documento. Ninguna cifra está escrita a mano, de
modo que la sustentación no puede quedar diciendo algo distinto del documento que
el jurado tiene delante.
"""
import encuesta
import ppt
from e1_requisitos import MODULOS, RNF, prioridad, puntaje


def _criticos(requisitos):
    return sum(1 for c, n, d, a, v, u in requisitos if prioridad(v, u) == "Crítica")


def _n(cantidad):
    return f"{cantidad} ({encuesta.porcentaje(cantidad)} %)"


def encuesta_tecnica(d):
    """Diapositiva 12."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Herramientas para la Captura de Requisitos")
    ppt.parrafo(d, "Encuesta", 0.9, 1.45, 4.0, 0.45, tamano=ppt.Pt(22), color=ppt.AZUL,
                negrita=True)
    ppt.parrafo(d, f"Cuestionario de doce preguntas cerradas aplicado a "
                   f"{encuesta.MUESTRA} empresas de Cúcuta, agrupadas en cuatro bloques que "
                   "indagaban su situación frente a la obligación, las herramientas que "
                   "utilizan, las barreras percibidas y su disposición frente a una solución "
                   "que se integre con el software existente.",
                0.9, 1.95, 11.5, 1.0, tamano=ppt.Pt(18))
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "FIG-encuesta-contraste.png",
                        0.75, 3.0, 11.85, 3.0)
    ppt.parrafo(d, "Rechazan cambiar de software, no facturar electrónicamente.",
                0.9, 6.15, 11.5, 0.5, tamano=ppt.Pt(22), color=ppt.AZUL, negrita=True)
    ppt.pie(d, "Preguntas 6 y 7 del instrumento. Elaboración propia.")


def historias_encuesta(d):
    """Diapositiva 13."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Historias de Usuario")
    ppt.parrafo(d, "Derivadas de la encuesta", 0.9, 1.4, 6.0, 0.4, tamano=ppt.Pt(20),
                color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "HU-03. Como sistema cliente, quiero enviar los datos de una venta y recibir el "
        "documento ya emitido para cumplir con la obligación sin cambiar el software con el "
        "que opero.",
        "HU-04. Como sistema cliente, quiero reenviar una emisión con la misma referencia y "
        "obtener el documento ya expedido para poder reintentar sin duplicar facturas.",
        "HU-06. Como comprador, quiero recibir el PDF y el XML en mi correo para contar con "
        "el soporte de la compra sin tener que solicitarlo.",
    ], 0.9, 2.1, 11.4, tamano=ppt.Pt(19), separacion=1.4)
    ppt.parrafo(d, "La HU-04 no la pidió nadie. Salió de advertir que el sistema que integra "
                   "puede perder la respuesta por una falla de red y volver a intentarlo.",
                0.9, 6.3, 11.4, 0.6, tamano=ppt.Pt(17), color=ppt.GRIS)


def rf_encuesta(d):
    """Diapositiva 14."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Requisitos Funcionales Relacionados")
    ppt.tabla(d,
              ["Código", "Requisito", "Qué resuelve"],
              [["RF 8.5", "Emisión por API",
                "El sistema del cliente solicita la expedición sin cambiar su operación"],
               ["RF 8.6", "Idempotencia de la emisión",
                "Reenviar la misma referencia devuelve el documento, no crea otro"],
               ["RF 8.10", "Documentación automática",
                "El contrato se publica desde el código, para que integrarse sea barato"],
               ["RF 2.10", "Envío del documento al comprador",
                "El PDF y el XML llegan al correo sin demorar la respuesta"]],
              x=0.75, y=1.9, ancho=11.85, alto=3.4,
              anchos=[1.7, 3.6, 6.55], tamano=ppt.Pt(17))
    ppt.parrafo(d, "Los cuatro pertenecen a los módulos de integración y de documentos "
                   "electrónicos, que son los que sostienen la propuesta de valor.",
                0.75, 5.6, 11.85, 0.6, tamano=ppt.Pt(18))


def observacion_tecnica(d):
    """Diapositiva 15."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Herramientas para la Captura de Requisitos")
    ppt.parrafo(d, "Observación directa", 0.9, 1.4, 5.0, 0.45, tamano=ppt.Pt(22),
                color=ppt.AZUL, negrita=True)
    ppt.parrafo(d, "Se presenció el registro de ventas en un punto de venta en operación que no "
                   "emitía facturación electrónica.",
                0.9, 1.95, 11.5, 0.8, tamano=ppt.Pt(18))
    ppt.vinetas(d, [
        "El punto de venta concentra información que el negocio no está dispuesto a migrar, "
        "como su catálogo, sus precios y sus clientes frecuentes.",
        "El registro de una venta toma pocos segundos, de modo que cualquier solución que "
        "agregue pasos será rechazada por quien la usa.",
        "El comprobante que hoy se entrega no tiene validez fiscal, pero el cliente ya lo "
        "espera.",
        "El negocio no cuenta con personal técnico permanente, así que la integración debe "
        "poder hacerla quien mantiene el punto de venta.",
    ], 0.9, 2.95, 11.4, tamano=ppt.Pt(18), separacion=1.0)


def historias_observacion(d):
    """Diapositiva 16."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Historias de Usuario")
    ppt.parrafo(d, "Derivadas de la observación directa", 0.9, 1.4, 7.0, 0.4,
                tamano=ppt.Pt(20), color=ppt.AZUL, negrita=True)
    ppt.vinetas(d, [
        "HU-01. Como administrador, quiero registrar una empresa cliente y generar su llave "
        "de acceso para que su sistema pueda empezar a emitir documentos electrónicos.",
        "HU-02. Como administrador, quiero rotar la llave de un cliente para revocar una "
        "credencial comprometida sin interrumpir el servicio.",
        "HU-11. Como administrador, quiero consultar el tablero de control filtrado por "
        "periodo para evaluar el comportamiento del servicio y del recaudo.",
    ], 0.9, 2.1, 11.4, tamano=ppt.Pt(19), separacion=1.4)
    ppt.parrafo(d, "Que la integración deba ser sencilla no es una preferencia de diseño. "
                   "Es la condición para que un negocio sin personal técnico pueda adoptarla.",
                0.9, 6.3, 11.4, 0.6, tamano=ppt.Pt(17), color=ppt.GRIS)


def rf_observacion(d):
    """Diapositiva 17."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Requisitos Funcionales Relacionados")
    ppt.tabla(d,
              ["Código", "Requisito", "Qué resuelve"],
              [["RF 1.1", "Registro de cliente API",
                "Da de alta la empresa con su plan y su empresa emisora"],
               ["RF 1.2", "Generación de la llave de acceso",
                "Produce la credencial con que el sistema del cliente se identifica"],
               ["RF 1.8", "Rotación de la llave",
                "Reemplaza una credencial comprometida sin interrumpir el servicio"],
               ["RF 5.1", "Tablero del servicio",
                "Muestra los documentos emitidos, la aceptación y el ingreso recurrente"]],
              x=0.75, y=1.9, ancho=11.85, alto=3.4,
              anchos=[1.7, 3.9, 6.25], tamano=ppt.Pt(17))
    ppt.parrafo(d, "La observación no produjo funciones nuevas sino condiciones sobre las "
                   "que ya existían, y esa es la diferencia entre las dos técnicas.",
                0.75, 5.6, 11.85, 0.6, tamano=ppt.Pt(18))


def stakeholders(d):
    """Diapositiva 18."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Matriz de Stakeholders")
    ppt.imagen_ajustada(d, ppt.DIAGRAMAS / "FIG-stakeholders.png", 1.3, 1.45, 10.7, 4.45)
    ppt.parrafo(d, "La DIAN quedó en alta influencia y bajo interés, porque no participa en "
                   "el proyecto pero fija las condiciones que todo documento debe cumplir.",
                0.9, 6.1, 11.5, 0.7, tamano=ppt.Pt(18))
    ppt.pie(d, "Elaboración propia.")


def priorizacion(d):
    """Diapositiva 19."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Técnica de Priorización de Requisitos")
    ppt.tabla(d,
              ["Puntaje", "Valor de negocio", "Urgencia"],
              [["1", "Impacto muy bajo para la operación", "No es urgente, puede esperar"],
               ["2", "Impacto bajo, aporta poca funcionalidad", "Poco urgente"],
               ["3", "Impacto medio, mejora procesos importantes", "Urgencia moderada"],
               ["4", "Impacto alto, necesario para operar", "Muy urgente"],
               ["5", "Impacto crítico, indispensable", "Debe implementarse de inmediato"]],
              x=0.75, y=1.75, ancho=11.85, alto=3.2,
              anchos=[1.5, 5.6, 4.75], tamano=ppt.Pt(16))
    ppt.parrafo(d, "El puntaje pondera el valor de negocio al 60 % y la urgencia al 40 %, "
                   "porque lo importante debe pesar más que lo afanado. Un requisito urgente "
                   "pero de bajo valor desplaza recursos de otro que sostiene la operación.",
                0.75, 5.3, 11.85, 1.0, tamano=ppt.Pt(18))


def conclusion_priorizacion(d):
    """Diapositiva 20."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Conclusión General de la Priorización")
    orden = sorted(
        ((codigo, nombre, round(sum(puntaje(v, u) for *_, v, u in reqs) / len(reqs), 1))
         for codigo, nombre, _, _, reqs in MODULOS),
        key=lambda x: -x[2])
    ppt.tabla(d,
              ["Código", "Módulo", "Puntaje"],
              [[c, n, f"{p}"] for c, n, p in orden],
              x=1.6, y=1.7, ancho=10.1, alto=3.9,
              anchos=[1.6, 6.5, 2.0], tamano=ppt.Pt(16))
    ppt.parrafo(d, f"Encabeza la lista {orden[0][1].lower()}, del que depende que un documento "
                   f"salga correctamente expedido, y cierra {orden[-1][1].lower()}, que agrupa "
                   "parámetros que se ajustan de vez en cuando.",
                0.9, 5.9, 11.5, 0.9, tamano=ppt.Pt(18))


def requisitos_funcionales(d):
    """Diapositiva 21."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Requisitos Funcionales")
    total = sum(len(r) for *_, r in MODULOS)
    criticos = sum(_criticos(r) for *_, r in MODULOS)
    ppt.tabla(d,
              ["Código", "Módulo", "Requisitos", "Críticos"],
              [[c, n, str(len(r)), str(_criticos(r))] for c, n, _, _, r in MODULOS]
              + [["", "Total", str(total), str(criticos)]],
              x=1.35, y=1.6, ancho=10.6, alto=4.3,
              anchos=[1.5, 5.4, 1.9, 1.8], tamano=ppt.Pt(15))
    ppt.parrafo(d, "Donde un sistema comercial tendría gestión de inventario y de compras, "
                   "aquí hay gestión de clientes API y de consumo y planes.",
                0.9, 6.15, 11.5, 0.7, tamano=ppt.Pt(18))


def requisitos_no_funcionales(d):
    """Diapositiva 22."""
    ppt.limpiar(d, imagenes=True)
    ppt.titulo(d, "Requisitos No Funcionales")
    categorias = {}
    for codigo, categoria, _, _ in RNF:
        categorias.setdefault(categoria, []).append(codigo)
    ejemplos = {
        "Seguridad": "Del secreto de las llaves solo se conserva su hash",
        "Integridad de los datos": "Dos documentos del mismo emisor no pueden compartir número",
        "Trazabilidad": "Toda escritura queda registrada y el rastro no se puede editar",
        "Rendimiento": "La emisión responde en menos de tres segundos",
        "Disponibilidad": "Un servicio externo caído no impide emitir",
        "Cumplimiento normativo": "El documento se genera bajo el estándar UBL 2.1",
        "Mantenibilidad": "La aritmética tributaria está implementada una sola vez",
        "Usabilidad": "Cada destino tiene un solo lugar en la navegación",
        "Escalabilidad": "Admite nuevas empresas emisoras sin cambios en el código",
        "Portabilidad": "Opera desde cualquier sistema operativo con un navegador",
        "Compatibilidad": "Funciona en los navegadores vigentes sin instalación local",
    }
    filas = [[categoria, str(len(codigos)), ejemplos.get(categoria, "")]
             for categoria, codigos in categorias.items()]
    ppt.tabla(d,
              ["Categoría", "N.º", "Ejemplo"],
              filas + [["Total", str(len(RNF)), ""]],
              x=0.75, y=1.55, ancho=11.85, alto=4.6,
              anchos=[3.1, 1.0, 7.75], tamano=ppt.Pt(14))
    ppt.parrafo(d, "Cada requisito indica cómo se comprueba, porque uno que no lo indica es "
                   "una aspiración y no un requisito.",
                0.75, 6.35, 11.85, 0.5, tamano=ppt.Pt(17), color=ppt.GRIS)


def escribir(presentacion):
    s = presentacion.slides
    encuesta_tecnica(s[11])
    historias_encuesta(s[12])
    rf_encuesta(s[13])
    observacion_tecnica(s[14])
    historias_observacion(s[15])
    rf_observacion(s[16])
    stakeholders(s[17])
    priorizacion(s[18])
    conclusion_priorizacion(s[19])
    requisitos_funcionales(s[20])
    requisitos_no_funcionales(s[21])


if __name__ == "__main__":
    import p1_formulacion
    p = ppt.abrir()
    p1_formulacion.escribir(p)
    escribir(p)
    print("Guardado:", ppt.guardar(p))
