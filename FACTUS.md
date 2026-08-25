# Factus — lo que hace falta para transmitir a la DIAN de verdad

Extraído de `https://developers.factus.com.co/` el **2026-08-20**, antes de que llegue la
documentación por correo. Si el correo trae algo distinto, **manda el correo**: esto es una
lectura de la web pública, no un contrato firmado.

Factus es el proveedor tecnológico habilitado por la DIAN que pondremos detrás de
`services/dian_proveedor.py`. Nosotros seguimos siendo el sistema que el cliente usa;
Factus es quien firma y transmite.

---

## 1 · Lo esencial en diez líneas

| | |
|---|---|
| **Autenticación** | OAuth2 *password grant*. Token **válido 1 hora**, con *refresh token*. |
| **Base sandbox** | `https://api-sandbox.factus.com.co` |
| **Base producción** | `https://api.factus.com.co` |
| **Formato** | JSON. Todos los valores numéricos van como **string**, máximo dos decimales. |
| **Límite** | **80 peticiones por minuto** por usuario → `429` con `Retry-After`. |
| **Emitir factura** | `POST /v2/bills/validate` → devuelve `number`, `cufe`, `qr`, `public_url`. |
| **Idempotencia** | Campo `reference_code`. Repetirlo devuelve la factura existente, no crea otra. |
| **Numeración** | **La asigna Factus** desde el rango de numeración, no nosotros. |
| **CUFE y XML** | Los genera y firma **Factus**. No los calculamos nosotros. |
| **Una cuenta = una empresa** | `GET /v2/companies` devuelve *la* empresa del usuario. Ver §7. |

---

## 2 · Autenticación

`POST /oauth/token` — cuerpo como **form-data**, no JSON:

| Campo | Valor |
|---|---|
| `grant_type` | `password` |
| `client_id` | el que entrega Factus |
| `client_secret` | el que entrega Factus |
| `username` | correo del usuario |
| `password` | contraseña del usuario |

Devuelve `access_token` y `refresh_token`. Para renovar, el mismo endpoint con
`grant_type=refresh_token`.

Todas las demás peticiones llevan:

```http
Authorization: Bearer {access_token}
Content-Type: application/json
Accept: application/json
```

> El token dura **una hora**. Hay que cachearlo y renovarlo solo cuando caduque: pedir uno
> nuevo en cada emisión gasta dos peticiones del límite de 80/minuto por cada factura.

---

## 3 · Emitir una factura

`POST /v2/bills/validate`

### Cuerpo mínimo

```json
{
  "reference_code": "FG-2026-000124",
  "document": "01",
  "numbering_range_id": 389,
  "operation_type": "10",
  "observation": "",
  "payment_details": [
    { "payment_form": "1", "payment_method_code": "10", "amount": "83300" }
  ],
  "customer": {
    "identification_document_code": "31",
    "identification": "900874512",
    "dv": "3",
    "legal_organization_code": "1",
    "tribute_code": "01",
    "responsibilities": ["R-99-PN"],
    "company": "Droguería La Salud S.A.S.",
    "address": "Calle 11 # 6-32",
    "email": "compras@lasalud.co",
    "phone": "6075742210",
    "municipality_code": "54001"
  },
  "items": [
    {
      "code_reference": "PLAN-PRO",
      "name": "Plan Profesional — agosto 2026",
      "quantity": "1.00",
      "discount_rate": "0.00",
      "price": "70000.00",
      "unit_measure_code": "94",
      "standard_code": "999",
      "taxes": [ { "code": "01", "rate": "19.00" } ]
    }
  ]
}
```

### Campos de nivel raíz

