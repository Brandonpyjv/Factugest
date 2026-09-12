# FactuGest

**Backend de facturación electrónica para Colombia**, construido como una plataforma middleware: cualquier sistema (POS, ERP, e-commerce) puede emitir facturas, notas crédito y notas débito válidas ante la DIAN llamando a una sola API REST, sin implementar por su cuenta el cálculo tributario, la numeración autorizada, el CUFE, el XML UBL 2.1 o el PDF.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.135-009688?logo=fastapi&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-raw%20SQL-4479A1?logo=mysql&logoColor=white)
![Tests](https://img.shields.io/badge/tests-158%2B-brightgreen)
![Status](https://img.shields.io/badge/status-en%20desarrollo-yellow)

[English overview](#english-overview) · [Documentación en español](#documentación-en-español)

---

## English overview

FactuGest is a Colombian **electronic invoicing engine**, built as a monolithic FastAPI service that plays two roles at once:

1. **A commercial back office** (Jinja2 admin panel) where FactuGest manages its own customers, invoicing plans, inventory and financial dashboard.
2. **A DIAN middleware REST API** (`/api/v1/`) that any third-party system integrates with to issue tax-compliant electronic invoices, credit notes and debit notes on its own behalf, authenticated with a per-client API key.

Both faces share the same business logic layer (`services/`), so tax math, numbering and document generation are implemented and tested exactly once.

### Key features

- **Electronic documents** — invoices, credit notes and debit notes with per-line and invoice-level discounts, prorated VAT, CUFE generation, UBL 2.1 XML and a PDF representation rendered per-issuer (logo, brand color, or an auto-generated monogram when there's no logo).
- **Integration API** (`/api/v1/`) — API-key authentication, idempotent issuance via an external reference, a single consistent error contract, and plan-based usage quotas.
- **Inventory control** — stock is only ever modified through one service, every movement is journaled (kardex), with low-stock alerts and valuation.
- **Reporting dashboard** — service metrics (documents issued, DIAN acceptance, recurring revenue) and commercial metrics (net sales, collections, aging), with configurable date ranges and Chart.js visualizations.
- **Audit trail** — an append-only log of who did what, keeping the actor's name even if the account is later renamed or deleted.
- **Role-based access** — a four-level role hierarchy (`ADMIN` → `JEFE_TIENDA` → `SUPERVISOR` → `CAJERO`) shared by the panel and the API.
- **DIAN provider adapter** — a swappable interface (`simulado` today, a real provider pluggable behind the same contract) so switching who actually transmits to the DIAN doesn't touch the rest of the system.

### Tech stack

| Layer | Choice | Why |
|---|---|---|
| Web framework | FastAPI | Async-ready, automatic OpenAPI docs (`/docs`), native request validation via Pydantic — a good fit for an API-first invoicing service. |
| Templating | Jinja2 + Bootstrap 5 | Server-rendered admin panel, no separate frontend build to maintain. |
| Database | MySQL, raw SQL (`mysql-connector-python`) | No ORM — every query is explicit and reviewable, which matters for financial data. |
| Documents | ReportLab (PDF), custom UBL 2.1 XML builder, `qrcode`, `num2words` | Full control over the legal representation of a tax document. |
| Auth | `bcrypt` (passwords), cookie sessions for the panel, hashed API keys for integrations | Two different consumers (people vs. systems), two matching auth mechanisms. |
| Tests | `pytest`, 158+ unit tests | Covers tax calculation, the canonical document contract and PDF/XML edge cases — no database required to run them. |

### Architecture in one line

```
routes/            thin HTTP layer (Jinja views + JSON API), no business logic
  └── api/v1/       the integration API: API-key auth, Pydantic contracts, uniform errors
services/           all business logic — tax math, numbering, documents, inventory, reports
  └── shared by both the web panel and the API, so nothing is implemented twice
database.py         four small helpers over raw SQL (execute_query / execute_update / get_one / get_many)
```

See the [full documentation below](#arquitectura) for the complete module map, the data model and how to run the project locally.

---

## Documentación en español

### Tabla de contenido

- [¿Qué es FactuGest?](#qué-es-factugest)
- [Funcionalidades](#funcionalidades)
- [Arquitectura](#arquitectura)
- [Modelo de datos](#modelo-de-datos)
- [Seguridad y autenticación](#seguridad-y-autenticación)
- [Cómo levantar el proyecto](#cómo-levantar-el-proyecto)
- [Pruebas](#pruebas)
- [Contexto del proyecto](#contexto-del-proyecto)
- [Roadmap](#roadmap)

### ¿Qué es FactuGest?

FactuGest es un motor de **facturación electrónica para Colombia**. Nació como un sistema de punto de venta con facturación integrada y evolucionó a un modelo de **proveedor tecnológico / middleware DIAN**: en vez de ser el software que un negocio usa para facturar, es la API que **cualquier** software (un POS, un ERP, una tienda en línea) llama para que sus ventas salgan como documentos electrónicos válidos, sin tener que implementar por su cuenta el cálculo de impuestos, la numeración autorizada por la DIAN, el CUFE, el XML UBL 2.1 ni la representación en PDF.

El mismo backend sirve dos frentes con la misma lógica de negocio:

- Un **panel web** (Jinja2 + Bootstrap) donde FactuGest administra sus propios clientes, planes de facturación, inventario, reportes y tablero financiero.
- Una **API REST de integración** (`/api/v1/`) que consumen sistemas externos, autenticada con una llave por cliente (`X-API-Key`), no con sesión de usuario.

### Funcionalidades

**Documentos electrónicos**
- Facturas, notas crédito y notas débito, con referencia al documento origen.
- Descuentos por línea y por factura, cada uno calculado sobre la base que le corresponde, con prorrateo de IVA.
- CUFE, XML UBL 2.1 y PDF, generados por cada emisor (no por FactuGest): logo y color de marca propios, o un monograma con las iniciales generado al momento si la empresa no tiene logo.
- Consecutivos reservados de forma atómica por emisor, con un índice único como red de seguridad ante concurrencia.

**API de integración (`/api/v1/`)**
- Autenticación por API key (`X-API-Key`), una llave por cliente integrado; solo se guarda el hash de la llave, nunca el secreto.
- Emisión idempotente: si el integrador reintenta con la misma `referencia_externa`, recibe el mismo documento en vez de emitir uno duplicado (y gastar un número de la resolución DIAN por nada).
- Cupo de emisión por plan contratado, verificado antes de reservar el número.
- Contrato de error único (`{"detail": {"codigo", "mensaje", "campo"}}`) para todos los códigos de estado, del 401 al 500.
- Documentación automática e interactiva en `/docs` (Swagger) y `/redoc`.

**Control de inventario**
- Toda modificación de stock pasa por un único servicio (`inventory_service`), que además registra el movimiento (kardex). Nunca hay un `UPDATE` de stock suelto en otra parte del código.
- Alertas de stock bajo y valorización de inventario.
- Productos marcados como servicio (`controla_stock = 0`) quedan fuera del control de stock sin generar errores.

**Tablero de control y reportes**
- Dos secciones: el servicio (documentos emitidos, aceptación DIAN, ingreso recurrente) y la venta (ventas netas, cartera, cobranza), cada una con su propio filtro de periodo.
- Series temporales con granularidad ajustable (día / semana / mes), sugerida automáticamente según el rango elegido.
- Ocho reportes exportables a CSV y PDF.
- Vista reducida para el rol `CAJERO`, sin cifras financieras.

**Auditoría**
- Registro de solo-escritura de quién hizo qué, cuándo y desde dónde, en las rutas que modifican datos.
- Un fallo al auditar nunca tumba la operación que se estaba auditando.

**Roles**
```
ADMIN (4) > JEFE_TIENDA (3) > SUPERVISOR (2) > CAJERO (1)
```
Los tres primeros tienen acceso administrativo completo; `CAJERO` queda limitado a la operación de facturación diaria.

### Arquitectura

```
FactuGest/
├── main.py                  Punto de entrada FastAPI: middlewares, registro de routers
├── auth.py                  Autenticación de sesión del panel, hash de contraseñas, roles
├── database.py               Helpers sobre SQL directo: execute_query, execute_update, get_one, get_many
├── migrate.py                Migraciones de esquema, versionadas e idempotentes
│
├── routes/                   Capa HTTP — sin lógica de negocio
│   ├── invoice.py, customer.py, productos.py, users.py, ...     Panel web (Jinja2)
│   ├── inventory.py, reports.py, dashboard.py, auditoria.py     Inventario, reportes, tablero
│   ├── clientes_api.py, documentos.py, consumo.py               Administración de la plataforma
│   └── api/v1/                                                  API de integración
│       ├── dependencias.py    Resuelve y valida la API key del cliente
│       ├── facturas.py        POST /facturas · GET /documentos
│       ├── notas.py           POST /notas-credito · POST /notas-debito
│       └── errores.py         Forma única de error para toda la API
│
├── services/                 Toda la lógica de negocio — compartida entre panel y API
│   ├── calculo_documento.py   Aritmética tributaria pura: bases, descuentos, prorrateo de IVA
│   ├── numeracion_service.py  Reserva atómica de consecutivos por emisor
│   ├── documento_canonico.py  Contrato de entrada de pdf_service y xml_service
│   ├── pdf_service.py / xml_service.py / cufe_service.py
│   ├── inventory_service.py   Único punto de escritura de stock (kardex)
│   ├── report_service.py / export_service.py
│   ├── api_key_service.py     Genera, verifica y rota llaves de integración
│   ├── auditoria_service.py   Registro de auditoría, solo-escritura
│   └── dian_proveedor.py      Interfaz intercambiable del proveedor que transmite a la DIAN
│
├── templates/                 Vistas Jinja2 (layout.html + una carpeta por dominio)
├── static/                     CSS, JS, imágenes
└── tests/                      Pruebas unitarias (no requieren base de datos)
```

**Patrón clave**: `routes/` son *thin wrappers* — reciben la petición, llaman a un `service` y devuelven una respuesta. Toda la lógica de negocio vive en `services/`, así el panel web y la API JSON reutilizan exactamente el mismo código para calcular impuestos, numerar y generar documentos.

### Modelo de datos

La base de datos separa lo que FactuGest vende de lo que emite por cuenta de terceros:

| Zona | Tablas | Contenido |
|---|---|---|
| Comercial | `facturas`, `detalle_factura`, `customers`, `productos` | Las propias ventas de FactuGest: los planes de facturación. |
| Middleware | `clientes_api`, `receptores`, `documentos`, `documento_lineas`, `documento_eventos` | Lo emitido por cuenta de terceros a través de la API. |
| Puente | `facturas_plan` | Qué mes de qué cliente ya se facturó, enlazando la venta con el documento electrónico correspondiente. |
| Compartida | `empresas`, `municipios`, `impuestos` | Emisores y catálogos DIAN. |

Un documento emitido para un tercero nunca se guarda en `facturas`: esa tabla alimenta el tablero y los reportes propios de FactuGest, así que mezclar ambas cosas haría que la facturación de un cliente apareciera como ingreso propio.

### Seguridad y autenticación

- **Panel web**: sesiones basadas en cookie (`SessionMiddleware` + `AuthMiddleware`), con cierre automático por inactividad. Contraseñas con `bcrypt`.
- **API de integración**: cada cliente tiene su propia llave (`X-API-Key`). Solo se guarda el hash de la llave — nunca el secreto — y se puede rotar o suspender sin tocar el resto de la cuenta.
- **Separación de roles** compartida entre panel y API.
- Ninguna credencial real, dato personal ni volcado de base de datos vive en este repositorio: las variables de entorno se configuran a partir de [`.env.example`](.env.example), y los datos de demostración se generan localmente con `seed_proveedor.py`.

### Cómo levantar el proyecto

**Requisitos**: Python 3.10+, MySQL (por ejemplo vía XAMPP), Git.

```bash
# 1. Clonar y crear el entorno virtual
git clone https://github.com/Brandonpyjv/Factugest.git
cd Factugest
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac
pip install -r requirements.txt

# 2. Configurar variables de entorno
copy .env.example .env        # Windows
cp .env.example .env          # Linux/Mac
# Edita .env con tus datos locales de MySQL

# 3. Crear la base de datos vacía en MySQL, luego:
python migrate.py             # aplica el esquema versionado
python seed_proveedor.py      # datos de demostración (opcional)

# 4. Arrancar
python main.py
# o, con recarga automática:
uvicorn main:app --reload
```

La aplicación queda en `http://127.0.0.1:8000`. La documentación interactiva de la API de integración está en `/docs` (Swagger) y `/redoc`.

### Pruebas

```bash
pip install -r requirements-dev.txt
python -m pytest
```

Más de 150 pruebas unitarias cubren la aritmética tributaria, el contrato del documento canónico y los puntos donde el emisor cambia la salida del PDF y del XML. No requieren base de datos.

### Contexto del proyecto

FactuGest nació como **proyecto de grado** (Tecnólogo en Análisis y Desarrollo de Software, SENA), evaluado contra tres objetivos específicos, todos cumplidos:

1. **Emisión de documentos electrónicos** — facturas, notas crédito y notas débito con cálculo de bases gravables, descuentos y prorrateo de IVA, consecutivo, CUFE, PDF y XML UBL 2.1.
2. **Control de inventarios** — stock dinámico con alertas por bajo volumen y kardex de entradas y salidas.
3. **Reportes y tablero de control** — métricas financieras y comerciales, exportables.

Sobre esa base se construyó un cuarto objetivo, la **API REST de integración** (`/api/v1/`), que llevó al proyecto de ser un sistema de punto de venta que factura a ser una plataforma que cualquier sistema de punto de venta puede usar para facturar.

### Roadmap

- [ ] Conexión con un proveedor tecnológico real ante la DIAN (hoy el proveedor `simulado` valida el documento sin transmitirlo).
- [ ] Despliegue fuera de entorno local: contenedores, HTTPS y dominio propio.
- [ ] Ampliar la cobertura de pruebas de integración sobre la API.

---

## Licencia

Proyecto académico y de portafolio. No tiene una licencia de código abierto asignada todavía — todos los derechos reservados salvo que se indique lo contrario.
