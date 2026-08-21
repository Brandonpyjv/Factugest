"""
E1 — Especificación de requisitos funcionales y no funcionales de FactuGest.

Documento aparte y **completo**: de aquí se extraen después los requisitos más
relevantes para el punto 4.4 del documento de grado. Se levantó recorriendo los 24
routers y los 33 servicios del sistema; no hay requisito que no corresponda a algo
que exista en el código.

**Los puntajes son la única fuente de la prioridad.** Cada requisito trae su valor
de negocio y su urgencia, y de ahí sale tanto la columna «Prioridad» del capítulo 3
como la tabla de priorización del capítulo 5. Si estuvieran escritos por separado,
el día que uno cambie el documento se contradiría a sí mismo.

    python e1_requisitos.py
"""
from pathlib import Path

from apa import DocumentoAPA, inicial_minuscula

SALIDA = Path(__file__).resolve().parent.parent / "entregables"
ARCHIVO = SALIDA / "FactuGest - Requisitos Funcionales y No Funcionales.docx"

# --- Cómo se calcula la prioridad ----------------------------------------------

def puntaje(valor, urgencia):
    """El valor de negocio pesa más que la urgencia, y lo importante manda sobre lo afanado."""
    return round(valor * 0.6 + urgencia * 0.4, 1)


def prioridad(valor, urgencia):
    p = puntaje(valor, urgencia)
    if p >= 4.6:
        return "Crítica"
    if p >= 4.0:
        return "Alta"
    if p >= 3.0:
        return "Media"
    return "Baja"


# --- Los requisitos -------------------------------------------------------------
# (código, requisito, descripción, actor, valor de negocio, urgencia)

RF1 = [
    ("RF 1.1", "Registro de cliente API",
     "Registrar una empresa integrada con su NIT, razón social, correo, plan contratado y "
     "empresa emisora asociada.", "Administrador", 5, 5),
    ("RF 1.2", "Generación de la llave de acceso",
     "Generar automáticamente una llave con el formato fg_live_<prefijo>.<secreto> al dar de "
     "alta al cliente.", "Sistema", 5, 5),
    ("RF 1.3", "Entrega de la llave una sola vez",
     "Mostrar el secreto de la llave únicamente en el momento de generarla; después solo se "
     "conserva su hash.", "Sistema", 5, 5),
    ("RF 1.4", "Listado de clientes API",
     "Consultar los clientes integrados con búsqueda por nombre o NIT y filtros por plan y por "
     "estado.", "Administrador", 4, 4),
    ("RF 1.5", "Detalle del cliente API",
     "Consultar los datos del cliente, su consumo del mes, su empresa emisora y el prefijo de "
     "su llave vigente.", "Administrador", 4, 4),
    ("RF 1.6", "Edición del cliente API",
     "Modificar los datos del cliente, cambiarlo de plan y ajustar su cupo mensual.",
     "Administrador", 4, 4),
    ("RF 1.7", "Cambio de estado del cliente",
     "Suspender, reactivar o revocar un cliente integrado sin borrar su historial de "
     "documentos.", "Administrador", 5, 4),
    ("RF 1.8", "Rotación de la llave",
     "Generar una llave nueva e invalidar la anterior, dejando registro del cambio sin guardar "
     "la credencial.", "Administrador", 5, 4),
    ("RF 1.9", "Eliminación del cliente API",
     "Eliminar un cliente integrado siempre que no comprometa la trazabilidad de lo ya "
     "emitido.", "Administrador", 3, 2),
]

RF2 = [
    ("RF 2.1", "Emisión de factura de venta",
     "Emitir una factura de venta electrónica con los datos del emisor, el comprador y las "
     "líneas de la operación.", "Sistema cliente", 5, 5),
    ("RF 2.2", "Emisión de nota crédito",
     "Emitir una nota crédito referenciando la factura de origen y el concepto de la "
     "corrección.", "Sistema cliente", 5, 5),
    ("RF 2.3", "Emisión de nota débito",
     "Emitir una nota débito referenciando la factura de origen y el concepto del mayor valor.",
     "Sistema cliente", 4, 4),
    ("RF 2.4", "Reserva atómica del consecutivo",
     "Reservar el número de la resolución en una sola sentencia, de modo que dos emisiones "
     "simultáneas nunca obtengan el mismo número.", "Sistema", 5, 5),
    ("RF 2.5", "Cálculo tributario del documento",
     "Calcular bases gravables, descuentos de línea, descuento de factura, prorrateo de IVA y "
     "totales según el impuesto de cada producto.", "Sistema", 5, 5),
    ("RF 2.6", "Generación del CUFE",
     "Calcular el código único de facturación electrónica de cada documento emitido.",
     "Sistema", 5, 5),
    ("RF 2.7", "Representación gráfica en PDF",
     "Generar el PDF del documento con el membrete, el logo y el color de la empresa que "
     "emite, nunca los del proveedor.", "Sistema", 5, 5),
    ("RF 2.8", "Generación del XML UBL 2.1",
     "Generar el archivo XML del documento bajo el estándar UBL 2.1 exigido por la DIAN.",
     "Sistema", 5, 5),
    ("RF 2.9", "Monograma de la empresa sin logo",
     "Dibujar las iniciales de la empresa sobre su color de marca cuando no ha cargado un "
     "logo, sin generar archivos.", "Sistema", 3, 3),
    ("RF 2.10", "Envío del documento al comprador",
     "Enviar el PDF y el XML al correo del comprador en segundo plano, sin demorar la "
     "respuesta al sistema que emitió.", "Sistema", 4, 4),
    ("RF 2.11", "Registro de eventos del documento",
     "Registrar cada hecho del documento, sea la emisión, la respuesta del proveedor o el "
     "envío del correo, con su fecha y su resultado.", "Sistema", 4, 4),
    ("RF 2.12", "Consulta de documentos emitidos",
     "Consultar lo emitido por cuenta de terceros con filtros por cliente, tipo, estado y "
     "rango de fechas.", "Administrador", 4, 4),
    ("RF 2.13", "Descarga del PDF y del XML",
     "Descargar la representación gráfica y el archivo XML de cualquier documento emitido.",
     "Administrador", 4, 4),
    ("RF 2.14", "Conservación del documento",
     "Conservar la cabecera, el detalle y los eventos de cada documento emitido para efectos "
     "de la obligación legal de conservación.", "Sistema", 5, 4),
]