| Campo | Req. | Nota |
|---|---|---|
| `reference_code` | **sí** | Único por documento. **Es la idempotencia**: si se repite, devuelve el existente. |
| `document` | no | `01` por defecto (factura de venta). `03` = instrumento de transmisión. |
| `numbering_range_id` | condicional | Obligatorio solo si hay **más de un rango activo**. |
| `operation_type` | no | `10` (estándar) por defecto. |
| `send_email` | no | `true` por defecto. **Ver §6**: ponerlo en `false` si queremos mandar nuestro propio PDF. |
| `observation` | no | Máx. 500 caracteres (la *skill* oficial dice 250; usar 250 por seguridad). |
| `created_time` | no | `HH:mm:ss`. |
| `currency` | no | Para mostrar totales en moneda extranjera. Si se envía, sus campos internos son obligatorios. |
| `cash_rounding_amount` | no | Concilia la suma de `payment_details` contra el total. Máx. ±500,00. |
| `prepayment_details[]` | no | Anticipos: `reference_code`, `received_date`, `amount`, `note`. |
| `establishment` | no | Solo con varias sedes. Todos sus campos pasan a obligatorios. |
| `billing_period` | no | Servicios públicos, arriendos, matrículas. |
| `order_reference` | no | Orden de pedido: `reference_code`, `issue_date`. |
| `related_documents[]` | condicional | Obligatorio cuando `document` = `03`. |
| `allowance_charges[]` | no | **Descuentos y recargos a nivel de factura** — ver §9, nos afecta. |

### `payment_details[]` (obligatorio)

| Campo | Req. | Nota |
|---|---|---|
| `payment_form` | sí | `1` contado · `2` crédito. |
| `payment_method_code` | sí | `10` efectivo, `42` consignación, `47` transferencia… |
| `amount` | sí | **La suma de todos debe igualar el total con impuestos.** |
| `reference_code` | no | Referencia interna del pago. |
| `due_date` | condicional | **Obligatorio si `payment_form` = `2`** (crédito). `YYYY-MM-DD`. |

### `customer` (obligatorio)

| Campo | Req. | Nota |
|---|---|---|
| `identification_document_code` | sí | `13` cédula, `31` NIT… |
| `identification` | sí | **Sin dígito de verificación ni guion.** |
| `dv` | no | Solo para NIT. Si se omite, Factus lo calcula; **si se envía mal, error**. |
| `legal_organization_code` | sí | `1` jurídica · `2` natural. |
| `tribute_code` | no | `01` IVA · `ZZ` no aplica (por defecto). |
| `responsibilities[]` | no | `R-99-PN` por defecto. |
| `company` | condicional | Obligatorio si `legal_organization_code` = `1`. |
| `names` | condicional | Obligatorio si `legal_organization_code` = `2`. |
| `trade_name`, `address`, `email`, `phone`, `country_code`, `municipality_code` | no | |

### `items[]` (obligatorio)

| Campo | Req. | Nota |
|---|---|---|
| `code_reference` | sí | Nuestro código de producto. |
| `name` | sí | |
| `quantity` | sí | Máx. dos decimales. |
| `price` | sí | Unitario, **sin impuestos ni descuentos**. |
| `unit_measure_code` | sí | `94` = unidad. |
| `standard_code` | sí | `999` = adopción del contribuyente. |
| `discount_rate` **o** `discount_amount` | no | **Uno u otro, nunca los dos.** |
| `note` | no | |
| `taxes[]` | sí | `{ "code": "01", "rate": "19.00", "is_excluded": false }` |
| `withholding_taxes[]` | no | Autorretenciones: `code`, `rate`. |

> **Regla que hay que grabarse**: un campo opcional de tipo objeto o array, *en cuanto
> lleva datos*, vuelve obligatorios todos sus campos internos. No se puede mandar medio
> objeto.

### Respuesta `201 Created`

```json
{
  "status": "Created",
  "data": {
    "reference_code": "FG-2026-000124",
    "number": "SETP990002443",
    "is_validated": true,
    "validated_at": "13-05-2026 08:21:49 AM",
    "cufe": "a821f2e05cb1b82e0f74...",
    "errors": {},
    "links": {
      "qr": "https://catalogo-vpfe-hab.dian.gov.co/document/searchqr?documentkey=...",
      "public_url": "https://app-sandbox.factus.com.co/documents/bills/..."
    },
    "totals": {
      "gross_amount": "70000.00", "taxable_amount": "70000.00",
      "tax_amount": "13300.00", "total": "83300.00"
    },
    "customer": {}, "items": [], "company": {}, "numbering_range": {}
  }
}
```

**Lo que hay que guardar sí o sí**: `number`, `cufe`, `links.qr`, `links.public_url` y
`is_validated`.

