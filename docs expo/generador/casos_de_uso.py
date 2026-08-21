"""
Catálogo de casos de uso de FactuGest — **fuente única**.

De aquí salen los diagramas (E2) y las fichas de documentación (E3). Tenerlo en un
solo lugar no es prolijidad: son dos documentos que hablan de lo mismo, y cuando
cada uno mantiene su propia lista, basta un caso agregado en uno para que el otro
quede describiendo un sistema que ya no existe. Un diagrama con ocho elipses y una
documentación con nueve fichas es un error que nadie nota hasta la sustentación.

Cada caso se enuncia como un **objetivo del actor**, no como una operación de la
base: «Gestionar impuestos» y no «Insertar, actualizar y eliminar impuesto». Por eso
hay 56 casos de uso frente a 82 requisitos funcionales; la correspondencia entre
unos y otros queda anotada en el campo `rf`.
"""

# (código, nombre, [actores], descripción, requisitos que cubre)

M1 = [
    ("CU-01", "Registrar cliente API", ["Administrador"],
     "Dar de alta una empresa que se integra con la plataforma, con su plan y su empresa "
     "emisora.", "RF 1.1"),
    ("CU-02", "Generar llave de acceso", ["Administrador"],
     "Producir la credencial con la que el sistema del cliente se identificará ante la API.",
     "RF 1.2, RF 1.3"),
    ("CU-03", "Consultar clientes API", ["Administrador"],
     "Revisar los clientes integrados, buscarlos y filtrarlos por plan y estado.",
     "RF 1.4, RF 1.5"),
    ("CU-04", "Editar cliente y plan", ["Administrador"],
     "Modificar los datos del cliente, cambiarlo de plan o ajustar su cupo mensual.",
     "RF 1.6"),
    ("CU-05", "Cambiar estado del cliente", ["Administrador"],
     "Suspender, reactivar o revocar el acceso de un cliente integrado.", "RF 1.7"),
    ("CU-06", "Rotar llave de acceso", ["Administrador"],
     "Reemplazar la llave vigente por una nueva e invalidar la anterior.", "RF 1.8"),
    ("CU-07", "Eliminar cliente API", ["Administrador"],
     "Retirar del sistema un cliente integrado que no tiene operación asociada.", "RF 1.9"),
]

M2 = [
    ("CU-08", "Emitir factura de venta", ["Sistema cliente", "Cajero"],
     "Expedir una factura de venta electrónica por cuenta de la empresa emisora.",
     "RF 2.1"),
    ("CU-09", "Emitir nota crédito", ["Sistema cliente", "Administrador"],
     "Expedir una nota crédito que corrige una factura ya emitida.", "RF 2.2"),
    ("CU-10", "Emitir nota débito", ["Sistema cliente", "Administrador"],
     "Expedir una nota débito por un mayor valor sobre una factura ya emitida.", "RF 2.3"),
    ("CU-11", "Reservar consecutivo", [],
     "Tomar el siguiente número autorizado de la resolución del emisor.", "RF 2.4"),
    ("CU-12", "Calcular totales del documento", [],
     "Determinar bases, descuentos, prorrateo de IVA y totales del documento.", "RF 2.5"),
    ("CU-13", "Generar PDF y XML", [],
     "Producir la representación gráfica y el archivo XML UBL 2.1 con el CUFE.",
     "RF 2.6, RF 2.7, RF 2.8"),
    ("CU-14", "Enviar documento al comprador", ["Comprador"],
     "Hacer llegar el PDF y el XML al correo del comprador.", "RF 2.10"),
    ("CU-15", "Consultar documentos emitidos", ["Administrador", "Supervisor"],
     "Revisar lo emitido por cuenta de terceros con filtros por cliente, tipo y fecha.",
     "RF 2.12"),
    ("CU-16", "Descargar PDF y XML", ["Administrador", "Supervisor"],
     "Obtener los archivos de un documento ya emitido.", "RF 2.13"),
]