RF3 = [
    ("RF 3.1", "Cálculo del consumo mensual",
     "Contar los documentos emitidos por cada cliente en el mes directamente de la tabla de "
     "documentos, sin contadores paralelos.", "Sistema", 5, 5),
    ("RF 3.2", "Consulta del cupo disponible",
     "Mostrar cuántos documentos del plan lleva consumidos el cliente y cuántos le quedan en "
     "el mes en curso.", "Administrador", 4, 4),
    ("RF 3.3", "Bloqueo por cupo agotado",
     "Rechazar la emisión de facturas con el código cupo_agotado cuando el cliente alcanzó el "
     "límite de su plan, antes de reservar el consecutivo.", "Sistema", 5, 5),
    ("RF 3.4", "Excepción de las notas",
     "Permitir la emisión de notas crédito y débito aunque el cupo esté agotado, para no dejar "
     "al cliente sin poder corregir un documento errado.", "Sistema", 5, 4),
    ("RF 3.5", "Alerta de cupo próximo a agotarse",
     "Advertir en el panel cuáles clientes están cerca del límite de su plan, para ofrecerles "
     "el siguiente antes de que les rebote una emisión.", "Administrador", 4, 3),
    ("RF 3.6", "Determinación del periodo facturable",
     "Tomar el último mes cerrado como periodo a cobrar, porque hasta que el mes no termina no "
     "se conoce el consumo ni el excedente.", "Sistema", 4, 4),
    ("RF 3.7", "Cola de mensualidades sin cobrar",
     "Listar los clientes activos a los que todavía no se les ha facturado el mes cerrado.",
     "Administrador", 4, 4),
    ("RF 3.8", "Emisión de la mensualidad",
     "Facturar la mensualidad del cliente emitiéndola por la propia API del sistema y "
     "conservando el número y el CUFE que esta devuelve.", "Administrador", 5, 5),
    ("RF 3.9", "Idempotencia de la mensualidad",
     "Impedir que un mismo mes de un mismo cliente se facture dos veces mediante una "
     "referencia externa con el formato PLAN-<cliente>-<AAAA-MM>.", "Sistema", 5, 4),
    ("RF 3.10", "Cobro de documentos excedentes",
     "Incluir en la mensualidad los documentos emitidos por encima del cupo del plan, "
     "valorados con el servicio de documento adicional.", "Administrador", 4, 3),
]

RF4 = [
    ("RF 4.1", "Registro de la venta del plan",
     "Emitir la factura de venta de los planes y servicios que el proveedor le vende a sus "
     "propios clientes.", "Administrador", 5, 5),
    ("RF 4.2", "Gestión de clientes propios",
     "Registrar, consultar, actualizar y eliminar los clientes a los que se les factura el "
     "servicio.", "Administrador", 4, 4),
    ("RF 4.3", "Gestión de planes y servicios",
     "Registrar, consultar, actualizar y eliminar el catálogo de planes y servicios, con su "
     "precio, su unidad y su impuesto.", "Administrador", 4, 4),
    ("RF 4.4", "Descuentos por producto",
     "Asociar descuentos a un plan o servicio y aplicarlos al facturar, indicando el concepto "
     "de la rebaja.", "Administrador", 3, 3),
    ("RF 4.5", "Búsqueda asistida al facturar",
     "Buscar clientes y servicios desde el formulario de factura sin recargar la página.",
     "Cajero", 4, 3),
    ("RF 4.6", "Registro de pagos",
     "Registrar los pagos recibidos de una factura, totales o parciales, con su método y su "
     "fecha.", "Administrador", 4, 4),
    ("RF 4.7", "Estado de pago de la factura",
     "Actualizar y consultar el estado de pago de cada factura entre pagada, pendiente, vencida, "
     "anulada, en disputa o reembolsada.", "Administrador", 4, 4),
    ("RF 4.8", "Notas sobre la factura propia",
     "Emitir notas crédito y notas débito referidas a una factura propia ya emitida.",
     "Administrador", 4, 4),
    ("RF 4.9", "Listado de facturas",
     "Consultar las facturas emitidas con búsqueda, filtros y paginación.",
     "Administrador", 4, 4),
    ("RF 4.10", "Descarga de la factura propia",
     "Descargar el PDF y el XML de cualquier factura emitida por el proveedor.",
     "Administrador", 4, 3),
    ("RF 4.11", "Emisión atómica",
     "Ejecutar la reserva del número, el guardado de la cabecera y el del detalle dentro de "
     "una sola transacción, de modo que un fallo no consuma un consecutivo.", "Sistema", 5, 5),
]

RF5 = [
    ("RF 5.1", "Tablero del servicio",
     "Mostrar documentos emitidos, clientes que emitieron, aceptación ante la DIAN, ingreso "
     "recurrente y volumen por periodo.", "Administrador", 5, 4),
    ("RF 5.2", "Tablero de la venta",
     "Mostrar ventas netas, valor cobrado, cartera pendiente, facturación contra cobro e "
     "ingreso por plan.", "Administrador", 5, 4),
    ("RF 5.3", "Filtro de periodo",
     "Filtrar todas las cifras del tablero por rango de fechas, con presets de 7, 15, 30 y 90 "
     "días y 12 meses.", "Administrador", 4, 4),
    ("RF 5.4", "Filtro por empresa",
     "Consolidar o separar las cifras por empresa emisora, según el alcance del rol.",
     "Administrador", 4, 3),
    ("RF 5.5", "Grano de las series temporales",
     "Agrupar las gráficas de tiempo por día, semana o mes, sugiriendo el grano según el largo "
     "del rango y compartiéndolo entre las dos series.", "Administrador", 3, 3),
    ("RF 5.6", "Cartera por antigüedad",
     "Clasificar la cartera pendiente por tramos de vencimiento para orientar la gestión de "
     "cobro.", "Administrador", 4, 3),
    ("RF 5.7", "Generación de reportes",
     "Generar los siete reportes del sistema, que son ventas por periodo, cartera por cobrar, "
     "productos más vendidos, clientes por facturación, resumen tributario, facturación por "
     "estado de pago y facturación por usuario.", "Administrador", 5, 4),
    ("RF 5.8", "Exportación de reportes",
     "Exportar cualquier reporte a CSV y a PDF conservando los filtros aplicados.",
     "Administrador", 4, 4),
    ("RF 5.9", "Tablero reducido para el cajero",
     "Presentar al cajero una vista operativa sin cifras financieras ni información de otros "
     "clientes.", "Cajero", 4, 3),
]