---

## 4 · Aceptado, rechazado y «no se sabe»

Esto es lo más delicado de toda la integración, porque son **tres** estados y no dos.

| Situación | Cómo se reconoce | Qué se hace |
|---|---|---|
| **Validada** | `is_validated: true` | Guardar número y CUFE. Listo. |
| **Rechazada** | `is_validated: false` **y** `errors` contiene la palabra *«Rechazo»* | **Eliminar** el documento por su `reference_code`, corregir y volver a emitir. Si no se elimina, **la API no deja procesar los siguientes envíos**. |
| **La DIAN se demoró** | `is_validated: false` **y** `errors` *sin* rechazo | **No eliminar.** Reintentar con los mismos datos: la API detecta el reintento y consulta el estado actual. |

Y un cuarto caso, el `409 Conflict`: *«Se encontró una factura pendiente por enviar a la
DIAN»* → eliminar por referencia y crear de nuevo.

> **`errors` con contenido no significa rechazo.** `FAJ44b` y `RUT01` son *notificaciones*
> (el nombre en el RUT no coincide letra por letra) y la factura es válida igual. Lo que
> decide es `is_validated`. Un integrador que trate cualquier `errors` como fallo va a
> anular facturas buenas.

`DELETE /v2/bills/destroy/reference/:reference_code` — solo funciona mientras el documento
**no** esté validado.

---

## 5 · Notas crédito y débito

| | Crédito | Débito |
|---|---|---|
| Endpoint | `POST /v2/credit-notes/validate` | `POST /v2/debit-notes/validate` |
| Referencia a la factura | `bill_number` | `bill_number` |
| Concepto | `correction_concept_code` | `correction_concept_code` |
| Tipo de operación | `customization_id`: `20` con factura · `22` sin factura | `30` con factura · `32` sin factura |

**Conceptos de corrección — nota crédito**: `1` devolución parcial · `2` anulación de la
factura · `3` rebaja o descuento · `4` ajuste de precio · `5` pronto pago · `6` volumen.

**Conceptos — nota débito**: `1` intereses · `2` gastos por cobrar · `3` cambio de valor ·
`4` otros.

Cuando `customization_id` = `22` (sin referencia a factura), `billing_period` pasa a ser
obligatorio.

---

## 6 · PDF, XML y correo

| Qué | Endpoint |
|---|---|
| PDF de Factus | `GET /v2/bills/:number/download-pdf` → `pdf_base_64_encoded` |
| XML firmado | `GET /v2/bills/:number/download-xml` → `xml_base_64_encoded` |
| XML *AttachedDocument* | `GET /v2/bills/:number/download-attached-document-xml` |
| Enviar por correo | `POST /v2/bills/:number/send-email` |

**El hallazgo que nos importa**: el endpoint de correo acepta un
`pdf_base_64_encoded` **nuestro**. Es decir, **nuestro `pdf_service` no se tira a la
basura**: podemos seguir generando la representación gráfica con el membrete, el logo, el
monograma y los descuentos que ya construimos, y que sea *esa* la que reciba el comprador.
Factus arma el ZIP con nuestro PDF más su XML `AttachedDocument`.

Condición: hay que emitir con **`send_email: false`**, o Factus manda el suyo primero.

---

## 7 · Rangos de numeración — aquí se rompe un invariante nuestro

`GET /v2/numbering-ranges` devuelve, por cada rango: `id`, `document`, `prefix`, `from`,
`to`, **`current`** (siguiente número sin usar), `resolution_number`, `start_date`,
`end_date`, `technical_key`, `is_expired`, `is_active`.

Códigos de documento para rangos: `21` factura · `22` nota crédito · `23` nota débito ·
`24` documento soporte · `25` nota de ajuste · `30` talonario.

También existen `POST /v2/numbering-ranges` (crear), `PATCH .../current` (mover el
consecutivo), `PATCH .../toggle-status` y `GET /v2/numbering-ranges/dian` (los rangos que
la DIAN tiene asociados al software).

> ⚠️ **Consecuencia directa**: hoy `services/numeracion_service.reservar_numero()` asigna
> el consecutivo **antes** de emitir, dentro de la transacción. Con Factus, **el número lo
> pone Factus** y llega en la respuesta. Los dos no pueden mandar a la vez. Ver §10.

