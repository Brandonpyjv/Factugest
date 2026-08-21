"""
E3 — Documentación de los casos de uso de FactuGest.

Los casos salen de `casos_de_uso.py`, el mismo catálogo del que se dibujan los
diagramas de E2. Aquí se les agregan los campos de comportamiento: precondiciones,
secuencia normal, flujos alternos, postcondiciones y excepciones.

Dos niveles de detalle, a propósito. Documentar los cincuenta y seis casos con
ficha completa produce sesenta páginas en las que los casos que deciden si el
sistema sirve —emitir, numerar, cobrar, autenticar— quedan sepultados entre fichas
que repiten el mismo formulario de un mantenimiento de catálogo. Los diecisiete
casos críticos llevan ficha completa; los treinta y nueve restantes van en formato
breve, con su precondición y su resultado esperado, que es lo que de ellos hay que
verificar.

    python e3_documentacion.py
"""
from pathlib import Path

import casos_de_uso as catalogo
from apa import DocumentoAPA, inicial_minuscula

SALIDA = Path(__file__).resolve().parent.parent / "entregables"
ARCHIVO = SALIDA / "FactuGest - Documentacion de Casos de Uso.docx"

# --- Fichas completas: los casos de los que depende que el sistema sirva ---------
# codigo: (precondiciones, secuencia normal, flujos alternos, postcondiciones, excepciones)