RF6 = [
    ("RF 6.1", "Centro de configuración",
     "Reunir en una sola pantalla los catálogos y parámetros del sistema, agrupados por su "
     "finalidad y con el conteo de cada uno.", "Administrador", 3, 3),
    ("RF 6.2", "Gestión de impuestos",
     "Registrar, consultar, actualizar y eliminar los impuestos con su tarifa y su código "
     "DIAN.", "Administrador", 5, 4),
    ("RF 6.3", "Gestión de descuentos",
     "Registrar, consultar, actualizar y eliminar los descuentos aplicables a la facturación.",
     "Administrador", 3, 3),
    ("RF 6.4", "Gestión de métodos de pago",
     "Registrar, consultar, actualizar y eliminar los métodos de pago admitidos.",
     "Administrador", 3, 3),
    ("RF 6.5", "Gestión de empresas emisoras",
     "Registrar y mantener las empresas emisoras con su NIT, su resolución de facturación, su "
     "prefijo y su rango autorizado.", "Administrador", 5, 5),
    ("RF 6.6", "Marca de la empresa emisora",
     "Cargar el logo y definir el color de marca de cada empresa emisora, y eliminarlos cuando "
     "corresponda.", "Administrador", 3, 3),
    ("RF 6.7", "Catálogo de ubicación",
     "Consultar departamentos y municipios encadenados para los datos de emisor y comprador.",
     "Administrador", 3, 3),
    ("RF 6.8", "Estados de pago",
     "Mantener el catálogo de estados de pago que puede tomar una factura.",
     "Administrador", 3, 3),
]

RF7 = [
    ("RF 7.1", "Autenticación de usuarios",
     "Validar las credenciales del usuario contra la contraseña almacenada antes de dar acceso "
     "al panel.", "Usuario", 5, 5),
    ("RF 7.2", "Almacenamiento seguro de contraseñas",
     "Guardar únicamente el hash de la contraseña, calculado con bcrypt.", "Sistema", 5, 5),
    ("RF 7.3", "Control de acceso por rol",
     "Restringir el acceso a cada ruta según la jerarquía de roles, que son administrador, jefe de "
     "tienda, supervisor y cajero.", "Sistema", 5, 5),
    ("RF 7.4", "Reserva de los módulos de plataforma",
     "Impedir que el cajero acceda a clientes API, documentos emitidos, consumo, reportes, "
     "inventario y configuración, donde se ven llaves y cifras de todos los clientes.",
     "Sistema", 5, 4),
    ("RF 7.5", "Cierre de sesión por inactividad",
     "Cerrar la sesión tras el tiempo de inactividad configurado, renovando el reloj con cada "
     "petición del usuario.", "Sistema", 4, 4),
    ("RF 7.6", "Aviso previo al cierre de sesión",
     "Advertir en pantalla antes de que la sesión expire, contando en el navegador para que el "
     "aviso no cuente como actividad.", "Usuario", 3, 3),
    ("RF 7.7", "Gestión de usuarios",
     "Registrar, consultar, actualizar y eliminar usuarios del panel con su rol y su empresa.",
     "Administrador", 4, 4),
    ("RF 7.8", "Foto de perfil",
     "Permitir a cada usuario cambiar su propia foto y a un superior la de sus inferiores, "
     "validando y normalizando la imagen.", "Usuario", 2, 2),
    ("RF 7.9", "Registro de auditoría",
     "Anotar cada operación de escritura con el usuario, su nombre, la acción, la entidad y la "
     "descripción escrita en el momento del hecho.", "Sistema", 5, 4),
    ("RF 7.10", "Auditoría que no interrumpe",
     "Garantizar que un fallo al registrar la auditoría no impida completar la operación que "
     "se estaba auditando.", "Sistema", 4, 4),
    ("RF 7.11", "Consulta de auditoría",
     "Consultar el rastro de operaciones con filtros por usuario, acción, entidad y fecha.",
     "Administrador", 4, 3),
]

RF8 = [
    ("RF 8.1", "Autenticación por llave",
     "Autenticar cada petición de la API con el encabezado X-API-Key, resolviendo el cliente "
     "por el prefijo y verificando el secreto contra su hash.", "Sistema cliente", 5, 5),
    ("RF 8.2", "Distinción entre credencial y permiso",
     "Responder 401 cuando la llave falta o no sirve, y 403 cuando la llave es válida pero el "
     "cliente está suspendido o revocado.", "Sistema", 4, 4),
    ("RF 8.3", "Forma única de error",
     "Devolver todos los errores con la misma estructura de código estable, mensaje legible y "
     "campo señalado.", "Sistema", 4, 4),
    ("RF 8.4", "Validación de la entrada",
     "Validar el cuerpo de cada petición contra su modelo antes de procesarla, informando qué "
     "campo está mal.", "Sistema", 5, 4),
    ("RF 8.5", "Emisión por API",
     "Exponer la emisión de facturas, notas crédito y notas débito como operaciones de la API "
     "consumibles por un sistema externo.", "Sistema cliente", 5, 5),
    ("RF 8.6", "Idempotencia de la emisión",
     "Devolver el documento ya emitido, sin crear otro, cuando se reenvía la misma referencia "
     "externa.", "Sistema cliente", 5, 4),
    ("RF 8.7", "Consulta y listado por API",
     "Permitir al sistema integrado consultar sus documentos emitidos y el detalle de "
     "cualquiera de ellos.", "Sistema cliente", 4, 4),
    ("RF 8.8", "Descarga de archivos por API",
     "Permitir descargar el PDF y el XML de un documento emitido a través de la API.",
     "Sistema cliente", 4, 4),
    ("RF 8.9", "Verificación de la llave",
     "Ofrecer una operación de comprobación que permita al integrador confirmar que su llave "
     "quedó bien configurada.", "Sistema cliente", 3, 3),
    ("RF 8.10", "Documentación automática",
     "Publicar el contrato de la API en formato OpenAPI y una interfaz de exploración, para "
     "que el integrador no dependa de documentación escrita aparte.", "Sistema cliente", 4, 4),
]