---

## 8 · Tablas de referencia (las que usaremos)

**Tipo de identificación** — `11` registro civil · `12` tarjeta de identidad ·
`13` cédula · `21` tarjeta de extranjería · `22` cédula de extranjería · `31` NIT ·
`41` pasaporte · `42` documento extranjero · `47` PEP · `48` PPT · `50` NIT otro país ·
`91` NUIP.

**Tipo de organización** — `1` jurídica · `2` natural.

**Tributos del cliente** — `01` IVA · `ZZ` no aplica.

**Impuestos** — `01` IVA · `04` INC · `35` ultraprocesados.
**Retenciones** — `05` ReteIVA · `06` Retefuente.

**Formas de pago** — `1` contado · `2` crédito.

**Métodos de pago** — `10` efectivo · `20` cheque · `42` consignación · `47` transferencia ·
`48` tarjeta crédito · `49` tarjeta débito · `71` bonos · `72` vales · `1` no definido ·
`ZZZ` otro.

**Responsabilidades fiscales** — `O-13` gran contribuyente · `O-15` autorretenedor ·
`O-23` agente de retención de IVA · `O-47` régimen simple · `R-99-PN` no responsable.

**Estándar de producto** — `999` adopción del contribuyente · `001` UNSPSC ·
`010` GTIN · `020` partida arancelaria.

**Tipos de operación** — `10` estándar · `11` mandatos · `12` transporte de carga ·
`SS-*` sector salud.

**Eventos RADIAN** — `030` acuse de recibo · `031` reclamo · `032` recibo del bien ·
`033` aceptación expresa · `034` aceptación tácita.

Municipios y unidades de medida tienen endpoint propio y son tablas largas:
`/tablas-de-referencia/municipios` y `/tablas-de-referencia/unit-measures`.

---

## 9 · Endpoints completos

### Facturas
```
POST   /v2/bills/validate
GET    /v2/bills                                    listar y filtrar
GET    /v2/bills/:number
DELETE /v2/bills/destroy/reference/:reference_code
GET    /v2/bills/:number/download-pdf
GET    /v2/bills/:number/download-xml
GET    /v2/bills/:number/download-attached-document-xml
POST   /v2/bills/:number/send-email                 acepta PDF propio
GET    /v2/bills/:number/email-content
GET    /v2/bills/:number/radian/events
POST   /v2/bills/:number/radian/events/:event_type  aceptación tácita
```

### Notas
```
POST   /v2/credit-notes/validate     ·  POST /v2/debit-notes/validate
GET    /v2/credit-notes[/:number]    ·  GET  /v2/debit-notes[/:number]
DELETE /v2/credit-notes/reference/:reference_code   (ídem débito)
GET    /v2/{credit|debit}-notes/:number/download-{pdf|xml}
POST   /v2/{credit|debit}-notes/:number/send-email
```

### Numeración, empresa y utilidades
```
GET    /v2/numbering-ranges          ·  POST /v2/numbering-ranges
GET    /v2/numbering-ranges/:id      ·  DELETE /v2/numbering-ranges/:id
PATCH  /v2/numbering-ranges/:id/current
PATCH  /v2/numbering-ranges/:id/toggle-status
GET    /v2/numbering-ranges/dian
GET    /v2/companies    ·  PUT /v2/companies  ·  POST /v2/companies/logo
GET    /v2/subscriptions                       cupo del plan: asignado, consumido, disponible
GET    /v2/dian/acquirer?identification_document_code=&identification_number=
```

### Fuera de nuestro alcance hoy
Documentos soporte (`/v2/support-documents`), notas de ajuste
(`/v2/adjustment-notes`), nómina electrónica (`/v2/payrolls`,
`/v2/adjustment-payrolls`) y recepción de documentos (`/v2/receptions`).

### Códigos HTTP
`200` · `201` · `204` · `400` · `401` · `402` pago requerido · `403` · `404` ·
`409` conflicto · `422` validación · `429` demasiadas · `500` · `503`.

---

## 10 · Qué hay que cambiar en FactuGest

