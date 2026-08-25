"""
E4 — Capítulo 6, parte A. Implementación, estructura del proyecto y módulos.

Las capturas corresponden al sistema en funcionamiento con los datos de
demostración. Cada módulo se describe por lo que resuelve y no por los controles
que muestra la pantalla, porque una descripción que enumera botones envejece con el
primer cambio de interfaz y no explica para qué existe el módulo.
"""
from pathlib import Path

from apa import inicial_minuscula

CAPTURAS = Path(__file__).resolve().parent.parent / "documento para que te guies claude"

REQUERIMIENTOS = [
    ("Servidor de aplicación", "Procesador de dos núcleos, 4 GB de memoria RAM",
     "Procesador de cuatro núcleos, 8 GB de memoria RAM"),
    ("Almacenamiento", "20 GB disponibles",
     "50 GB en disco de estado sólido, con respaldo automático"),
    ("Sistema operativo del servidor", "Windows 10 o distribución Linux con soporte vigente",
     "Distribución Linux con soporte extendido"),
    ("Entorno de ejecución", "Python 3.11 o superior", "Python 3.13"),
    ("Gestor de base de datos", "MySQL 8.0", "MySQL 8.0 con réplica de lectura"),
    ("Servidor web", "Uvicorn", "Uvicorn detrás de un proxy inverso con HTTPS"),
    ("Equipo del usuario", "Cualquier equipo con navegador vigente y 4 GB de memoria",
     "Pantalla de 1366 × 768 o superior"),
    ("Navegador", "Chrome, Firefox o Edge en versión vigente", "Chrome o Edge actualizado"),
    ("Conexión a internet", "2 Mbps simétricos", "10 Mbps simétricos con respaldo"),
    ("Servicio de correo", "Cuenta SMTP con autenticación",
     "Servicio de envío transaccional con registro de entrega"),
]