MODULOS = [
    ("RF 1", "Gestión de clientes API",
     "Administra las empresas que se integran con el proveedor, con su alta, el plan que "
     "contratan, la llave con la que llaman a la API y el estado en que se encuentran.",
     "Este módulo es la puerta de entrada del negocio, porque sin un cliente registrado y con llave "
     "vigente no hay emisión posible. Las reglas de la llave, que son entregarla una sola vez, "
     "guardar solo su hash y poder rotarla, son las que permiten que una credencial "
     "comprometida se reemplace sin interrumpir el servicio.", RF1),
    ("RF 2", "Gestión de documentos electrónicos",
     "Reúne la emisión de facturas de venta, notas crédito y notas débito por cuenta de "
     "terceros, con todo lo que cada documento debe producir.",
     "Es el núcleo del sistema y el que sostiene el primer objetivo específico. Sus requisitos "
     "no describen únicamente la creación del documento, sino las condiciones que lo hacen "
     "válido, y son un consecutivo que no se repite, un cálculo tributario correcto, el membrete de "
     "quien emite y los dos archivos que la normativa exige.", RF2),
    ("RF 3", "Gestión de consumo y planes",
     "Controla cuántos documentos ha emitido cada cliente contra el cupo de su plan y "
     "convierte ese consumo en la facturación mensual del servicio.",
     "Aquí se cruza la operación con el negocio. El consumo se cuenta de los documentos "
     "realmente emitidos y no de un contador aparte, de modo que la cifra que se le cobra al "
     "cliente y la que el sistema muestra no puedan separarse.", RF3),
    ("RF 4", "Gestión de facturación y cartera propias",
     "Cubre la venta que hace el proveedor, con los planes y servicios de su catálogo, sus "
     "clientes, sus facturas y el recaudo de las mismas.",
     "Estos requisitos operan sobre la zona comercial de la base, separada de la del "
     "middleware. La separación no es una preferencia de diseño, porque si un documento emitido para "
     "un tercero se guardara aquí, el tablero y los reportes lo contarían como ingreso "
     "propio.", RF4),
    ("RF 5", "Gestión de reportes y tablero de control",
     "Consolida la información del servicio y de la venta en indicadores, gráficas y reportes "
     "exportables.",
     "El tablero está partido en dos secciones y el orden importa, porque primero va el servicio, que es "
     "lo que el proveedor hace, y después la venta, que es cobrarlo. Todas las cifras respetan "
     "el filtro de periodo, porque un indicador que no se mueve cuando el rango cambia está "
     "midiendo algo distinto de lo que su rótulo dice.", RF5),
    ("RF 6", "Gestión de configuración y catálogos",
     "Mantiene los parámetros que la operación usa pero que se ajustan de vez en cuando, como "
     "impuestos, descuentos, métodos de pago, estados, empresas emisoras y ubicación.",
     "Se agrupan aparte del trabajo diario porque su frecuencia de uso es otra. El catálogo de "
     "empresas emisoras es el más delicado de todos, porque de él salen la resolución, el prefijo y "
     "el rango autorizado con los que se numera cada documento.", RF6),
    ("RF 7", "Gestión de seguridad y auditoría",
     "Controla quién entra al panel, qué puede ver según su rol y qué queda registrado de lo "
     "que hace.",
     "La auditoría solo escribe, y no existe forma de corregir ni de borrar un registro, y la "
     "frase se redacta en el momento del hecho en vez de reconstruirse después leyendo el "
     "documento, que puede anularse o desaparecer. Un rastro que se puede editar no es un "
     "rastro.", RF7),
    ("RF 8", "Integración mediante API REST",
     "Expone los servicios de facturación como una interfaz consumible por sistemas externos, como "
     "puntos de venta, ERP o aplicaciones propias del cliente.",
     "Es el módulo que sostiene la propuesta de valor del proyecto, ya que la empresa cumple con la "
     "obligación de facturar electrónicamente sin cambiar el software con el que ya trabaja. "
     "Por eso sus requisitos incluyen la documentación automática y la idempotencia, que son "
     "las que hacen que integrarse sea barato y reintentar sea seguro.", RF8),
]

# --- Requisitos no funcionales --------------------------------------------------
# (código, categoría, requisito, verificación)