La buena noticia: **la costura ya está hecha**. `services/dian_proveedor.py` define
`ProveedorDian.transmitir()` y `RespuestaDian`, y esa clase ya contempla que un proveedor
real devuelva su propio `numero`, `cufe`, `xml` y `pdf`. `get_proveedor()` incluso nombra
`factus` como pendiente. Lo que sigue es trabajo concreto, no rediseño.

### 10.1 · Lo que se puede hacer tal cual

| Ya lo tenemos | Encaja con |
|---|---|
| `reference_code` idempotente | Nuestra `referencia_externa` (`PLAN-<cliente>-<AAAA-MM>`) es exactamente eso. |
| `calculo_documento.py` | Factus recibe `price` sin impuestos y la tasa; nuestra aritmética sigue siendo la fuente. |
| `pdf_service.py` con membrete, logo y monograma | `send-email` acepta nuestro PDF (§6). No se tira nada. |
| Tabla `documentos` | Ya tiene `numero`, `cufe`, `qr`, `xml`, `estado`, `proveedor_dian`, `referencia_externa`. |
| `documento_eventos` | Es donde va el rastro de cada intento contra Factus. |
| `consumo_service` | `GET /v2/subscriptions` da el cupo *de Factus*; el nuestro es otro y sigue valiendo. |

### 10.2 · Lo que hay que construir

1. **`ProveedorFactus(ProveedorDian)`** en `services/dian_proveedor.py`: token cacheado
   con su hora de caducidad, armado del JSON, envío, y traducción de la respuesta a
   `RespuestaDian`.
2. **Un mapeo de códigos.** Nuestras columnas guardan cosas como `regimen_tributario =
   'RESPONSABLE_IVA'` y `tipo_documento`; Factus quiere `tribute_code`,
   `legal_organization_code`, `responsibilities[]`, `unit_measure_code`, `standard_code`.
   Hace falta una tabla de traducción.
   **Los municipios ya están**: nuestro `municipios.cod_municipio` guarda el código DANE
   (`05001` Medellín) y es el mismo que Factus pide como `municipality_code` (su ejemplo,
   `68679`, es San Gil en DANE). Solo hay que comprobar el cero a la izquierda.
3. **Manejo de los tres estados** de §4, con el borrado por referencia en el caso de
   rechazo. Sin eso, un rechazo deja la cuenta bloqueada para las siguientes facturas.
4. **Reintento y límite de 80/min.** El `429` con `Retry-After` hay que respetarlo.

### 10.3 · Lo que hay que decidir — y son decisiones, no detalles

**a) La numeración deja de ser nuestra.** Hoy `reservar_numero()` asigna el consecutivo
dentro de la transacción de emisión, y el índice único `(cod_empresa, tipo, numero)` lo
protege. Con Factus el número llega **después** de emitir. Dos caminos:

- *Factus manda*: guardamos el documento sin número, llamamos a Factus, escribimos el
  número que devuelva. Es lo correcto —el número de la resolución es de quien la tiene—,
  pero rompe la emisión atómica: hay una llamada de red en medio.
- *Seguimos numerando nosotros* y solo usamos a Factus para firmar. **No sirve**: Factus
  numera desde su propio rango, y tendríamos dos numeraciones distintas para el mismo
  documento.

  → Recomendación: **Factus manda**. La transacción se parte en dos: primero se guarda el
  documento en estado `PENDIENTE` sin número, después se transmite y se completa. El
  estado ya existe —`documentos.estado` maneja `PENDIENTE`, `ACEPTADO` y `RECHAZADO`— y es
  además lo que ya hace el POS con sus ventas pendientes, así que el patrón está probado
  en el proyecto.

**b) Una cuenta de Factus = una empresa emisora.** `GET /v2/companies` devuelve *la*
empresa del usuario autenticado, en singular, y `PUT /v2/companies` actualiza esa. **La
documentación pública no describe forma de emitir por cuenta de catorce empresas con una
sola credencial.** Eso choca de frente con lo que somos: un middleware que emite por cuenta
de terceros.

  → Hay que preguntárselo a Factus directamente. Las salidas posibles: un esquema de
  *partner* o revendedor no documentado, o **una credencial de Factus por cada cliente
  nuestro**, guardada cifrada en `clientes_api`. Si es lo segundo, `ProveedorFactus` deja
  de ser un objeto único y pasa a construirse por cliente. **Esta es la pregunta que hay
  que hacer en el correo**, porque cambia el diseño del adaptador.

