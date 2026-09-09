"""
La evidencia del informe, recogida del sistema y no escrita a mano.

Los capítulos importan de aquí en vez de repetir cifras en su propio texto. El
motivo es concreto: el informe afirma que hay 190 pruebas en verde, y esa cifra
aparece en el resumen, en el plan y en la tabla de resultados. Escrita tres veces,
la primera vez que alguien agregue una prueba el informe se contradice a sí mismo.

Los 32 requisitos no funcionales tampoco se copian, se importan del entregable donde
ya estaban, `docs expo/generador/e1_requisitos.py`.

Recogido el 8 de septiembre de 2026 con la corrida guardada en
`calidad-documentos/evidencia/pytest_salida.txt`.
"""
from comun import GENERADOR_GRADO                       # noqa: F401  (fija el sys.path)
from e1_requisitos import RNF                           # noqa: E402

FECHA_CORRIDA = "8 de septiembre de 2026"
HERRAMIENTA = "pytest 9.1.1 sobre Python 3.13.3"
DURACION = "3,39 segundos"

# (archivo, pruebas, qué protege). Las cifras salen de la corrida guardada, no de
# contar las funciones del archivo: las pruebas parametrizadas valen por varias.
UNITARIAS = [
    ("test_validaciones.py", 45,
     "Las reglas de validación del dominio, desde el formato de un correo hasta el "
     "dígito de verificación del NIT y el orden de las fechas de una resolución"),
    ("test_dian_proveedor.py", 24,
     "El adaptador del proveedor de facturación electrónica, que además deja escrito "
     "el contrato que tendrá que cumplir el proveedor real"),
    ("test_modelos_api.py", 22,
     "El contrato de entrada de la API, comprobando que aplica las mismas reglas que "
     "el formulario web y no unas propias"),
    ("test_calculo_documento.py", 19,
     "La aritmética tributaria, con bases gravables, descuentos de línea y de factura "
     "y prorrateo del impuesto"),
    ("test_calculo_notas.py", 16,
     "La aritmética de las notas crédito y débito, que es donde un redondeo mal puesto "
     "se convierte en dinero a favor o en contra de alguien"),
    ("test_monograma.py", 13,
     "El distintivo de la empresa que no cargó logo, que debe ser siempre el mismo para "
     "el mismo nombre"),
    ("test_api_key_service.py", 11,
     "La generación y el formato de las llaves de la API, con sus propiedades "
     "criptográficas"),
    ("test_pdf_membrete.py", 10,
     "Que el membrete del PDF sea el del emisor del documento y nunca el de FactuGest"),
    ("test_consumo_service.py", 9,
     "El cálculo del excedente sobre el cupo del plan y el aviso previo al cliente"),
    ("test_xml_service.py", 9,
     "El XML bajo el estándar UBL 2.1 en los puntos donde el emisor cambia la salida"),
    ("test_documento_canonico.py", 6,
     "El contrato de entrada que comparten el generador de PDF y el de XML"),
    ("test_pdf_descuentos.py", 6,
     "Que cada descuento salga en el pie de la factura con el porcentaje de la base que "
     "de verdad le corresponde"),
]

TOTAL_UNITARIAS = sum(n for _, n, _ in UNITARIAS)

# (número, nombre, método, ruta, qué comprueba)
INTEGRACION = [
    (1, "Comprobar la llave", "GET", "/api/v1/ping",
     "Que la llave sirve y con qué emisor va a numerar quien integra"),
    (2, "Emitir una factura", "POST", "/api/v1/facturas",
     "La emisión completa, con el número, el código único y los enlaces al PDF y al XML"),
    (3, "Reintentar la misma venta", "POST", "/api/v1/facturas",
     "La idempotencia, pues la misma petición devuelve la factura existente sin gastar "
     "otro número de la resolución"),
    (4, "Consultar un documento", "GET", "/api/v1/documentos/{id}",
     "La reconciliación cuando el sistema del cliente perdió la respuesta"),
    (5, "Descargar el PDF", "GET", "/api/v1/documentos/{id}/pdf",
     "La representación gráfica del documento"),
    (6, "Descargar el XML", "GET", "/api/v1/documentos/{id}/xml",
     "El archivo con validez legal, tal como se transmitió"),
    (7, "Listar los documentos del mes", "GET", "/api/v1/documentos",
     "El listado con filtros de tipo y fecha, paginado, para la conciliación"),
    (8, "Nota crédito, anular la factura", "POST", "/api/v1/notas-credito",
     "La anulación total, que se queda con los precios de la factura original"),
    (9, "Nota crédito, devolución parcial", "POST", "/api/v1/notas-credito",
     "La devolución de parte de una línea, con su base, su descuento y su impuesto "
     "proporcionales"),
    (10, "Nota débito, cobrar un adicional", "POST", "/api/v1/notas-debito",
     "El cobro posterior, con el impuesto incluido en el valor o sumado encima"),
    (11, "Un error, para ver su forma", "GET", "/api/v1/ping",
     "Que todos los errores salgan con la misma forma, del 401 al 500"),
]