RNF = [
    ("RNF 01", "Rendimiento",
     "La emisión de un documento por la API debe responder en menos de tres segundos bajo "
     "carga normal.",
     "Medición del tiempo de respuesta de la operación de emisión."),
    ("RNF 02", "Rendimiento",
     "El envío del documento al comprador no debe demorar la respuesta al sistema que emitió.",
     "El correo se agenda como tarea de fondo y su resultado queda anotado en los eventos."),
    ("RNF 03", "Rendimiento",
     "Los listados de documentos, facturas y auditoría deben paginarse para no cargar la "
     "totalidad de los registros en una sola consulta.",
     "Revisión de las consultas paginadas del servicio de listados."),
    ("RNF 04", "Seguridad",
     "Las contraseñas de los usuarios deben almacenarse cifradas con un algoritmo de hash de "
     "un solo sentido.",
     "Inspección de la tabla de usuarios, en la que no debe existir ninguna contraseña legible."),
    ("RNF 05", "Seguridad",
     "Del secreto de las llaves de la API solo debe conservarse su hash; el prefijo se guarda "
     "en claro únicamente para poder localizar la fila.",
     "Inspección de la tabla de clientes API y prueba automatizada del servicio de llaves."),
    ("RNF 06", "Seguridad",
     "Ninguna credencial debe quedar escrita en el registro de auditoría ni en los registros "
     "del servidor.",
     "Revisión del registro tras rotar una llave, en el que debe constar el hecho y no la llave."),
    ("RNF 07", "Seguridad",
     "Toda ruta del panel, salvo el ingreso y los recursos estáticos, debe exigir sesión "
     "iniciada.",
     "Petición sin sesión a una ruta protegida, que debe redirigir al formulario de ingreso."),
    ("RNF 08", "Seguridad",
     "La sesión debe cerrarse por inactividad y no por tiempo transcurrido.",
     "Prueba de inactividad prolongada frente a uso continuo durante el mismo lapso."),
    ("RNF 09", "Seguridad",
     "La comunicación debe realizarse sobre HTTPS en el despliegue productivo.",
     "Verificación del certificado y de la redirección forzada en el servidor."),
    ("RNF 10", "Integridad de los datos",
     "Dos documentos del mismo emisor y del mismo tipo no pueden compartir número, ni siquiera "
     "ante peticiones simultáneas.",
     "Reserva del consecutivo en una sola sentencia más índice único en la base."),
    ("RNF 11", "Integridad de los datos",
     "Una emisión que falla a mitad no debe dejar rastro parcial ni consumir un consecutivo.",
     "Prueba de fallo intencional dentro de la transacción de emisión."),
    ("RNF 12", "Integridad de los datos",
     "El consumo del cliente debe calcularse siempre de los documentos emitidos y nunca de un "
     "contador almacenado.",
     "Revisión del servicio de consumo, donde no debe existir tabla de contadores."),
    ("RNF 13", "Integridad de los datos",
     "Los documentos emitidos por cuenta de terceros no deben registrarse en las tablas de la "
     "venta propia.",
     "Revisión de las dos zonas de la base y de las consultas del tablero."),
    ("RNF 14", "Trazabilidad",
     "Toda operación de escritura debe quedar registrada con el usuario que la realizó, y el "
     "registro debe conservar su nombre aunque la cuenta se elimine.",
     "Consulta del registro de auditoría después de eliminar un usuario."),
    ("RNF 15", "Trazabilidad",
     "El registro de auditoría no debe ofrecer operaciones de modificación ni de borrado.",
     "Revisión del servicio, donde solo existe la función de registrar."),
    ("RNF 16", "Disponibilidad",
     "La indisponibilidad de servicios externos, como el correo, no debe impedir la emisión de "
     "documentos.",
     "Emisión con el servidor de correo apagado, que debe completarse y anotar el intento."),
    ("RNF 17", "Disponibilidad",
     "El sistema debe estar disponible al menos el 99 % del tiempo en horario hábil.",
     "Monitoreo del servicio en el entorno de despliegue."),
    ("RNF 18", "Usabilidad",
     "La interfaz debe agruparse por trabajo y no por tabla, y cada destino debe tener un solo "
     "lugar en la navegación.",
     "Revisión del menú, donde ningún destino debe alcanzarse por dos caminos distintos."),
    ("RNF 19", "Usabilidad",
     "Los formularios deben validar los datos y explicar el error señalando el campo que lo "
     "provocó.",
     "Envío de formularios con datos inválidos."),
    ("RNF 20", "Usabilidad",
     "La interfaz debe adaptarse a pantallas de escritorio y de dispositivos móviles.",
     "Revisión en distintos anchos de pantalla."),
    ("RNF 21", "Compatibilidad",
     "El sistema debe funcionar en los navegadores vigentes sin requerir instalación local.",
     "Prueba en los navegadores de mayor uso."),
    ("RNF 22", "Compatibilidad",
     "El contrato de la API debe publicarse en formato OpenAPI para que cualquier cliente "
     "pueda generar su integración.",
     "Descarga del documento OpenAPI y generación de un cliente a partir de él."),
    ("RNF 23", "Cumplimiento normativo",
     "Los documentos deben generarse conforme al estándar UBL 2.1 y llevar el código único de "
     "facturación electrónica.",
     "Validación estructural del XML emitido."),
    ("RNF 24", "Cumplimiento normativo",
     "La representación gráfica debe llevar siempre los datos de la empresa que emite y nunca "
     "los del proveedor tecnológico.",
     "Prueba automatizada del membrete del PDF."),
    ("RNF 25", "Cumplimiento normativo",
     "Los documentos emitidos deben conservarse por el término que exige la normativa "
     "tributaria.",
     "Revisión de la política de conservación y de los respaldos."),
    ("RNF 26", "Mantenibilidad",
     "La aritmética tributaria debe estar implementada una sola vez y ser la misma que usan la "
     "aplicación web y la API.",
     "Revisión del servicio de cálculo y de sus pruebas automatizadas."),
    ("RNF 27", "Mantenibilidad",
     "Las rutas deben limitarse a recibir y responder, dejando la lógica de negocio en la capa "
     "de servicios.",
     "Revisión de la estructura del proyecto."),
    ("RNF 28", "Mantenibilidad",
     "Todo cambio en el esquema de la base debe aplicarse mediante una migración versionada y "
     "repetible.",
     "Ejecución del migrador dos veces seguidas, de modo que la segunda no altere nada."),
    ("RNF 29", "Mantenibilidad",
     "El sistema debe contar con pruebas automatizadas sobre el cálculo tributario, el "
     "contrato de la API y la generación de los documentos.",
     "Ejecución de la batería de pruebas."),
    ("RNF 30", "Escalabilidad",
     "El sistema debe admitir nuevas empresas emisoras y nuevos clientes integrados sin "
     "cambios en el código.",
     "Alta de una empresa y de un cliente nuevos por el panel."),
    ("RNF 31", "Escalabilidad",
     "Un cambio que rompa el contrato de la API debe publicarse como una versión nueva, "
     "manteniendo la anterior en funcionamiento.",
     "Revisión de la política de versionado de la API."),
    ("RNF 32", "Portabilidad",
     "El sistema debe operar desde cualquier sistema operativo mediante un navegador, sin "
     "instalación en el equipo del usuario.",
     "Acceso desde equipos con distintos sistemas operativos."),
]

# --- Trazabilidad con los objetivos específicos ---------------------------------

TRAZABILIDAD = [
    ("OE 1", "Emisión de documentos electrónicos", "RF 2", "Nueva factura y Documentos emitidos"),
    ("OE 2", "API REST de integración", "RF 8, RF 3.3, RF 3.4", "API /api/v1/"),
    ("OE 3", "Clientes API y planes de suscripción", "RF 1, RF 3, RF 4.3",
     "Clientes API, Consumo y planes, Planes y servicios"),
    ("OE 4", "Panel de control y reportes", "RF 5", "Panel de control y Reportes"),
    ("OE 5", "Seguridad, roles y auditoría", "RF 7", "Usuarios y Auditoría"),
]