DETALLE = {
"CU-01": (
    ["El administrador ha iniciado sesión con un rol administrativo.",
     "Existe la empresa emisora con su resolución de facturación vigente.",
     "Existe el cliente comercial al que se le facturará la suscripción."],
    ["El administrador abre el módulo de clientes API y solicita registrar uno nuevo.",
     "El sistema presenta el formulario con los planes disponibles y las empresas emisoras.",
     "El administrador diligencia NIT, razón social, correo, plan y empresa emisora.",
     "El sistema valida los datos y comprueba que el NIT no esté ya registrado.",
     "El sistema genera la llave de acceso y guarda únicamente el hash de su secreto.",
     "El sistema registra el cliente con estado ACTIVO y el cupo del plan elegido.",
     "El sistema muestra la llave completa una sola vez, advirtiendo que no volverá a "
     "mostrarse.",
     "El sistema anota la creación en el registro de auditoría."],
    [("El plan elegido no trae cupo",
      ["Si el plan es ilimitado, el sistema registra el cliente sin límite mensual y omite "
       "la validación de cupo en las emisiones posteriores."])],
    ["El cliente queda registrado y en condiciones de emitir.",
     "El administrador tiene la llave para entregarla al integrador.",
     "Del secreto de la llave solo queda su hash en la base."],
    ["Si el NIT ya está registrado, el sistema rechaza el alta y lo informa.",
     "Si la empresa emisora no tiene resolución vigente, el sistema advierte que el cliente "
     "no podrá emitir hasta corregirlo.",
     "Si el administrador abandona la pantalla sin copiar la llave, esta no puede "
     "recuperarse, y hay que rotarla."],
),
"CU-06": (
    ["El administrador ha iniciado sesión con un rol administrativo.",
     "El cliente API existe y tiene una llave vigente."],
    ["El administrador abre el detalle del cliente y solicita rotar la llave.",
     "El sistema advierte que la llave actual dejará de funcionar de inmediato.",
     "El administrador confirma la rotación.",
     "El sistema genera una llave nueva y reemplaza el prefijo y el hash almacenados.",
     "El sistema muestra la llave nueva una sola vez.",
     "El sistema anota la rotación en auditoría, sin registrar la credencial."],
    [("Rotación por sospecha de compromiso",
      ["El administrador puede suspender al cliente antes de rotar, de modo que ninguna "
       "petición se atienda mientras el integrador recibe la llave nueva."])],
    ["La llave anterior queda invalidada y las peticiones que la usen reciben 401.",
     "El cliente conserva su historial de documentos y su consumo del mes.",
     "En auditoría consta quién rotó, cuándo y sobre qué cliente."],
    ["Si el integrador no actualiza la llave, sus emisiones fallarán con llave inválida "
     "hasta que lo haga.",
     "Si falla el guardado, la llave anterior sigue vigente, y no se invalida nada hasta que "
     "la nueva quede escrita."],
),
"CU-08": (
    ["El sistema cliente cuenta con una llave válida y su estado es ACTIVO.",
     "La empresa emisora tiene resolución vigente con numeración disponible.",
     "El cliente no ha agotado el cupo de documentos de su plan en el mes."],
    ["El sistema cliente envía los datos de la venta, con el comprador, las líneas, los impuestos y "
     "descuentos.",
     "El sistema valida la estructura de la petición y el contenido de cada campo.",
     "El sistema comprueba el cupo disponible del cliente para el mes en curso.",
     "El sistema abre una transacción y reserva el siguiente consecutivo autorizado.",
     "El sistema calcula bases gravables, descuentos, prorrateo de IVA y totales.",
     "El sistema guarda la cabecera y el detalle del documento.",
     "El sistema genera el CUFE, la representación gráfica en PDF y el archivo XML UBL 2.1.",
     "El sistema confirma la transacción y responde con el número, el CUFE y el estado.",
     "El sistema agenda el envío del documento al comprador como tarea de fondo."],
    [("Reenvío con la misma referencia externa",
      ["Si la petición trae una referencia externa ya utilizada, el sistema no emite otro "
       "documento y responde con el que ya había expedido.",
       "El consecutivo no se consume y el cupo no se descuenta por segunda vez."]),
     ("Emisión desde el formulario web",
      ["Un cajero puede originar el mismo caso desde el panel; el recorrido a partir del "
       "paso 2 es idéntico, porque la lógica de emisión es la misma."])],
    ["Existe un documento electrónico con número consecutivo único y CUFE.",
     "El consumo del cliente en el mes aumentó en un documento.",
     "El PDF y el XML quedan disponibles para su descarga.",
     "El evento de emisión queda anotado en la bitácora del documento."],
    ["Si la llave falta o no sirve, el sistema responde 401 y no emite.",
     "Si el cliente está suspendido o revocado, responde 403 sin emitir.",
     "Si el cupo del plan está agotado, responde 403 con el código cupo_agotado, antes "
     "de reservar el consecutivo.",
     "Si algún dato es inválido, responde 422 señalando el campo.",
     "Si falla cualquier paso dentro de la transacción, esta se revierte por completo y el "
     "consecutivo queda libre."],
),
"CU-09": (
    ["Existe la factura de origen, emitida por la misma empresa emisora.",
     "El sistema cliente cuenta con una llave válida y activa."],
    ["El sistema cliente envía la nota indicando la factura de origen y el concepto de la "
     "corrección.",
     "El sistema valida que la factura referenciada exista y pertenezca al mismo emisor.",
     "El sistema reserva el consecutivo de notas crédito del emisor.",
     "El sistema calcula los totales de la nota sobre las líneas informadas.",
     "El sistema guarda el documento con su referencia a la factura de origen.",
     "El sistema genera el CUFE, el PDF y el XML, y responde al sistema cliente."],
    [("Nota por anulación total",
      ["Cuando la nota cubre la totalidad de la factura, se emite por el mismo valor y el "
       "documento de origen queda corregido en su totalidad."])],
    ["Existe la nota crédito con su referencia a la factura de origen.",
     "El consumo del mes aumentó en un documento.",
     "Si el documento afectaba existencias, estas se reintegran."],
    ["Si la factura de origen no existe o es de otro emisor, el sistema responde 422.",
     "El cupo agotado no impide emitir la nota, porque negarle a un cliente la corrección de "
     "una factura mal emitida lo dejaría con un documento equivocado ante la DIAN y sin "
     "forma de arreglarlo hasta el mes siguiente."],
),
"CU-11": (
    ["La empresa emisora tiene prefijo, resolución y rango autorizado registrados.",
     "El caso se ejecuta dentro de la transacción de emisión."],
    ["El sistema solicita el siguiente número para el emisor y el tipo de documento.",
     "El sistema incrementa el consecutivo y devuelve el valor reservado en una sola "
     "sentencia.",
     "El sistema entrega el número al caso que lo invocó."],
    [],
    ["El número queda reservado y ningún otro documento puede obtenerlo.",
     "Si la transacción que lo invocó se revierte, el consecutivo queda sin usar."],
    ["Si el rango autorizado se agotó, el sistema interrumpe la emisión e informa que la "
     "resolución debe renovarse.",
     "Si dos peticiones coinciden en el mismo instante, la sentencia única garantiza que "
     "cada una obtenga un número distinto; el índice único de la base actúa como última "
     "defensa."],
),
"CU-13": (
    ["El documento ya fue guardado con su cabecera y su detalle.",
     "La empresa emisora tiene registrados sus datos de identificación."],
    ["El sistema calcula el CUFE del documento.",
     "El sistema arma la representación gráfica con el membrete, el logo y el color de la "
     "empresa emisora.",
     "Si la empresa no tiene logo, el sistema dibuja el monograma con sus iniciales sobre "
     "su color de marca.",
     "El sistema construye el archivo XML bajo el estándar UBL 2.1.",
     "El sistema deja ambos archivos disponibles para su descarga."],
    [],
    ["El documento cuenta con su CUFE, su PDF y su XML.",
     "El PDF lleva la identidad de la empresa emisora, no la del proveedor tecnológico."],
    ["Si faltan datos obligatorios del emisor o del comprador, la generación se interrumpe "
     "y el fallo queda anotado en los eventos del documento."],
),
"CU-14": (
    ["El documento fue emitido correctamente.",
     "El comprador tiene una dirección de correo registrada.",
     "El servidor de correo está configurado."],
    ["El sistema arma el mensaje con el PDF y el XML adjuntos.",
     "El sistema lo envía en segundo plano, después de haber respondido a quien emitió.",
     "El sistema anota el resultado del envío en la bitácora del documento."],
    [("Comprador sin correo",
      ["Si el comprador no tiene correo registrado, el envío se omite y así queda anotado. "
       "La emisión no se ve afectada."])],
    ["El comprador recibe los dos archivos.",
     "En la bitácora del documento consta si el envío salió, se omitió o falló."],
    ["Si el servidor de correo no responde, el intento se anota como fallido y el documento "
     "sigue siendo válido, ya que la emisión había terminado.",
     "Si no hay servidor configurado, el envío se anota como omitido y no se interrumpe "
     "nada."],
),
"CU-18": (
    ["El cliente API está identificado y su estado es ACTIVO.",
     "Se está solicitando la emisión de una factura de venta."],
    ["El sistema cuenta los documentos que el cliente emitió en el mes en curso.",
     "El sistema compara ese conteo con el cupo del plan contratado.",
     "Si queda cupo, el sistema autoriza continuar con la emisión.",
     "Si no queda, el sistema interrumpe antes de reservar el consecutivo."],
    [("Plan sin límite",
      ["Si el plan del cliente es ilimitado, la validación se resuelve siempre a favor."]),
     ("Documento distinto de una factura",
      ["Las notas crédito y débito no se bloquean por cupo, aunque sí lo consumen."])],
    ["La emisión continúa, o se rechaza sin haber gastado un número de la resolución."],
    ["Si el cupo está agotado, el sistema responde 403 con el código cupo_agotado y un "
     "mensaje que indica el plan y el consumo alcanzado."],
),
"CU-20": (
    ["El mes a facturar ya cerró.",
     "El cliente está activo y no tiene facturada esa mensualidad.",
     "La llave del propio proveedor está configurada en el entorno."],
    ["El administrador abre el módulo de consumo y elige el cliente y el periodo.",
     "El sistema muestra el consumo del periodo, el plan y los excedentes si los hubo.",
     "El administrador confirma la facturación de la mensualidad.",
     "El sistema arma el documento con el plan y, si corresponde, los documentos "
     "excedentes.",
     "El sistema emite la factura por su propia API, con la referencia externa "
     "PLAN-<cliente>-<periodo>.",
     "El sistema guarda en la facturación propia el número y el CUFE que la API devolvió.",
     "El sistema registra el puente entre la mensualidad y el cliente del periodo."],
    [("Cliente sin consumo en el periodo",
      ["La mensualidad se factura igual, porque el plan se cobra por disponibilidad del servicio, "
       "no por uso."])],
    ["El cliente tiene su factura del periodo, con número y CUFE reales.",
     "El periodo queda marcado como cobrado y desaparece de la cola de pendientes."],
    ["Si la API falla, no se guarda ninguna factura, ya que emitir va antes que guardar, para no "
     "dejar una factura propia sin número real.",
     "Si se pulsa el botón dos veces, la referencia externa hace que la segunda petición "
     "devuelva el documento ya emitido en lugar de crear otro."],
),
"CU-23": (
    ["El usuario ha iniciado sesión con permiso para facturar.",
     "Existen el cliente y los servicios que se van a facturar."],
    ["El usuario abre el formulario de nueva factura.",
     "El usuario selecciona el cliente y agrega los planes o servicios con su cantidad.",
     "El sistema calcula bases, descuentos, impuestos y totales en pantalla.",
     "El usuario indica la forma de pago y confirma la emisión.",
     "El sistema reserva el consecutivo, guarda la factura y su detalle en una sola "
     "transacción.",
     "El sistema genera el PDF y el XML y muestra la factura emitida."],
    [("Descuento sobre una línea",
      ["El usuario puede aplicar un descuento a una línea indicando su concepto, que viaja "
       "con la línea hasta el PDF."])],
    ["La factura queda registrada en la facturación propia del proveedor.",
     "La operación queda anotada en auditoría."],
    ["Si falta un dato obligatorio, el sistema devuelve el formulario señalando el campo.",
     "Si la transacción falla, no queda factura ni se consume el consecutivo."],
),
"CU-26": (
    ["Existe la factura y su saldo pendiente es mayor que cero.",
     "El usuario ha iniciado sesión con un rol administrativo."],
    ["El usuario abre la factura y elige registrar un pago.",
     "El usuario indica el valor, la fecha y el método de pago.",
     "El sistema valida que el valor no supere el saldo pendiente.",
     "El sistema registra el pago y recalcula el saldo.",
     "El sistema actualiza el estado de la factura si el saldo quedó en cero."],
    [("Pago parcial",
      ["Si el pago no cubre el total, la factura conserva su estado pendiente y el saldo "
       "disminuye."])],
    ["El pago queda registrado y la cartera refleja el nuevo saldo.",
     "Los reportes de cartera y de cobro incorporan el movimiento."],
    ["Si el valor supera el saldo, el sistema rechaza el registro.",
     "Si la factura está anulada, no admite pagos."],
),
"CU-33": (
    ["El usuario ha iniciado sesión con un rol con acceso a reportes.",
     "Existe operación registrada en el periodo consultado."],
    ["El usuario abre el módulo de reportes y elige uno de los siete disponibles.",
     "El usuario define el rango de fechas y, si su rol lo permite, la empresa.",
     "El sistema consulta la información y calcula las cifras del reporte.",
     "El sistema presenta el resultado en pantalla con su título y su subtítulo de "
     "filtros."],
    [("Exportación",
      ["Desde el resultado, el usuario puede descargarlo en CSV o en PDF conservando los "
       "mismos filtros."])],
    ["El usuario obtiene la información solicitada, acotada al periodo y al alcance de su "
     "rol."],
    ["Si el rango no contiene operación, el reporte se presenta vacío e indica que no hay "
     "datos en el periodo.",
     "Si el rol no alcanza a la empresa solicitada, el sistema restringe el resultado a la "
     "empresa del usuario."],
),
"CU-43": (
    ["El usuario está registrado y su cuenta está activa."],
    ["El usuario abre el formulario de ingreso.",
     "El usuario escribe su nombre de usuario y su contraseña.",
     "El sistema compara la contraseña contra el hash almacenado.",
     "El sistema abre la sesión y guarda el rol y la empresa del usuario.",
     "El sistema anota el ingreso en auditoría.",
     "El sistema presenta el panel correspondiente al rol."],
    [("Usuario con rol de cajero",
      ["El sistema presenta el panel operativo reducido, sin cifras financieras."])],
    ["El usuario queda autenticado y el reloj de inactividad empieza a correr.",
     "El ingreso queda registrado."],
    ["Si las credenciales no coinciden, el sistema lo informa sin precisar cuál de los dos "
     "datos falló y anota el intento fallido.",
     "Si la cuenta está inactiva, el sistema niega el acceso.",
     "Tras el tiempo de inactividad configurado, la sesión se cierra sola."],
),
"CU-48": (
    ["Se completó una operación de escritura sobre el sistema.",
     "Existe una sesión con un usuario identificado."],
    ["La ruta que ejecutó la operación invoca el registro de auditoría.",
     "El sistema toma el usuario, su nombre, la acción, la entidad y su identificador.",
     "El sistema redacta la descripción en ese momento, con los datos del hecho.",
     "El sistema guarda el registro con la fecha y la dirección de origen."],
    [],
    ["Queda constancia de quién hizo qué y cuándo.",
     "El registro conserva el nombre del usuario aunque después se elimine su cuenta."],
    ["Si el registro falla, la excepción se captura y se envía al log del servidor, y la "
     "operación auditada no se interrumpe. Un sistema que deja de facturar porque no "
     "pudo anotar que facturó es peor que uno sin auditoría.",
     "Ninguna credencial entra al registro, de modo que rotar una llave se anota pero la llave no."],
),
"CU-50": (
    ["El sistema cliente incluye el encabezado X-API-Key en la petición."],
    ["El sistema separa el prefijo del secreto en la llave recibida.",
     "El sistema localiza el cliente por el prefijo, que se guarda en claro.",
     "El sistema verifica el secreto contra el hash almacenado.",
     "El sistema comprueba el estado del cliente.",
     "El sistema resuelve la empresa emisora con la que ese cliente numera y continúa."],
    [],
    ["La petición queda asociada al cliente integrado y a su empresa emisora."],
    ["Si falta la llave o no corresponde a ningún cliente, el sistema responde 401.",
     "Si la llave es válida pero el cliente está suspendido o revocado, responde 403. La "
     "distinción importa, porque en el primer caso el integrador revisa su configuración, en el "
     "segundo tiene que hablar con el proveedor."],
),
"CU-51": (
    ["El sistema cliente está autenticado por su llave.",
     "El cuerpo de la petición cumple el contrato publicado en OpenAPI."],
    ["El sistema cliente envía la petición de emisión al recurso correspondiente.",
     "El sistema valida el cuerpo contra el modelo de entrada.",
     "El sistema ejecuta la emisión del documento solicitado.",
     "El sistema responde con el identificador, el número, el CUFE y el estado.",
     "El sistema cliente guarda esos datos y continúa su propia operación."],
    [("Consulta posterior",
      ["El sistema cliente puede recuperar después el documento, su PDF y su XML mediante "
       "el identificador recibido."])],
    ["El documento queda emitido y el sistema externo conoce su número y su CUFE.",
     "La empresa cumplió su obligación sin cambiar el software con el que opera."],
    ["Todos los errores se devuelven con la misma estructura de código estable, mensaje "
     "legible y campo señalado.",
     "De un fallo inesperado, la traza va al log del servidor y al cliente solo le llega "
     "que la operación falló."],
),
"CU-56": (
    ["El sistema cliente reenvía una petición con una referencia externa ya utilizada."],
    ["El sistema busca un documento del mismo cliente con esa referencia externa.",
     "El sistema encuentra el documento ya emitido.",
     "El sistema responde con ese documento, sin emitir uno nuevo."],
    [],
    ["No se duplica el documento ni se consume un consecutivo adicional.",
     "El consumo del cliente no aumenta por el reintento."],
    ["Si la referencia externa no se envía, el sistema no puede reconocer el reintento y "
     "emitirá un documento nuevo, y por eso el contrato recomienda enviarla siempre."],
),
}