M3 = [
    ("CU-17", "Consultar consumo del cupo", ["Administrador"],
     "Revisar cuántos documentos lleva emitidos cada cliente contra el cupo de su plan.",
     "RF 3.1, RF 3.2"),
    ("CU-18", "Validar cupo disponible", [],
     "Comprobar que al cliente le queda cupo antes de dejarlo emitir una factura.",
     "RF 3.3, RF 3.4"),
    ("CU-19", "Consultar mensualidades por cobrar", ["Administrador"],
     "Revisar a qué clientes no se les ha facturado el mes ya cerrado.",
     "RF 3.6, RF 3.7"),
    ("CU-20", "Facturar mensualidad", ["Administrador"],
     "Emitir la factura del plan de un cliente por el periodo correspondiente.",
     "RF 3.8, RF 3.9"),
    ("CU-21", "Calcular excedentes del periodo", [],
     "Valorar los documentos emitidos por encima del cupo incluido en el plan.", "RF 3.10"),
    ("CU-22", "Revisar alertas de cupo", ["Administrador"],
     "Identificar los clientes próximos a agotar el cupo de su plan.", "RF 3.5"),
]

M4 = [
    ("CU-23", "Emitir factura propia", ["Administrador", "Cajero"],
     "Facturar un plan o un servicio del catálogo a un cliente del proveedor.", "RF 4.1"),
    ("CU-24", "Gestionar clientes", ["Administrador", "Cajero"],
     "Registrar, consultar, actualizar y eliminar los clientes a los que se factura.",
     "RF 4.2"),
    ("CU-25", "Gestionar planes y servicios", ["Administrador"],
     "Mantener el catálogo de planes y servicios con su precio, unidad e impuesto.",
     "RF 4.3, RF 4.4"),
    ("CU-26", "Registrar pago de factura", ["Administrador"],
     "Anotar un pago recibido, total o parcial, sobre una factura emitida.", "RF 4.6"),
    ("CU-27", "Actualizar estado de pago", ["Administrador"],
     "Cambiar el estado de una factura entre pagada, pendiente, vencida u otro.", "RF 4.7"),
    ("CU-28", "Emitir nota sobre factura propia", ["Administrador"],
     "Expedir una nota crédito o débito referida a una factura del proveedor.", "RF 4.8"),
    ("CU-29", "Consultar facturas", ["Administrador", "Supervisor", "Cajero"],
     "Buscar y filtrar las facturas emitidas por el proveedor.", "RF 4.9"),
    ("CU-30", "Descargar factura propia", ["Administrador", "Supervisor"],
     "Obtener el PDF y el XML de una factura del proveedor.", "RF 4.10"),
]

M5 = [
    ("CU-31", "Consultar tablero de control", ["Administrador", "Jefe de tienda"],
     "Revisar los indicadores del servicio y de la venta en el periodo seleccionado.",
     "RF 5.1, RF 5.2"),
    ("CU-32", "Filtrar por periodo y empresa", [],
     "Acotar las cifras del tablero a un rango de fechas y a una empresa emisora.",
     "RF 5.3, RF 5.4, RF 5.5"),
    ("CU-33", "Generar reporte", ["Administrador", "Supervisor"],
     "Producir cualquiera de los siete reportes del sistema con los filtros indicados.",
     "RF 5.7"),
    ("CU-34", "Exportar reporte a CSV", ["Administrador", "Supervisor"],
     "Descargar el reporte en formato de valores separados por comas.", "RF 5.8"),
    ("CU-35", "Exportar reporte a PDF", ["Administrador", "Supervisor"],
     "Descargar el reporte en formato PDF conservando los filtros aplicados.", "RF 5.8"),
    ("CU-36", "Consultar panel operativo", ["Cajero"],
     "Revisar la vista reducida del panel, sin cifras financieras.", "RF 5.9"),
]

M6 = [
    ("CU-37", "Consultar centro de configuración", ["Administrador"],
     "Revisar en una sola pantalla los catálogos del sistema y su conteo.", "RF 6.1"),
    ("CU-38", "Gestionar impuestos", ["Administrador"],
     "Mantener el catálogo de impuestos con su tarifa y su código DIAN.", "RF 6.2"),
    ("CU-39", "Gestionar descuentos", ["Administrador"],
     "Mantener el catálogo de descuentos aplicables a la facturación.", "RF 6.3"),
    ("CU-40", "Gestionar métodos y estados de pago", ["Administrador"],
     "Mantener los métodos de pago admitidos y los estados que puede tomar una factura.",
     "RF 6.4, RF 6.8"),
    ("CU-41", "Gestionar empresas emisoras", ["Administrador"],
     "Registrar y mantener las empresas emisoras con su resolución, prefijo y rango.",
     "RF 6.5"),
    ("CU-42", "Configurar marca de la empresa", ["Administrador"],
     "Cargar el logo y definir el color con que se identifica la empresa emisora.",
     "RF 6.6, RF 6.7"),
]