USUARIOS = [
    ("Administrador", "Acceso completo. Administra clientes API, planes, empresas emisoras, "
     "usuarios, configuración y reportes, y puede consolidar las cifras de todas las empresas."),
    ("Jefe de tienda", "Acceso a la operación y a las cifras de su propia empresa, sin "
     "consolidar las demás."),
    ("Supervisor", "Consulta de la operación y de los reportes de su empresa, con capacidad "
     "limitada de modificación."),
    ("Cajero", "Solo facturación. Emite y consulta clientes y servicios. No accede a cifras "
     "financieras ni a los módulos de plataforma."),
    ("Sistema cliente", "Sistema externo, sea punto de venta, ERP o aplicación propia, que consume "
     "la API con su llave para emitir y consultar sus documentos."),
    ("Comprador", "Destinatario del documento. No accede al sistema y recibe el PDF y el XML en "
     "su correo."),
]

ENTORNO = [
    ("Servidor de aplicación", "Python 3.13 con FastAPI y servidor ASGI Uvicorn"),
    ("Interfaz web", "Plantillas Jinja2 con Bootstrap 5.3.2 y gráficas Chart.js"),
    ("Base de datos", "MySQL, con acceso mediante consultas SQL explícitas"),
    ("Generación de documentos", "ReportLab para el PDF y construcción de XML UBL 2.1"),
    ("Seguridad", "bcrypt para contraseñas, sesiones por cookie firmada y llaves de API con hash"),
    ("Cliente", "Navegador web vigente, sin instalación local"),
    ("Integración", "API REST sobre HTTP con documentación OpenAPI"),
]


# --- Armado del documento -------------------------------------------------------

def construir():
    d = DocumentoAPA()

    d.portada(
        titulo="FACTUGEST",
        subtitulo="Especificación de requisitos funcionales y no funcionales",
        integrantes=["Brandon Arley Restrepo Gélvez",
                     "Johan Sebastián Acosta Sánchez",
                     "Wilmer Jesús Contreras Rangel"],
        grado="Documento de especificación de requisitos del proyecto de grado\n"
              "Tecnólogo en Análisis y Desarrollo de Software",
        institucion=["SERVICIO NACIONAL DE APRENDIZAJE (SENA)",
                     "Centro de la Industria, la Empresa y los Servicios (CIES)",
                     "Tecnólogo en Análisis y Desarrollo de Software"],
        ciudad="CÚCUTA, NORTE DE SANTANDER",
        anio=2026,
    )
    d.tabla_contenido()

    _introduccion(d)
    _descripcion_general(d)
    _funcionales(d)
    _no_funcionales(d)
    _priorizacion(d)
    _trazabilidad(d)

    SALIDA.mkdir(parents=True, exist_ok=True)
    d.guardar(ARCHIVO)
    return d


def _introduccion(d):
    d.titulo("1. Introducción", nivel=1)

    d.titulo("1.1 Propósito", nivel=2)
    d.parrafo(
        "Este documento especifica la totalidad de los requisitos funcionales y no funcionales "
        "de FactuGest, plataforma web de facturación electrónica desarrollada como proyecto de "
        "grado del programa Tecnólogo en Análisis y Desarrollo de Software. Su finalidad es "
        "servir de referencia única sobre lo que el sistema debe hacer y bajo qué condiciones "
        "de calidad debe hacerlo, de modo que el desarrollo, las pruebas y la verificación del "
        "cumplimiento de los objetivos se contrasten contra un mismo enunciado."
    )
    d.parrafo(
        "Del catálogo aquí especificado se extraen, para el documento de grado, los requisitos "
        "de mayor relevancia. Este documento conserva el registro completo, incluidos aquellos "
        "que por su carácter secundario no se incorporan al cuerpo del trabajo pero sí forman "
        "parte del sistema construido."
    )

    d.titulo("1.2 Alcance del producto", nivel=2)
    d.parrafo(
        "FactuGest opera como proveedor tecnológico de facturación electrónica. Emite facturas "
        "de venta, notas crédito y notas débito por cuenta de las empresas que contratan el "
        "servicio, genera para cada documento su consecutivo autorizado, su código único de "
        "facturación electrónica, su representación gráfica en PDF y su archivo XML bajo el "
        "estándar UBL 2.1, y lo hace llegar al comprador. Las empresas se integran mediante una "
        "API REST que consumen desde el software que ya utilizan, sin necesidad de "
        "reemplazarlo."
    )
    d.parrafo(
        "El sistema administra además el negocio del proveedor, con el registro de las empresas "
        "integradas, la llave con la que cada una accede, el plan de suscripción que contrata, "
        "el control de su consumo mensual contra el cupo de ese plan y la facturación de la "
        "mensualidad correspondiente. Sobre esa operación construye un tablero de control y un "
        "conjunto de reportes exportables."
    )
    d.parrafo(
        "Queda fuera del alcance de esta versión la transmisión de los documentos a los "
        "servicios en producción de la administración tributaria, de modo que el código único se genera en "
        "modalidad de pruebas, a la espera de la habilitación correspondiente."
    )

    d.titulo("1.3 Definiciones y acrónimos", nivel=2)
    d.tabla(
        "Definiciones y acrónimos empleados en el documento",
        ["Término", "Significado"],
        [
            ["API", "Interfaz de programación de aplicaciones. Conjunto de operaciones que un "
                    "sistema expone para que otro sistema las consuma."],
            ["CUFE", "Código único de facturación electrónica. Identificador irrepetible que "
                     "acompaña a cada documento emitido."],
            ["DIAN", "Dirección de Impuestos y Aduanas Nacionales, autoridad tributaria "
                     "colombiana."],
            ["Cliente API", "Empresa que contrata el servicio y se integra con la plataforma "
                            "mediante una llave propia."],
            ["Cupo", "Cantidad de documentos que el plan contratado incluye en el mes."],
            ["Emisor", "Empresa por cuenta de la cual se expide el documento."],
            ["Comprador", "Destinatario del documento electrónico."],
            ["Idempotencia", "Propiedad por la cual repetir una operación produce el mismo "
                             "resultado que ejecutarla una sola vez."],
            ["Llave de API", "Credencial con la que un sistema externo se identifica ante la "
                             "plataforma."],
            ["Middleware", "Componente que se sitúa entre dos sistemas y les permite "
                           "comunicarse sin que ninguno cambie."],
            ["RF / RNF", "Requisito funcional / requisito no funcional."],
            ["UBL 2.1", "Estándar de documentos comerciales en formato XML adoptado por la "
                        "normativa de facturación electrónica."],
        ],
        nota="Elaboración propia.",
        anchos=[3.2, 13.1],
    )