# --- Formato breve: precondición y resultado esperado ----------------------------

BREVE = {
"CU-02": ("El cliente API se está registrando o su llave se está rotando.",
          "Existe una llave nueva; del secreto solo queda su hash."),
"CU-03": ("El administrador ha iniciado sesión.",
          "Obtiene el listado de clientes integrados con su plan, estado y consumo."),
"CU-04": ("El cliente API existe.",
          "Los datos, el plan o el cupo quedan actualizados y la operación queda auditada."),
"CU-05": ("El cliente API existe.",
          "El cliente queda suspendido, reactivado o revocado; su historial se conserva."),
"CU-07": ("El cliente API no tiene documentos emitidos asociados.",
          "El cliente se retira del sistema sin afectar la trazabilidad de lo emitido."),
"CU-10": ("Existe la factura de origen del mismo emisor.",
          "Se emite la nota débito con su referencia y su CUFE."),
"CU-12": ("El documento tiene sus líneas cargadas.",
          "Quedan calculadas las bases, los descuentos, el prorrateo de IVA y los totales."),
"CU-15": ("El usuario tiene acceso al módulo de documentos emitidos.",
          "Obtiene lo emitido por cuenta de terceros con los filtros aplicados."),
"CU-16": ("El documento existe y fue emitido.",
          "Se descargan la representación gráfica y el archivo XML."),
"CU-17": ("Existen clientes integrados con documentos emitidos en el mes.",
          "Se conoce el consumo de cada cliente frente al cupo de su plan."),
"CU-19": ("El mes anterior ya cerró.",
          "Se obtiene la lista de clientes activos con la mensualidad sin facturar."),
"CU-21": ("El cliente emitió más documentos de los que incluye su plan.",
          "Los documentos excedentes quedan valorados para incluirse en la mensualidad."),
"CU-22": ("Hay clientes con consumo cercano al cupo de su plan.",
          "Se identifican los clientes a los que conviene ofrecer el plan siguiente."),
"CU-24": ("El usuario tiene permiso sobre el módulo de clientes.",
          "El cliente queda registrado, actualizado o eliminado, y la operación auditada."),
"CU-25": ("El usuario tiene un rol administrativo.",
          "El catálogo de planes y servicios queda actualizado con su precio e impuesto."),
"CU-27": ("La factura existe.",
          "El estado de pago queda actualizado y los reportes de cartera lo reflejan."),
"CU-28": ("Existe la factura propia de origen.",
          "Se emite la nota crédito o débito con su referencia a la factura de origen."),
"CU-29": ("El usuario ha iniciado sesión.",
          "Obtiene las facturas del proveedor con búsqueda, filtros y paginación."),
"CU-30": ("La factura existe y fue emitida.",
          "Se descargan el PDF y el XML de la factura del proveedor."),
"CU-31": ("El usuario tiene acceso al tablero.",
          "Ve los indicadores del servicio y de la venta del periodo seleccionado."),
"CU-32": ("Se está consultando el tablero o un reporte.",
          "Las cifras quedan acotadas al rango de fechas y a la empresa indicada."),
"CU-34": ("Existe un reporte generado.",
          "Se descarga el archivo CSV con los mismos filtros del reporte."),
"CU-35": ("Existe un reporte generado.",
          "Se descarga el PDF del reporte con su título y sus filtros."),
"CU-36": ("El usuario tiene rol de cajero.",
          "Ve el panel operativo, sin cifras financieras ni datos de otros clientes."),
"CU-37": ("El usuario tiene un rol administrativo.",
          "Ve los catálogos del sistema agrupados por finalidad y con su conteo."),
"CU-38": ("El usuario tiene un rol administrativo.",
          "El catálogo de impuestos queda actualizado con su tarifa y su código DIAN."),
"CU-39": ("El usuario tiene un rol administrativo.",
          "El catálogo de descuentos queda actualizado."),
"CU-40": ("El usuario tiene un rol administrativo.",
          "Los métodos de pago y los estados de factura quedan actualizados."),
"CU-41": ("El usuario tiene un rol administrativo.",
          "La empresa emisora queda registrada con su resolución, prefijo y rango."),
"CU-42": ("Existe la empresa emisora.",
          "La empresa queda con su logo y su color; sin logo se usa el monograma."),
"CU-44": ("Existe una sesión abierta.",
          "La sesión se cierra, por decisión del usuario o por inactividad, y queda anotada."),
"CU-45": ("El usuario tiene rol de administrador.",
          "El usuario queda creado, actualizado o eliminado, con su contraseña en hash."),
"CU-46": ("El usuario existe.",
          "El rol y la empresa determinan a qué rutas y a qué cifras alcanza."),
"CU-47": ("El usuario edita su propia foto o la de alguien de menor jerarquía.",
          "La imagen queda validada, normalizada y asociada al usuario."),
"CU-49": ("El usuario tiene rol de administrador.",
          "Obtiene el rastro de operaciones filtrado por usuario, acción, entidad o fecha."),
"CU-52": ("El sistema cliente está autenticado.",
          "Obtiene sus documentos emitidos o el detalle de uno de ellos."),
"CU-53": ("El documento existe y pertenece al cliente autenticado.",
          "Obtiene el PDF o el XML del documento por la interfaz de integración."),
"CU-54": ("El integrador configuró su llave.",
          "Confirma que la llave es válida antes de intentar emitir."),
"CU-55": ("La API está disponible.",
          "Obtiene la especificación OpenAPI para construir su integración."),
}