COLECCION = "Factugest/docs/FactuGest.postman_collection.json"

# (operación, captura del formulario, captura del resultado)
FUNCIONALES = [
    ("Registrar un servicio del catálogo",
     "Registro de servicios.png", "registro de servicios emitidos.png"),
    ("Registrar un cliente",
     "registro de nuevo cliente.png", "registro de nuevo cliente emitido.png"),
    ("Emitir una factura",
     "registro de nueva factura.png", "registro de nueva factura emitida.png"),
    ("Registrar un usuario",
     "registro de nuevo usuario.png", "registro de nuevo usuario emitido.png"),
]

CARPETA_CAPTURAS = "docs expo/documento para que te guies claude"

# (defecto, consecuencia que tenía, cómo quedó cubierto)
DEFECTOS = [
    ("El PDF de un documento emitido por la API salía con el nombre, el logo y el color "
     "de FactuGest",
     "La factura de una clínica parecía expedida por nosotros, que es lo más grave que "
     "puede decir mal un documento fiscal",
     "El emisor pasó a ser un argumento explícito del generador, cubierto por las 10 "
     "pruebas de test_pdf_membrete.py"),
    ("El pie de la factura sumaba el descuento de línea con el de factura en una sola "
     "fila y la rotulaba con el porcentaje del segundo",
     "Cuando la rebaja venía de las líneas, la factura mostraba un descuento del 0,0 % "
     "restando dinero real",
     "Cada descuento salió a su propia fila con su porcentaje sobre la base que le "
     "corresponde, cubierto por las 6 pruebas de test_pdf_descuentos.py"),
    ("La ciudad y el departamento del comprador llegaban vacíos en todo lo emitido por "
     "la API",
     "La consulta del receptor pedía dos nombres que no son columnas de esa tabla, que "
     "guarda el municipio por código",
     "La consulta resuelve el código contra los catálogos de municipios y departamentos. "
     "Verificado en el documento emitido, pues comprobarlo automáticamente exige base "
     "de datos"),
    ("Las columnas de dinero de la tabla de líneas partían los importes de ocho cifras",
     "El impuesto de una factura corriente salía como «1,123,470.0» con un cero solitario "
     "debajo, o sea una cantidad que no se puede leer",
     "El ancho se midió con la propia función de medición de la librería y el espacio se "
     "tomó de la columna de descripción, que sí puede repartirse en varias líneas"),
]

# Invariantes del sistema que las pruebas y el diseño protegen. Salen de CLAUDE.md.
INVARIANTES = [
    ("Numeración", "El consecutivo se reserva en una sola sentencia de actualización, y "
     "la tabla tiene un índice único por emisor, tipo y número. Dos documentos con el "
     "mismo número de una resolución son dos rechazos"),
    ("Emisión atómica", "Reservar el número, guardar la cabecera, guardar el detalle y "
     "mover el inventario van dentro de una transacción, de modo que un fallo a mitad no "
     "deja rastro y el consecutivo queda libre"),
    ("Cálculo", "La aritmética tributaria vive en un solo módulo, que es el que alimenta "
     "por igual al formulario web y a la API, y es el que está cubierto por pruebas"),
    ("Inventario", "Toda modificación de existencias pasa por su servicio y deja su fila "
     "en el kardex, de modo que el saldo siempre es reconstruible"),
    ("Membrete", "El documento lleva siempre el emisor que lo expide, nunca el del "
     "proveedor tecnológico"),
    ("Auditoría", "El registro solo se escribe, nunca se corrige, guarda el nombre del "
     "usuario y no puede tumbar la operación que está anotando"),
]

# Lo que no se ha ejecutado. Va al informe como planificado, con esas palabras.
PENDIENTES = [
    ("Rendimiento", "Medición del tiempo de respuesta de la emisión bajo carga",
     "Menos de tres segundos por documento, según el primer requisito no funcional"),
    ("Seguridad automatizada", "Análisis con herramienta sobre las dependencias y las "
     "entradas de la API",
     "Ninguna vulnerabilidad de severidad alta sin tratar"),
    ("Regresión continua", "Ejecución de la suite en cada envío de cambios",
     "La suite completa en verde antes de integrar"),
    ("Validación con el proveedor", "Transmisión real contra la plataforma habilitada",
     "El documento aceptado por la autoridad tributaria con su acuse"),
]


def resumen():
    return {
        "unitarias": TOTAL_UNITARIAS,
        "archivos": len(UNITARIAS),
        "integracion": len(INTEGRACION),
        "funcionales": len(FUNCIONALES),
        "rnf": len(RNF),
        "defectos": len(DEFECTOS),
    }


if __name__ == "__main__":
    for clave, valor in resumen().items():
        print(f"{clave:14} {valor}")