def _descripcion_general(d):
    d.titulo("2. Descripción general", nivel=1, nueva_pagina=True)

    d.titulo("2.1 Perspectiva del producto", nivel=2)
    d.parrafo(
        "FactuGest se construyó como una aplicación monolítica que presenta dos caras sobre una "
        "misma capa de lógica de negocio. La primera es una aplicación web con la que el "
        "personal del proveedor administra clientes, planes, facturación y reportes. La segunda "
        "es una API REST que los sistemas de las empresas integradas consumen para emitir sus "
        "documentos. Ambas se apoyan en los mismos servicios y sobre la misma base de datos, de "
        "manera que una regla de negocio se implementa una sola vez y rige para las dos."
    )
    d.parrafo(
        "La base de datos está organizada en dos zonas que no se mezclan. La zona comercial "
        "guarda lo que el proveedor vende, esto es, sus planes, sus clientes y sus facturas. La zona de "
        "middleware guarda lo que el proveedor emite por cuenta de terceros, con las empresas "
        "integradas, los compradores y los documentos electrónicos. Una tabla puente relaciona "
        "la mensualidad cobrada con el cliente que la pagó."
    )

    d.titulo("2.2 Clases y características de los usuarios", nivel=2)
    d.tabla(
        "Clases de usuarios del sistema",
        ["Usuario", "Características y alcance"],
        [[u, c] for u, c in USUARIOS],
        nota="Elaboración propia. Los cuatro primeros son roles del panel; los dos últimos "
             "interactúan con el sistema sin acceder a él.",
        anchos=[3.4, 12.9],
    )

    d.titulo("2.3 Entorno operativo", nivel=2)
    d.tabla(
        "Entorno operativo del sistema",
        ["Componente", "Tecnología"],
        [[c, t] for c, t in ENTORNO],
        nota="Elaboración propia.",
        anchos=[4.6, 11.7],
    )

    d.titulo("2.4 Restricciones de diseño y de implementación", nivel=2)
    d.vinetas([
        "El acceso a la base de datos se realiza mediante consultas SQL explícitas, sin "
        "mapeador objeto-relacional, para mantener el control sobre cada consulta.",
        "La aritmética tributaria reside en un único servicio y ninguna ruta la reimplementa.",
        "Toda modificación del esquema de la base se aplica mediante migraciones versionadas y "
        "repetibles.",
        "Los consecutivos de la resolución se reservan en una sola sentencia, por tratarse de "
        "un recurso autorizado y finito.",
        "Un cambio que rompa el contrato de la API obliga a publicar una versión nueva y a "
        "mantener la anterior en funcionamiento.",
    ])

    d.titulo("2.5 Supuestos y dependencias", nivel=2)
    d.vinetas([
        "La empresa integrada cuenta con resolución de facturación vigente, con su prefijo y "
        "su rango autorizados.",
        "El sistema que se integra puede realizar peticiones HTTP y conservar su llave de "
        "acceso de manera segura.",
        "La operación requiere conexión a internet estable, tanto del lado del proveedor como "
        "del lado del sistema integrado.",
        "El envío del documento al comprador depende de un servidor de correo cuya "
        "indisponibilidad no debe impedir la emisión.",
        "La emisión en producción ante la administración tributaria depende de la habilitación "
        "del proveedor, que se encuentra en trámite.",
    ])


def _funcionales(d):
    d.titulo("3. Requisitos funcionales", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Los requisitos funcionales describen las funcionalidades que el sistema debe "
        "proporcionar. Se agruparon en ocho módulos que corresponden a los conjuntos de trabajo "
        "reales de la plataforma, con el fin de facilitar su organización, su desarrollo, su "
        "validación y su mantenimiento."
    )
    d.parrafo(
        "La agrupación se aparta deliberadamente de la de un sistema de punto de venta. "
        "FactuGest no administra mercancía ni compras a proveedores, sino que administra la emisión de "
        "documentos por cuenta de terceros y la suscripción con la que ese servicio se cobra. "
        "Por esa razón, donde un sistema comercial tendría gestión de inventario y gestión de "
        "compras, aquí hay gestión de clientes API y gestión de consumo y planes."
    )

    total = sum(len(m[4]) for m in MODULOS)
    d.tabla(
        "Módulos funcionales del sistema",
        ["Código", "Módulo", "Cantidad de RF"],
        [[c, n, str(len(rf))] for c, n, _, _, rf in MODULOS] + [["", "Total", str(total)]],
        nota="Elaboración propia.",
        anchos=[2.2, 10.6, 3.5],
    )

    for indice, (codigo, nombre, intro, cierre, requisitos) in enumerate(MODULOS, start=1):
        d.titulo(f"3.{indice} {codigo}. {nombre}", nivel=2, nueva_pagina=True)
        d.parrafo(intro)
        d.tabla(
            f"Requisitos funcionales del módulo de {inicial_minuscula(nombre)}",
            ["Código", "Requisito", "Descripción", "Actor", "Prioridad"],
            [[c, n, desc, actor, prioridad(v, u)] for c, n, desc, actor, v, u in requisitos],
            nota="Elaboración propia. La prioridad se deriva del valor de negocio y de la "
                 "urgencia asignados en el capítulo 5.",
            anchos=[1.6, 3.3, 6.8, 2.6, 2.0],
        )
        d.parrafo(cierre)