M7 = [
    ("CU-43", "Iniciar sesión", ["Administrador", "Supervisor", "Jefe de tienda", "Cajero"],
     "Acceder al panel presentando las credenciales del usuario.", "RF 7.1, RF 7.2"),
    ("CU-44", "Cerrar sesión", ["Administrador", "Supervisor", "Jefe de tienda", "Cajero"],
     "Terminar la sesión, por decisión del usuario o por inactividad.", "RF 7.5, RF 7.6"),
    ("CU-45", "Gestionar usuarios", ["Administrador"],
     "Registrar, consultar, actualizar y eliminar los usuarios del panel.", "RF 7.7"),
    ("CU-46", "Asignar rol y empresa", ["Administrador"],
     "Determinar el rol de cada usuario y la empresa sobre la que trabaja.",
     "RF 7.3, RF 7.4"),
    ("CU-47", "Cambiar foto de perfil", ["Administrador", "Supervisor", "Jefe de tienda",
                                         "Cajero"],
     "Actualizar la fotografía propia o la de un usuario de menor jerarquía.", "RF 7.8"),
    ("CU-48", "Registrar operación en auditoría", [],
     "Anotar quién realizó cada operación de escritura, cuándo y sobre qué.",
     "RF 7.9, RF 7.10"),
    ("CU-49", "Consultar auditoría", ["Administrador"],
     "Revisar el rastro de operaciones con filtros por usuario, acción y fecha.", "RF 7.11"),
]

M8 = [
    ("CU-50", "Autenticar por llave", ["Sistema cliente"],
     "Identificar al cliente integrado a partir de la llave enviada en la petición.",
     "RF 8.1, RF 8.2"),
    ("CU-51", "Emitir documento por API", ["Sistema cliente"],
     "Solicitar la expedición de una factura o de una nota desde un sistema externo.",
     "RF 8.4, RF 8.5"),
    ("CU-52", "Consultar documentos por API", ["Sistema cliente"],
     "Obtener el listado de los documentos emitidos y el detalle de cualquiera de ellos.",
     "RF 8.7"),
    ("CU-53", "Descargar archivos por API", ["Sistema cliente"],
     "Obtener el PDF o el XML de un documento a través de la interfaz de integración.",
     "RF 8.8"),
    ("CU-54", "Verificar llave", ["Sistema cliente"],
     "Comprobar que la llave quedó bien configurada antes de intentar emitir.", "RF 8.9"),
    ("CU-55", "Consultar contrato de la API", ["Sistema cliente"],
     "Obtener la especificación OpenAPI para construir la integración.", "RF 8.10"),
    ("CU-56", "Reenviar emisión con la misma referencia", ["Sistema cliente"],
     "Repetir una emisión sin duplicar el documento, obteniendo el ya expedido.",
     "RF 8.6, RF 8.3"),
]

# (código del módulo, nombre, actores a la izquierda, actores a la derecha, casos,
#  inclusiones, extensiones, descripción del diagrama)