ETIQUETAS = ["Código", "Módulo", "Actores", "Requisitos que cubre", "Descripción",
             "Precondiciones", "Secuencia normal", "Flujos alternos", "Postcondiciones",
             "Excepciones"]


def _viñetas(elementos):
    return "\n".join(f"- {e}" for e in elementos) if elementos else "No aplica."


def _pasos(elementos):
    return "\n".join(f"{i}. {e}" for i, e in enumerate(elementos, start=1))


def _alternos(bloques):
    if not bloques:
        return "No aplica."
    partes = []
    for nombre, pasos in bloques:
        partes.append(f"{nombre}:")
        partes.extend(f"   {i}. {p}" for i, p in enumerate(pasos, start=1))
    return "\n".join(partes)


def construir():
    d = DocumentoAPA()
    d.portada(
        titulo="FACTUGEST",
        subtitulo="Documentación de casos de uso",
        integrantes=["Brandon Arley Restrepo Gélvez",
                     "Johan Sebastián Acosta Sánchez",
                     "Wilmer Jesús Contreras Rangel"],
        grado="Ficha 3115426\nTecnólogo en Análisis y Desarrollo de Software",
        institucion=["SERVICIO NACIONAL DE APRENDIZAJE (SENA)",
                     "Centro de la Industria, la Empresa y los Servicios (CIES)",
                     "Tecnólogo en Análisis y Desarrollo de Software"],
        ciudad="CÚCUTA, NORTE DE SANTANDER",
        anio=2026,
    )
    d.tabla_contenido()

    _introduccion(d)
    _fichas(d)
    _breves(d)

    SALIDA.mkdir(parents=True, exist_ok=True)
    d.guardar(ARCHIVO)
    return d