def _no_funcionales(d):
    d.titulo("4. Requisitos no funcionales", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Los requisitos no funcionales establecen las condiciones de calidad que el sistema "
        "debe satisfacer. No describen funcionalidades, sino restricciones sobre la manera en "
        "que estas se prestan, esto es, con qué rapidez, con qué garantías de seguridad, con qué "
        "integridad de la información y con qué facilidad de mantenimiento."
    )
    d.parrafo(
        "Cada requisito se acompaña de la forma en que se comprueba. Un requisito no funcional "
        "que no indica cómo verificarse es una aspiración y no un requisito, porque al momento de "
        "evaluar el sistema no habría manera de afirmar si se cumplió."
    )

    categorias = []
    for codigo, categoria, requisito, verificacion in RNF:
        if categoria not in categorias:
            categorias.append(categoria)

    d.tabla(
        "Requisitos no funcionales por categoría",
        ["Código", "Categoría", "Requisito", "Verificación"],
        [[c, cat, r, v] for c, cat, r, v in RNF],
        nota="Elaboración propia. Las categorías responden a los atributos de calidad "
             "relevantes para un sistema que expide documentos con efectos tributarios.",
        anchos=[1.7, 2.6, 6.9, 5.1],
    )

    d.parrafo(
        "Tres de estas categorías merecen una observación. Las de integridad de los datos y "
        "trazabilidad no son exigencias genéricas de calidad. Un consecutivo repetido es un "
        "documento rechazado por la administración tributaria, y un rastro de operaciones que "
        "puede editarse no sirve como rastro. La de cumplimiento normativo, por su parte, "
        "recoge obligaciones legales cuyo incumplimiento no degrada el servicio sino que lo "
        "invalida."
    )


def _priorizacion(d):
    d.titulo("5. Priorización de los requisitos funcionales", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Con el fin de establecer el orden de implementación de las funcionalidades, se "
        "priorizaron los requisitos funcionales considerando su valor para el negocio y la "
        "urgencia asociada a cada uno. La evaluación empleó una escala de 1 a 5 en ambos "
        "criterios, donde los valores más altos representan un mayor impacto para la "
        "organización y una necesidad más inmediata de implementación."
    )
    d.tabla(
        "Escala de valoración empleada",
        ["#", "Valor de negocio", "Urgencia"],
        [
            ["1", "Impacto muy bajo para la operación", "No es urgente, puede esperar"],
            ["2", "Impacto bajo, aporta poca funcionalidad", "Poco urgente, puede desarrollarse después"],
            ["3", "Impacto medio, mejora procesos importantes", "Urgencia moderada, conviene implementarlo pronto"],
            ["4", "Impacto alto, necesario para operar con eficiencia", "Muy urgente, afecta procesos importantes"],
            ["5", "Impacto crítico, indispensable para el sistema", "Urgencia crítica, debe implementarse de inmediato"],
        ],
        nota="Elaboración propia, adaptada de la técnica de priorización por valor y urgencia.",
        anchos=[1.0, 7.6, 7.7],
    )
    d.parrafo(
        "El puntaje individual de cada requisito resulta de ponderar el valor de negocio en un "
        "sesenta por ciento y la urgencia en un cuarenta por ciento. La ponderación no es "
        "neutra y responde a una decisión explícita, y es que lo importante debe pesar más que lo "
        "afanado, porque un requisito urgente pero de bajo valor desplaza recursos de otro que "
        "sostiene la operación. El puntaje global del módulo es el promedio de los puntajes de "
        "sus requisitos."
    )

    filas = []
    for codigo, nombre, _, _, requisitos in MODULOS:
        global_modulo = round(sum(puntaje(v, u) for *_, v, u in requisitos) / len(requisitos), 1)
        for posicion, (c, n, _, _, v, u) in enumerate(requisitos):
            filas.append([
                f"{nombre}" if posicion == 0 else "",
                f"{c} {n}",
                str(v), str(u),
                str(puntaje(v, u)),
                str(global_modulo) if posicion == 0 else "",
            ])

    d.tabla(
        "Priorización de los requisitos funcionales",
        ["Módulo", "Requisito", "Valor", "Urgencia", "Puntaje individual", "Puntaje global del módulo"],
        filas,
        nota="Elaboración propia. El puntaje individual pondera el valor de negocio al 60 % y "
             "la urgencia al 40 %; el global es el promedio del módulo.",
        anchos=[3.2, 5.6, 1.3, 1.8, 2.2, 2.2],
    )

    orden = sorted(
        ((n, round(sum(puntaje(v, u) for *_, v, u in rf) / len(rf), 1))
         for _, n, _, _, rf in MODULOS),
        key=lambda x: x[1], reverse=True,
    )
    d.parrafo(
        "El orden resultante confirma la naturaleza del proyecto. Encabezan la lista los "
        "módulos de los que depende que un documento salga bien emitido y que el cliente pueda "
        "emitirlo, y quedan al final los que ajustan parámetros que cambian de vez en cuando. "
        f"El módulo mejor puntuado es el de {orden[0][0].lower()}, con {orden[0][1]} puntos, y "
        f"el de menor puntaje es el de {orden[-1][0].lower()}, con {orden[-1][1]}."
    )


def _trazabilidad(d):
    d.titulo("6. Trazabilidad con los objetivos del proyecto", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Cada objetivo específico del proyecto se sostiene en un conjunto determinado de "
        "requisitos funcionales y se evidencia en un módulo concreto del sistema. La siguiente "
        "matriz establece esa correspondencia, de modo que la verificación del cumplimiento de "
        "un objetivo pueda hacerse sobre requisitos comprobables y no sobre una apreciación "
        "general."
    )
    d.tabla(
        "Matriz de trazabilidad entre objetivos, requisitos y módulos",
        ["Objetivo", "Enunciado", "Requisitos", "Módulo del sistema"],
        [[o, e, r, m] for o, e, r, m in TRAZABILIDAD],
        nota="Elaboración propia.",
        anchos=[1.8, 5.2, 4.0, 5.3],
    )
    d.parrafo(
        "La matriz cumple además una función de control sobre la propia especificación, porque un "
        "requisito que no puede asociarse a ningún objetivo indica alcance no previsto, y un "
        "objetivo sin requisitos asociados indica una promesa que el sistema no está en "
        "condiciones de cumplir. En la especificación resultante no se presenta ninguno de los "
        "dos casos."
    )


if __name__ == "__main__":
    documento = construir()
    total_rf = sum(len(m[4]) for m in MODULOS)
    print(f"Generado: {ARCHIVO}")
    print(f"RF: {total_rf} en {len(MODULOS)} módulos · RNF: {len(RNF)}")
    print(f"Tablas: {documento.n_tabla} · Figuras: {documento.n_figura}")