MODULOS = [
    ("DCU-01", "Gestión de clientes API",
     ["Administrador"], ["Sistema cliente"], M1,
     [("CU-01", "CU-02")], [],
     "Recoge la administración de las empresas integradas. La generación de la llave se "
     "modela como caso incluido porque no ocurre por decisión aparte: registrar un cliente "
     "sin llave no lo deja en condiciones de emitir."),

    ("DCU-02", "Gestión de documentos electrónicos",
     ["Sistema cliente", "Cajero"], ["Administrador", "Supervisor", "Comprador"], M2,
     [("CU-08", "CU-11"), ("CU-08", "CU-12"), ("CU-08", "CU-13"),
      ("CU-09", "CU-12"), ("CU-10", "CU-12")],
     [("CU-14", "CU-08")],
     "Es el núcleo del sistema. Los tres casos de emisión comparten los pasos que hacen "
     "válido a un documento —el consecutivo, el cálculo y los dos archivos—, que por eso se "
     "modelan como casos incluidos y no se repiten en cada uno. El envío al comprador se "
     "modela como extensión: ocurre después de que la emisión terminó y su resultado no "
     "condiciona el del documento."),

    ("DCU-03", "Gestión de consumo y planes",
     ["Administrador"], ["Sistema cliente"], M3,
     [("CU-20", "CU-21")], [("CU-18", "CU-17")],
     "Une el control del cupo con el cobro de la suscripción. La validación del cupo aparece "
     "aquí porque es donde se decide, aunque quien la dispara sea la emisión de una factura "
     "en el diagrama anterior."),

    ("DCU-04", "Gestión de facturación y cartera propias",
     ["Administrador", "Cajero"], ["Supervisor"], M4,
     [], [("CU-26", "CU-27")],
     "Cubre la venta del proveedor: su catálogo de planes, sus clientes, sus facturas y el "
     "recaudo. El registro de un pago extiende la actualización del estado porque un abono "
     "parcial no siempre cambia el estado de la factura."),

    ("DCU-05", "Gestión de reportes y tablero de control",
     ["Administrador", "Jefe de tienda"], ["Supervisor", "Cajero"], M5,
     [("CU-31", "CU-32"), ("CU-33", "CU-32")],
     [("CU-34", "CU-33"), ("CU-35", "CU-33")],
     "El filtro de periodo y empresa se modela como caso incluido porque tanto el tablero "
     "como los reportes lo aplican siempre; las exportaciones extienden la generación del "
     "reporte, ya que se ejecutan sobre uno ya producido."),

    ("DCU-06", "Gestión de configuración y catálogos",
     ["Administrador"], [], M6, [], [],
     "Reúne los parámetros que se ajustan de vez en cuando. Todos sus casos corresponden a "
     "un mismo actor porque son ajustes de la plataforma, no trabajo de operación."),

    ("DCU-07", "Gestión de seguridad y auditoría",
     ["Administrador", "Supervisor"], ["Jefe de tienda", "Cajero"], M7,
     [("CU-45", "CU-48"), ("CU-46", "CU-48")], [],
     "El registro en auditoría se modela como caso incluido de las operaciones de escritura: "
     "no es una acción que alguien decida ejecutar, sino una consecuencia obligatoria de "
     "haber modificado algo."),

    ("DCU-08", "Integración mediante API REST",
     ["Sistema cliente"], [], M8,
     [("CU-51", "CU-50"), ("CU-52", "CU-50"), ("CU-53", "CU-50")],
     [("CU-56", "CU-51")],
     "Presenta el sistema desde la perspectiva del integrador. Los casos de emisión y "
     "consulta ya aparecieron en los diagramas anteriores como capacidades del negocio; aquí "
     "se muestran como operaciones de la interfaz, con la autenticación por llave incluida en "
     "todas ellas."),
]

GENERAL = [
    ("Gestionar clientes API", ["Administrador"]),
    ("Emitir documentos electrónicos", ["Sistema cliente", "Cajero"]),
    ("Controlar consumo y planes", ["Administrador"]),
    ("Facturar y recaudar", ["Administrador", "Cajero"]),
    ("Consultar reportes y tablero", ["Administrador", "Jefe de tienda", "Supervisor"]),
    ("Configurar la plataforma", ["Administrador"]),
    ("Administrar seguridad y auditoría", ["Administrador"]),
    ("Integrar sistemas externos", ["Sistema cliente"]),
    ("Recibir documento electrónico", ["Comprador"]),
]


def todos():
    """Los 56 casos, en orden, con el módulo al que pertenecen."""
    salida = []
    for _, nombre_modulo, _, _, casos, *_ in MODULOS:
        for codigo, nombre, actores, descripcion, rf in casos:
            salida.append((codigo, nombre, nombre_modulo, actores, descripcion, rf))
    return salida


def por_nombre(casos):
    """Convierte la lista del catálogo al formato que espera el dibujante."""
    return [(nombre, actores) for _, nombre, actores, _, _ in casos]


def codigo_de(nombre):
    for codigo, otro, *_ in todos():
        if otro == nombre:
            return codigo
    raise KeyError(nombre)