MODULOS = [
    ("Panel de control", "modulo panel de control.png",
     "Es la primera pantalla al ingresar y reúne los indicadores de la operación en el "
     "periodo seleccionado. Está dividido en dos secciones, y el orden entre ellas responde "
     "a lo que la empresa hace, porque primero va el servicio prestado y después su cobro.",
     "La sección del servicio presenta los documentos emitidos por cuenta de los clientes "
     "integrados, cuántos clientes emitieron, el porcentaje de aceptación ante la "
     "administración tributaria y el ingreso recurrente del periodo. La sección de la venta "
     "presenta las ventas netas, lo efectivamente cobrado, la cartera pendiente y el ingreso "
     "por plan.",
     "Todas las cifras respetan el filtro de periodo, incluidas las del servicio. La "
     "excepción es el consumo del cupo, que va por mes en curso y así lo advierte en "
     "pantalla, porque el cupo se agota por mes calendario y recortarlo a una ventana móvil "
     "daría un consumo que no corresponde con el que se le factura al cliente. Un indicador "
     "que no se mueve cuando el rango cambia está midiendo algo distinto de lo que su rótulo "
     "anuncia."),

    ("Clientes API", "modulo Clientes api.png",
     "Administra las empresas integradas con la plataforma. Desde aquí se dan de alta, se "
     "les asigna el plan y la empresa emisora con la que numeran, y se administra la llave "
     "con la que su sistema se autentica.",
     "El listado permite buscar por nombre o por NIT y filtrar por plan y por estado. Cada "
     "cliente muestra su consumo del mes, de manera que se identifica de un vistazo a quién "
     "conviene ofrecerle el plan siguiente.",
     "La llave completa se muestra una sola vez, en el momento de generarla, porque de su "
     "secreto solo se conserva el hash. Si el integrador la pierde, no se recupera y hay que "
     "rotarla, operación que invalida la anterior de inmediato y queda registrada en "
     "auditoría sin que la credencial entre en el registro."),

    ("Documentos emitidos", "modulo documentos emitidos.png",
     "Muestra en tiempo real lo que las empresas integradas están emitiendo a través de la "
     "plataforma. Es la ventana sobre la operación del servicio.",
     "Cada documento presenta el cliente por cuenta del cual se emitió, el tipo, el número "
     "con su prefijo, la fecha, el valor y el estado ante la administración tributaria. Los "
     "filtros permiten acotar por cliente, por tipo de documento, por estado y por rango de "
     "fechas.",
     "Desde el detalle de cada documento se descargan su representación gráfica y su archivo "
     "XML, y se consulta la bitácora de eventos, donde consta qué ocurrió con él y cuándo. "
     "Esa bitácora es lo que permite responder cuando un cliente reporta que su comprador no "
     "recibió el documento, porque ahí queda anotado si el correo salió, se omitió o falló."),

    ("Consumo y planes", "modulo consumo y planes.png",
     "Controla cuántos documentos ha emitido cada cliente contra el cupo de su plan y "
     "convierte ese consumo en la facturación mensual del servicio.",
     "El listado muestra, por cliente, el plan contratado, los documentos emitidos en el "
     "periodo y la proporción de cupo consumida. Los clientes próximos al límite quedan "
     "señalados, lo que permite ofrecerles el plan siguiente antes de que una emisión les "
     "sea rechazada.",
     "El periodo que se factura es el último mes cerrado y no el mes en curso, porque hasta "
     "que el mes no termina no se sabe cuántos documentos emitió el cliente ni cuánto "
     "excedente acumuló. Desde aquí se emite la mensualidad, que el sistema expide llamando "
     "a su propia API, de modo que la factura del plan lleva un número y un código único "
     "reales y no una numeración aparte."),

    ("Nueva factura", "modulo nueva factura.png",
     "Es el formulario con el que el proveedor factura sus planes y servicios a sus propios "
     "clientes.",
     "Está organizado en tres momentos, que son a quién se le factura, qué se le factura y "
     "cómo paga, con el resumen de totales visible de forma permanente. La búsqueda de "
     "clientes y de servicios se resuelve sin recargar la página, y los totales se recalculan "
     "a medida que se agregan líneas.",
     "La disposición responde a un hallazgo de la observación directa, y es que el registro "
     "de una venta toma pocos segundos, de modo que una pantalla que obligue a avanzar y "
     "retroceder para verificar una cifra termina siendo rechazada por quien la usa."),

    ("Planes y servicios", "modulo planes y servicios.png",
     "Mantiene el catálogo de lo que el proveedor vende, que son los planes de suscripción, "
     "el documento adicional que se cobra por encima del cupo y los servicios de enganche.",
     "Cada elemento del catálogo lleva su precio, su unidad y el impuesto que le corresponde. "
     "Subir una tarifa consiste en editar un elemento del catálogo y no en migrar datos, "
     "porque el precio vive aquí y no en cada cliente.",
     "Todo el catálogo está marcado como servicio y no descuenta existencias, lo que "
     "distingue a esta plataforma de un sistema comercial, porque un proveedor tecnológico no "
     "tiene bodega."),

    ("Reportes", "modulo reportes.png",
     "Permite generar los siete reportes del sistema y exportarlos para su análisis fuera de "
     "la plataforma.",
     "Los reportes disponibles son ventas por periodo, cartera por cobrar, productos más "
     "vendidos, clientes por facturación, resumen tributario, facturación por estado de pago "
     "y facturación por usuario. Cada uno admite un rango de fechas y, según el rol, la "
     "empresa sobre la que se consulta.",
     "Cualquier reporte se descarga en CSV o en PDF conservando los filtros aplicados, y el "
     "documento exportado incluye el subtítulo con el rango consultado, de modo que un "
     "archivo guardado meses atrás sigue diciendo a qué periodo corresponde."),
]


def escribir(d):
    d.titulo("Capítulo 6. Desarrollo, implementación, pruebas y resultados", nivel=1,
             nueva_pagina=True)
    _requerimientos(d)
    _descripcion(d)
    _estructura(d)
    _modulos(d)


def _requerimientos(d):
    d.titulo("6.1 Requerimientos técnicos de implementación", nivel=2)
    d.parrafo(
        "Se relacionan las condiciones de infraestructura necesarias para poner el sistema en "
        "funcionamiento. La columna de requerimiento mínimo corresponde a lo que permite "
        "operar, y la de recomendado a lo que conviene para un servicio en producción con "
        "varias empresas integradas emitiendo de manera simultánea."
    )
    d.tabla(
        "Requerimientos técnicos de implementación",
        ["Componente", "Mínimo", "Recomendado"],
        [[c, m, r] for c, m, r in REQUERIMIENTOS],
        nota="Elaboración propia.",
        anchos=[4.6, 6.0, 5.7],
    )
    d.parrafo(
        "Dos de estos requerimientos merecen aclaración. El servicio de correo aparece como "
        "requerimiento porque la normativa exige que el documento llegue al comprador, aunque "
        "su ausencia no impide emitir, ya que el intento queda anotado y la emisión se "
        "completa igual. Y el proxy inverso con HTTPS aparece en la columna de recomendado "
        "porque en producción la llave de la API viaja en cada petición, y sobre una conexión "
        "sin cifrar esa credencial quedaría expuesta."
    )