def _introduccion(d):
    d.titulo("1. Introducción", nivel=1)
    d.parrafo(
        "Este documento describe el comportamiento de los casos de uso de FactuGest. Mientras "
        "el diagrama muestra qué hace el sistema y quién lo usa, la documentación establece "
        "cómo transcurre cada caso, esto es, con qué condiciones empieza, qué pasos recorre, qué "
        "caminos alternos admite, en qué estado deja al sistema y qué ocurre cuando algo "
        "sale mal."
    )
    d.parrafo(
        f"Los casos son los mismos {len(catalogo.todos())} del documento de diagramas y "
        "conservan su código. La documentación se presenta en dos niveles de detalle."
    )
    d.parrafo(
        f"Los {len(DETALLE)} casos críticos llevan ficha completa. Son aquellos de los que "
        "depende que el sistema cumpla su propósito, como la emisión de documentos, la reserva de "
        "la numeración autorizada, el control del cupo, el cobro de la suscripción, la "
        "autenticación de los sistemas integrados y el registro de auditoría. En ellos, el "
        "orden de los pasos y el comportamiento ante el error no son un detalle de "
        "implementación, y son emitir antes de guardar, o validar el cupo antes de reservar el "
        f"consecutivo, cambia el resultado. Los {len(BREVE)} restantes se presentan en "
        "formato breve, con su precondición y su resultado esperado."
    )
    d.parrafo(
        "La distinción no es una reducción del alcance sino una decisión sobre qué merece "
        "detalle. Documentar los cincuenta y seis con ficha completa produciría sesenta "
        "páginas en las que los casos que deciden si el sistema sirve quedarían sepultados "
        "entre repeticiones del mismo formulario de mantenimiento de un catálogo. Los casos "
        "breves siguen siendo verificables, porque su resultado esperado es lo que la prueba "
        "comprueba."
    )

    d.titulo("1.1 Estructura de la ficha", nivel=2)
    d.tabla(
        "Campos de la ficha de caso de uso",
        ["Campo", "Qué registra"],
        [
            ["Código y módulo", "Identificación del caso y módulo al que pertenece."],
            ["Actores", "Quiénes participan. Los casos incluidos no tienen actor, y los "
                        "ejecuta el sistema como parte de otro caso."],
            ["Requisitos que cubre", "Requisitos funcionales que el caso satisface."],
            ["Descripción", "Objetivo del caso en una frase."],
            ["Precondiciones", "Lo que debe cumplirse antes de empezar."],
            ["Secuencia normal", "Los pasos del camino en que todo sale bien."],
            ["Flujos alternos", "Caminos válidos distintos del normal."],
            ["Postcondiciones", "Estado en que queda el sistema al terminar."],
            ["Excepciones", "Qué ocurre cuando algo falla y cómo responde el sistema."],
        ],
        nota="Elaboración propia con base en el formato de documentación de casos de uso.",
        anchos=[4.2, 12.1],
    )