**c) El CUFE y el XML propios pasan a ser de mentira.** `cufe_service.py` y
`xml_service.py` generan un CUFE simulado y un XML sin firmar. Con Factus los reales
llegan de allá. No hay que borrarlos —el proveedor `simulado` los sigue usando para las
pruebas sin red— pero **lo que se guarde en `documentos.cufe` cuando el proveedor sea
`factus` tiene que ser el de Factus**, nunca el nuestro. Mezclarlos sería guardar un
identificador fiscal inventado.

**d) Descuentos de factura.** Los nuestros se prorratean sobre el IVA en
`calculo_documento`. Factus tiene `allowance_charges[]` a nivel de factura *y*
`discount_rate`/`discount_amount` por línea. Hay que comprobar contra el sandbox si
mandando solo los descuentos de línea salen los mismos totales que calculamos nosotros, o
si hay que usar `allowance_charges`. Si los totales no cuadran, Factus rechaza.

### 10.4 · Lo que hace falta de Factus, y todavía no tenemos

- [ ] `client_id`, `client_secret`, `username` y `password` **de sandbox**.
- [ ] Confirmación de si existe esquema **multiempresa / partner** (§10.3b). *Es lo más
      importante del correo.*
- [ ] Rango de numeración de pruebas ya cargado, o instrucciones para crearlo.
- [ ] Costo por documento y cupos, para que cuadre con lo que cobramos en `/consumo`.
- [ ] Cómo se pasa de sandbox a producción: habilitación ante la DIAN, set de pruebas,
      tiempos.

---

## 11 · Plan de trabajo sugerido

1. Pedir credenciales de sandbox y **preguntar lo de multiempresa** — bloquea el diseño.
2. Añadir la tabla de traducción de códigos y el código DIAN de municipio.
3. Escribir `ProveedorFactus` contra el sandbox, con pruebas que no salgan a la red
   (respuestas grabadas), igual que se hizo con `ProveedorSimulado`.
4. Partir la emisión en dos pasos (`PENDIENTE` → transmitido) y mover la reserva de
   consecutivo detrás de una bandera: si el proveedor numera, no numeramos.
5. Emitir una factura real en sandbox y comparar totales, PDF y XML contra los nuestros.
6. Enviar el correo con **nuestro** PDF (`send_email: false` + `send-email` con
   `pdf_base_64_encoded`).
7. Notas crédito y débito.
8. Producción.

---

## 12 · Qué quedó guardado en el repo

- `docs/factus/skill-factus-crear-factura.md` — la *skill* oficial de Factus para
  asistentes de IA, tal como la publican. Es el contrato completo de la factura estándar,
  con ejemplos y reglas, y ellos mismos dicen que se agregue al proyecto.
- `docs/factus/tablas-de-referencia-dian.txt` — todas las tablas de códigos.

Las 121 páginas completas quedaron descargadas fuera del repo, en el directorio temporal
de esta sesión. No se comitean: son documentación de un tercero y se envejece sola.

---

## 13 · Fuentes

Documentación pública de Factus, consultada el 2026-08-20:

- `https://developers.factus.com.co/autenticacion/auth/`
- `https://developers.factus.com.co/buenas-practicas/primeros-pasos/`
- `https://developers.factus.com.co/facturas/crear-y-validar/`
- `https://developers.factus.com.co/skills/facturas-crear-y-validar.md` — Factus publica
  una *skill* para asistentes de IA con el contrato completo de la factura estándar; es la
  fuente más limpia de todas.
- `https://developers.factus.com.co/notas-credito/crear-y-validar/`
- `https://developers.factus.com.co/rangos-de-numeracion/facturación/obtener-rangos/`
- `https://developers.factus.com.co/manejo-errores/`
- `https://developers.factus.com.co/limite-de-request/`
- `https://developers.factus.com.co/tablas-de-referencia/tablas/`
- `https://developers.factus.com.co/facturas/representacion-grafica/`