def _descripcion(d):
    d.titulo("6.2 Descripción general del sistema", nivel=2, nueva_pagina=True)
    d.parrafo(
        "FactuGest es una aplicación web que presenta dos caras sobre una misma capa de "
        "lógica de negocio. La primera es un panel con el que el personal del proveedor "
        "administra clientes, planes, facturación y reportes. La segunda es una interfaz de "
        "integración que los sistemas de las empresas clientes consumen para emitir sus "
        "documentos electrónicos."
    )
    d.parrafo(
        "El recorrido completo de una emisión ilustra cómo trabaja el sistema. El punto de "
        "venta de una empresa integrada envía los datos de una venta con su llave de acceso. "
        "La plataforma identifica al cliente por esa llave, comprueba que le quede cupo en el "
        "mes, abre una transacción, reserva el siguiente número autorizado de la resolución "
        "del emisor, calcula bases gravables, descuentos e impuestos, guarda la cabecera y el "
        "detalle, genera el código único, la representación gráfica y el archivo XML, y "
        "responde con el número y el código. Después de haber respondido, y ya fuera de la "
        "transacción, envía el documento al comprador."
    )
    d.parrafo(
        "El orden de esos pasos no es accidental. La comprobación del cupo va antes de "
        "reservar el número porque la numeración de una resolución es un recurso autorizado y "
        "finito. Toda la operación va dentro de una transacción para que un fallo a mitad de "
        "camino no deje un documento incompleto ni gaste un consecutivo. Y el envío al "
        "comprador queda fuera de ella porque el documento ya es válido, de modo que un "
        "servidor de correo que no responda no puede impedir que una empresa facture."
    )
    d.parrafo(
        "Sobre esa operación el sistema construye su propio negocio. Cuenta los documentos "
        "que cada cliente emitió en el mes, los compara con el cupo de su plan, y al cerrar "
        "el periodo permite facturar la mensualidad correspondiente junto con los documentos "
        "excedentes. Esa facturación se emite llamando a la propia interfaz de integración, "
        "con lo cual el proveedor utiliza su servicio en las mismas condiciones que sus "
        "clientes."
    )


def _estructura(d):
    d.titulo("6.3 Estructura del proyecto", nivel=2, nueva_pagina=True)
    d.parrafo(
        "El proyecto está organizado en carpetas que corresponden a las responsabilidades "
        "descritas en la arquitectura del capítulo anterior. Esa correspondencia es "
        "deliberada, porque una estructura de carpetas que no refleja la arquitectura obliga "
        "a explicar dos veces lo mismo y termina divergiendo."
    )
    d.figura(
        "Estructura de carpetas del proyecto",
        CAPTURAS / "estructura del proyecto.png",
        nota="Elaboración propia. Organización del repositorio del sistema.",
    )
    d.vinetas([
        ("routes/", "un archivo por dominio, con las rutas de la aplicación web. Dentro está "
                    "api/v1/, que agrupa las operaciones de la interfaz de integración."),
        ("services/", "la lógica de negocio, que es la capa que alimenta por igual a las "
                      "rutas web y a las de la API."),
        ("templates/", "las plantillas de la interfaz, con un archivo base del que heredan "
                       "las demás y una carpeta por dominio."),
        ("static/", "hojas de estilo, guiones de navegador e imágenes."),
        ("tests/", "las pruebas automatizadas."),
        ("base/", "el esquema de la base de datos y los catálogos iniciales."),
        ("main.py", "el punto de entrada, donde se registran los routers y los middleware."),
        ("migrate.py", "el aplicador de migraciones, que lleva el esquema al día y registra "
                       "lo aplicado."),
    ])
    d.parrafo(
        "La regla que sostiene esta organización es que las rutas se limitan a recibir y "
        "responder. Una regla de negocio escrita dentro de una ruta es una regla que la otra "
        "entrada no tiene, y comprobarlo fue parte de la revisión de cada sprint."
    )


def _modulos(d):
    d.titulo("6.4 Módulos del sistema", nivel=2, nueva_pagina=True)
    d.parrafo(
        "Se describen a continuación los siete módulos principales de la plataforma, con una "
        "captura de cada uno tomada del sistema en funcionamiento. Los módulos de "
        "configuración, usuarios y auditoría no se documentan aquí por separado, ya que "
        "agrupan catálogos y parámetros cuyo comportamiento es el mismo en todos los casos."
    )
    for indice, (nombre, imagen, que_es, que_muestra, decision) in enumerate(MODULOS, start=1):
        d.titulo(f"6.4.{indice} Módulo de {inicial_minuscula(nombre)}", nivel=3,
                 nueva_pagina=(indice > 1))
        d.parrafo(que_es)
        d.figura(
            f"Módulo de {inicial_minuscula(nombre)}",
            CAPTURAS / imagen,
            nota="Elaboración propia. Captura del sistema en funcionamiento con datos de "
                 "demostración.",
        )
        d.parrafo(que_muestra)
        d.parrafo(decision)