def _fichas(d):
    d.titulo("2. Casos de uso críticos", nivel=1, nueva_pagina=True)
    d.parrafo(
        "Las fichas siguen el orden de los módulos. Cada una es autosuficiente y puede leerse "
        "sin haber leído la anterior, que es como se consulta esta clase de documento."
    )

    catalogo_completo = {c[0]: c for c in catalogo.todos()}
    for indice, codigo in enumerate(DETALLE, start=1):
        _, nombre, modulo, actores, descripcion, rf = catalogo_completo[codigo]
        precondiciones, flujo, alternos, postcondiciones, excepciones = DETALLE[codigo]

        d.titulo(f"2.{indice} {codigo}. {nombre}", nivel=2, nueva_pagina=True)
        d.tabla(
            f"Ficha del caso de uso {codigo}, {inicial_minuscula(nombre)}",
            ["CASO DE USO", f"{codigo}. {nombre}"],
            [
                ["Módulo", modulo],
                ["Actores", ", ".join(actores) if actores else
                 "Ninguno. Es un caso incluido que ejecuta el sistema."],
                ["Requisitos que cubre", rf],
                ["Descripción", descripcion],
                ["Precondiciones", _viñetas(precondiciones)],
                ["Secuencia normal", _pasos(flujo)],
                ["Flujos alternos", _alternos(alternos)],
                ["Postcondiciones", _viñetas(postcondiciones)],
                ["Excepciones", _viñetas(excepciones)],
            ],
            nota="Elaboración propia.",
            anchos=[3.6, 12.7],
        )


