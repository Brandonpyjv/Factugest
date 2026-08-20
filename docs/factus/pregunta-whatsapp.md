# Mensaje para Factus (WhatsApp)

Redactado el 2026-08-20. Copiar y pegar. Va en tres mensajes seguidos para que se lea
—un bloque de 40 líneas en WhatsApp no lo lee nadie—.

La pregunta que de verdad importa es la **1** del segundo mensaje: si la respuesta es
«una cuenta por empresa», cambia el diseño del adaptador y hay que rehacer la parte de
credenciales. Las demás son de trámite.

---

## Mensaje 1 — quiénes somos y qué tenemos

> Buenas, [nombre]. Te escribo para concretar la integración técnica y aprovecho para
> contarte bien el caso de uso, porque creo que define qué plan necesitamos.
>
> Somos **FactuGest**, un software de facturación que estamos desarrollando en Cúcuta. La
> particularidad es que **no vendemos el software a un solo negocio**: funcionamos como
> capa intermedia. Nuestros clientes son pequeños negocios —droguerías, panaderías,
> ferreterías, consultorios— que siguen usando su propio sistema (su POS, su software de
> siempre), y ese sistema **se conecta a una API nuestra** para emitir. Nosotros les
> resolvemos la parte electrónica sin que tengan que cambiar de programa.
>
> Ya lo tenemos construido y funcionando: API REST propia con autenticación por llave por
> cliente, cálculo de impuestos, generación de la representación gráfica en PDF, XML,
> control de consecutivos por empresa, notas crédito y débito, y envío por correo al
> comprador. **Lo único que nos falta es la transmisión real a la DIAN**, que es donde
> entran ustedes. Ya dejamos hecha la capa de conexión: internamente el sistema tiene una
> pieza intercambiable de "proveedor DIAN", hoy en modo simulado, esperando que entre
> Factus.

## Mensaje 2 — las preguntas

> Leyendo su documentación de developers me quedaron estas dudas, y la primera es la que
> nos define el diseño:
>
> **1. ¿Una cuenta de Factus puede emitir por cuenta de varias empresas (varios NIT)?**
> En la documentación veo que `GET /v2/companies` devuelve *la* empresa del usuario, en
> singular, y que los rangos de numeración cuelgan de esa cuenta. Nosotros necesitamos
> emitir a nombre de **cada uno de nuestros clientes**, cada uno con su NIT, su resolución
> y su numeración. ¿Existe un esquema de **partner / integrador / revendedor** que permita
> eso con una sola credencial? ¿O el modelo correcto es **una cuenta de Factus por cada
> cliente nuestro**, y nosotros administramos esas credenciales?
> Es lo que más necesitamos saber, porque cambia cómo lo construimos.
>
> **2. Credenciales de sandbox.** ¿Nos pueden habilitar `client_id`, `client_secret`,
> usuario y contraseña de pruebas para empezar a integrar ya? ¿Vienen con un rango de
> numeración de pruebas cargado, o lo creamos nosotros con `POST /v2/numbering-ranges`?
>
> **3. Costo y cupos.** ¿Cómo es el cobro: por documento, por paquete mensual, con cuota
> mínima? Lo pregunto porque nosotros también le cobramos un plan mensual con cupo a
> nuestros clientes, y necesito que los números cuadren por dentro.
>
> **4. Paso a producción.** ¿Qué implica pasar de sandbox a producción? ¿El set de pruebas
> ante la DIAN lo presentan ustedes o nosotros? ¿Cuánto suele tardar la habilitación?
>
> **5. Representación gráfica.** Vi que `POST /v2/bills/:number/send-email` acepta un
> `pdf_base_64_encoded` propio. ¿Eso significa que podemos seguir usando **nuestro PDF**
> —con el logo y el membrete de cada empresa emisora— y que ustedes lo empaquetan con su
> XML AttachedDocument? Quiero confirmarlo antes de contar con ello.

## Mensaje 3 — cierre

> Quedo atento también a la documentación que me iban a enviar por correo, por si trae algo
> distinto de lo que está publicado en developers.factus.com.co. Gracias.

---

## Notas para mí (no enviar)

- Si la respuesta a la 1 es **«una cuenta por empresa»**: hay que guardar las credenciales
  de Factus por cliente, cifradas, en `clientes_api`, y `ProveedorFactus` deja de ser un
  objeto único para construirse por cliente. Preguntar entonces si el alta de cada cuenta
  se puede hacer por API o es un trámite manual con ellos — si es manual, condiciona el
  tiempo de dar de alta a un cliente nuevo.
- Si la respuesta a la 5 es **no**, el PDF de la fase de puesta a punto (membrete por
  emisor, logo, monograma, descuentos) deja de llegarle al comprador y pasa a ser solo
  nuestra copia interna. No se pierde, pero cambia el discurso de la sustentación.
- No mencionar precios propios ni el número de clientes: todavía son catorce de
  demostración, no reales.