def _breves(d):
    d.titulo("3. Casos de uso complementarios", nivel=1, nueva_pagina=True)
    d.parrafo(
        f"Los {len(BREVE)} casos restantes se presentan agrupados por módulo, con la "
        "condición que debe cumplirse para ejecutarlos y el resultado que debe observarse al "
        "terminar. En su mayoría corresponden a consultas y a mantenimiento de catálogos, "
        "cuyo recorrido es el mismo en todos los casos, porque el usuario abre el módulo, el sistema "
        "presenta lo existente, el usuario registra o modifica, el sistema valida, guarda y "
        "confirma."
    )

    for _, nombre_modulo, _, _, casos, *_ in catalogo.MODULOS:
        suyos = [(c, n, a, rf) for c, n, a, _, rf in casos if c in BREVE]
        if not suyos:
            continue
        d.tabla(
            f"Casos complementarios del módulo de {nombre_modulo[0].lower()}{nombre_modulo[1:]}",
            ["Código", "Caso de uso", "Actores", "Precondición", "Resultado esperado"],
            [[c, n, ", ".join(a) if a else "Sistema", BREVE[c][0], BREVE[c][1]]
             for c, n, a, rf in suyos],
            nota="Elaboración propia.",
            anchos=[1.5, 3.1, 2.6, 4.5, 4.6],
        )


if __name__ == "__main__":
    documento = construir()
    faltan = [c for c, *_ in catalogo.todos() if c not in DETALLE and c not in BREVE]
    sobran = [c for c in list(DETALLE) + list(BREVE)
              if c not in {x[0] for x in catalogo.todos()}]
    print(f"Generado: {ARCHIVO}")
    print(f"Fichas completas: {len(DETALLE)} · Breves: {len(BREVE)} · "
          f"Total: {len(DETALLE) + len(BREVE)} de {len(catalogo.todos())}")
    if faltan:
        print(f"  ⚠ sin documentar: {faltan}")
    if sobran:
        print(f"  ⚠ documentados pero fuera del catálogo: {sobran}")
    print(f"Tablas: {documento.n_tabla}")
