# Factugest — Documentación del Sistema

**Versión:** 2.0
**Fecha:** Marzo 2026
**Framework:** FastAPI + Jinja2 + MySQL

---

## Tabla de Contenidos

1. [¿Qué es Factugest?](#1-qué-es-factugest)
2. [Stack Tecnológico](#2-stack-tecnológico)
3. [Estructura del Proyecto](#3-estructura-del-proyecto)
4. [Arquitectura en Capas](#4-arquitectura-en-capas)
5. [Base de Datos](#5-base-de-datos)
6. [Módulos del Sistema](#6-módulos-del-sistema)
7. [Flujo de Trabajo Completo](#7-flujo-de-trabajo-completo)
8. [Cálculo de Impuestos y Totales](#8-cálculo-de-impuestos-y-totales)
9. [Generación de PDF](#9-generación-de-pdf)
10. [Referencia de Endpoints](#10-referencia-de-endpoints)
11. [Cumplimiento DIAN](#11-cumplimiento-dian)
12. [Cambios Realizados vs Versión Anterior](#12-cambios-realizados-vs-versión-anterior)
13. [Cómo Ejecutar el Proyecto](#13-cómo-ejecutar-el-proyecto)

---

## 1. ¿Qué es Factugest?

Factugest es un sistema de facturación electrónica para Colombia, construido con FastAPI y renderizado del lado del servidor con Jinja2. Permite gestionar el ciclo completo de facturación: desde la configuración de maestros (clientes, productos, impuestos) hasta la emisión de facturas electrónicas con desglose DIAN y generación de PDF.

El sistema fue migrado originalmente de Flask a FastAPI y evolucionado de un sistema de solo lectura a un CRUD completo con lógica de negocio para cumplimiento tributario colombiano.

---

## 2. Stack Tecnológico

| Componente | Tecnología |
|---|---|
| Backend | FastAPI (Python 3.x) |
| Servidor ASGI | Uvicorn |
| Templates | Jinja2 (server-side rendering) |
| Base de Datos | MySQL / MariaDB |
| Driver DB | mysql-connector-python |
| Generación PDF | ReportLab 4.2.5 |
| Frontend | Bootstrap 5.3.2 + Bootstrap Icons |
| ORM | Ninguno (SQL puro) |

---

## 3. Estructura del Proyecto

```
Factugest/
├── main.py                    # Punto de entrada, registro de routers
├── database.py                # Capa de acceso a datos (funciones helper)
├── templates_config.py        # Configuración Jinja2
├── requirements.txt
│
├── routes/                    # Controladores HTTP (APIRouter)
│   ├── invoice.py             # Facturas
│   ├── customer.py            # Clientes
│   ├── branches.py            # Empresas / Sucursales
│   ├── productos.py           # Productos
│   ├── users.py               # Usuarios
│   ├── taxes.py               # Impuestos
│   ├── payment_methods.py     # Métodos de pago
│   ├── invoice_payments.py    # Estados de pago (pagos_factura)
│   ├── discounts.py           # Descuentos
│   ├── logs.py                # Logs del sistema
│   └── product_discount.py    # Descuentos por producto
│
├── services/                  # Lógica de negocio y consultas SQL
│   ├── invoice_service.py
│   ├── customer_service.py
│   ├── branches.py
│   ├── products_service.py
│   ├── user_service.py
│   ├── taxes.py
│   ├── payment_methods_service.py
│   ├── invoice_payments_service.py
│   ├── discounts.py
│   └── pdf_service.py         # Generación de PDF con ReportLab
│
├── templates/                 # Plantillas HTML (Jinja2)
│   ├── layout.html            # Base con navbar y sidebar
│   ├── index.html             # Dashboard
│   ├── invoice/
│   │   ├── index.html         # Listado de facturas
│   │   ├── form.html          # Crear factura
│   │   └── view.html          # Ver / gestionar factura
│   ├── customer/
│   ├── branches/
│   ├── product/
│   ├── users/
│   ├── invoice_taxes/
│   ├── payment_methods/
│   ├── invoice_payments/
│   ├── discount/
│   └── settings/
│
└── static/                    # CSS, JS, imágenes
```

---

## 4. Arquitectura en Capas

El sistema sigue una arquitectura de tres capas claramente separadas:

```
Navegador
    │
    ▼
routes/*.py          ← Recibe HTTP, valida Form params, llama al servicio
    │
    ▼
services/*.py        ← Lógica de negocio, arma las queries SQL
    │
    ▼
database.py          ← Funciones helper que ejecutan el SQL contra MySQL
    │
    ▼
MySQL / MariaDB
```

### database.py — Funciones helper

| Función | Uso |
|---|---|
| `create_connection()` | Abre una conexión MySQL |
| `execute_query(query, params)` | Ejecuta INSERT, retorna el ID generado (`lastrowid`) |
| `execute_update(query, params)` | Ejecuta UPDATE o DELETE |
| `get_one(query, params)` | SELECT que retorna un `dict` o `None` |
| `get_many(query, params)` | SELECT que retorna una `list[dict]` |

Todas las funciones abren y cierran la conexión por llamada (sin pool). El cursor usa `dictionary=True` para que las filas sean dicts con nombres de columna.

---

## 5. Base de Datos

### Tablas principales

#### `facturas`
| Columna | Tipo | Descripción |
|---|---|---|
| cod_factura | INT AUTO_INCREMENT PK | ID de la factura |
| fecha | DATETIME | Fecha y hora de emisión |
| fecha_vencimiento | DATE | Fecha límite de pago |
| cod_cliente | INT FK | Cliente |
| cod_usuario | INT FK | Cajero/usuario que creó |
| cod_empresa | INT FK | Empresa emisora |
| cod_metodo_pago | INT FK | Método de pago |
| cod_pago | INT FK | Estado del pago |
| total | DOUBLE | Total a pagar (base + impuestos − descuentos) |
| subtotal | DOUBLE | Base gravable (después de descuentos) |
| total_descuentos | DOUBLE | Suma total de descuentos aplicados |
| total_impuestos | DOUBLE | Suma total de impuestos |
| tipo_factura | VARCHAR(5) | `FV` Venta · `NC` Nota Crédito · `ND` Nota Débito |
| observaciones | TEXT | Notas adicionales |

#### `detalle_factura`
| Columna | Tipo | Descripción |
|---|---|---|
| cod_destalle | INT AUTO_INCREMENT PK | ID del ítem |
| cod_factura | INT FK | Factura padre |
| cod_producto | INT FK | Producto |
| cantidad | INT | Unidades |
| precio_unitario | DOUBLE | Precio por unidad |
| subtotal | DOUBLE | Base gravable de esta línea |
| descuento_porcentaje | DOUBLE | % de descuento aplicado |
| descuento_valor | DOUBLE | Valor monetario del descuento |
| impuesto_porcentaje | DOUBLE | % de impuesto (ej: 19 para IVA 19%) |
| impuesto_valor | DOUBLE | Valor monetario del impuesto |

#### `customers`
| Columna | Descripción |
|---|---|
| customer_id | PK |
| full_name | Nombre completo |
| document_type | Tipo documento: C, E, J, G |
| document_number | Número de documento |
| phone, email, address, ciudad, departamento, pais | Datos de contacto |
| tipo_persona | `NATURAL` o `JURIDICA` |
| regimen_tributario | `NO_RESPONSABLE_IVA`, `RESPONSABLE_IVA`, `GRAN_CONTRIBUYENTE`, etc. |

#### `empresas` (emisoras)
| Columna | Descripción |
|---|---|
| cod_empresa | PK |
| nombre | Razón social |
| nit | NIT sin dígito de verificación |
| dv | Dígito de verificación del NIT |
| tipo_documento | `NIT`, `CC`, `CE`, `PASAPORTE` |
| direccion, ciudad, telefono, correo | Datos de contacto |
| regimen_tributario | Régimen fiscal de la empresa |
| actividad_economica | Código CIIU |

#### `productos`
| Columna | Descripción |
|---|---|
| cod_producto | PK |
| sku | Código único del producto |
| nombre | Nombre del producto/servicio |
| precio_unitario | Precio base |
| cod_impuesto | FK a `impuestos` (define el IVA del producto) |
| tipo_item | `IP` (bien/producto) o `IS` (servicio) |
| stock, stock_minimo | Control de inventario |
| activo | 1 = activo, 0 = inactivo |

#### `impuestos`
| Columna | Descripción |
|---|---|
| cod_impuesto | PK |
| descripcion | Nombre del impuesto |
| porcentaje | Tasa (ej: 19.00 para IVA 19%) |
| codigo_dian | Código oficial DIAN: `01`=IVA, `02`=IC, `03`=ICA, `05`=ReteFuente, `06`=ReteICA, `07`=ReteIVA, `08`=ReteCREE, `ZY`=Exento |

#### `metodos_pago`
Describe la forma de pago: Efectivo, Transferencia, Tarjeta, etc.

#### `pagos_factura`
Define los estados posibles de una factura: `paid`, `pending`, `partially paid`, `overdue`, `cancelled`, `refunded`, `disputed`.

---

## 6. Módulos del Sistema

### Dashboard (`/`)
Muestra KPIs en tiempo real calculados desde la base de datos:
- Total de facturas emitidas (FV)
- Ingresos cobrados (facturas en estado `paid`)
- Total de clientes registrados
- Productos activos
- Monto en facturas pendientes
- Productos bajo stock mínimo
- Tabla de las 8 facturas más recientes con acceso rápido

### Facturas (`/invoice`)
Módulo central del sistema. Soporta creación, visualización, cambio de estado y eliminación.

### Clientes (`/customer`)
CRUD completo. Almacena datos fiscales del receptor: tipo persona, régimen tributario, tipo y número de documento.

### Empresas (`/branches`)
CRUD completo para las empresas emisoras. Cada factura lleva el NIT con dígito de verificación, régimen y actividad económica CIIU.

### Productos (`/products`)
CRUD completo. Cada producto tiene asociado un impuesto (IVA) que se aplica automáticamente al facturar.

### Impuestos (`/invoice_taxes`)
Catálogo de impuestos con código DIAN. Un impuesto se asigna a cada producto y se aplica por línea en la factura.

### Métodos de Pago (`/payment_methods`)
Catálogo de formas de pago (Efectivo, Transferencia, PSE, etc.).

### Estados de Pago (`/invoice_payments`)
Catálogo de estados del ciclo de vida de una factura.

### Usuarios (`/users`)
CRUD de los usuarios del sistema (cajeros, administradores).

### Descuentos (`/discount`)
Catálogo de descuentos que pueden asociarse a productos.

---

## 7. Flujo de Trabajo Completo

### Paso 1 — Configuración inicial (datos maestros)

Antes de poder emitir facturas, se deben configurar los datos maestros en este orden recomendado:

```
1. Impuestos         → /invoice_taxes/new
   Crear los impuestos: IVA 19%, IVA 5%, Exento, etc.
   Asignar el código DIAN correspondiente.

2. Empresa emisora   → /branches/new
   Registrar la empresa con NIT, DV, régimen tributario y actividad económica.

3. Métodos de pago   → /payment_methods/new
   Ej: Efectivo, Transferencia bancaria, Tarjeta crédito.

4. Estados de pago   → /invoice_payments/new
   Ej: Pendiente, Pagado, Vencido.

5. Productos         → /products/new
   Registrar cada producto/servicio con su precio, SKU y el impuesto que aplica.

6. Clientes          → /customer/new
   Registrar clientes con tipo de persona y régimen tributario.
```

### Paso 2 — Crear una factura

1. Ir a **Facturas → Nueva Factura** (`/invoice/new`)
2. Completar el formulario:

   **Datos generales:**
   - Tipo de documento: FV (Factura Venta), NC (Nota Crédito), ND (Nota Débito)
   - Cliente
   - Empresa emisora
   - Fecha de emisión (se llena automáticamente con la hora actual)
   - Fecha de vencimiento (opcional)
   - Método de pago
   - Estado de pago inicial
   - Observaciones (opcional)

   **Productos:**
   - Seleccionar un producto del desplegable → el precio y el IVA se cargan automáticamente
   - Ajustar cantidad
   - Aplicar descuento % si aplica
   - Los campos "Base Gravable" e "IVA" se calculan en tiempo real con JavaScript
   - Usar "Agregar Producto" para añadir más líneas

   **Panel resumen (DIAN):**
   - Se actualiza en tiempo real mientras se editan los productos
   - Muestra: Subtotal bruto → Descuentos → Base gravable → Impuestos → **TOTAL**

3. Hacer clic en **Guardar Factura**

### Paso 3 — Procesamiento del servidor (POST /invoice/new)

Cuando el formulario se envía, el servidor:

1. Recibe los arrays de productos, cantidades, precios y descuentos
2. **Por cada línea de producto**, consulta la base de datos para obtener el porcentaje de impuesto vinculado al producto:
   ```sql
   SELECT p.precio_unitario, i.porcentaje AS tax_pct
   FROM productos p
   LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto
   WHERE p.cod_producto = ?
   ```
3. Calcula:
   - `valor_bruto = precio × cantidad`
   - `descuento_valor = valor_bruto × (desc% / 100)`
   - `base_imponible = valor_bruto − descuento_valor`
   - `impuesto_valor = base_imponible × (tax% / 100)`
4. Acumula los totales globales
5. Inserta la cabecera en `facturas`
6. Inserta cada línea en `detalle_factura`
7. Redirige a la vista de la factura creada: `/invoice/{id}`

### Paso 4 — Ver la factura

La vista de factura (`/invoice/{id}`) muestra:
- Encabezado con datos de la empresa emisora
- Tipo de documento (Factura Venta / Nota Crédito / Nota Débito) y número
- Fecha de emisión y vencimiento
- Datos completos del cliente con régimen tributario
- Tabla de líneas con: precio unitario, cantidad, descuento %, base gravable, IVA, total línea
- Desglose DIAN: subtotal bruto → descuentos → base gravable → impuestos → **TOTAL**
- Observaciones
- Panel lateral para cambiar el estado de pago
- Botón para descargar el PDF

### Paso 5 — Gestionar el estado de pago

Desde la vista de la factura, el panel lateral permite cambiar el estado en cualquier momento:
- Pendiente → Pagado
- Pendiente → Vencido
- Pagado → Reembolsado
- etc.

El cambio se hace mediante `POST /invoice/{id}/status` y solo actualiza el campo `cod_pago` en la tabla `facturas`.

### Paso 6 — Generar y descargar el PDF

El botón **Descargar PDF** invoca `GET /invoice/{id}/pdf`, que:
1. Recupera la factura completa con JOIN a todas las tablas
2. Recupera el detalle de líneas
3. Genera el PDF en memoria con ReportLab (sin escribir en disco)
4. Retorna el PDF como `Response` con `Content-Type: application/pdf`
5. El navegador lo abre en una pestaña nueva con el nombre `factura_{id}.pdf`

---

## 8. Cálculo de Impuestos y Totales

### En el navegador (JavaScript — tiempo real)

Al seleccionar un producto o cambiar cantidad/descuento, el JS calcula y muestra:

```javascript
bruto      = precio × cantidad
descuento  = bruto × (desc% / 100)
base       = bruto − descuento
iva        = base × (tax% / 100)   // tax% viene del data-tax del <option>
```

El panel resumen suma todas las filas:
```javascript
subtotal_bruto = Σ bruto
total_desc     = Σ descuento
base_total     = subtotal_bruto − total_desc
total_impuestos = Σ iva
total          = base_total + total_impuestos
```

### En el servidor (Python — persistencia)

El servidor **recalcula los impuestos desde la base de datos** (no confía en los valores del formulario) para cada línea, usando el porcentaje del impuesto vinculado al producto en la tabla `impuestos`. Esto garantiza consistencia aunque el usuario manipule el HTML.

### Fórmula resumida

```
Total factura = (Σ precio_unit × cant) − (Σ descuentos_valor) + (Σ impuestos_valor)
             = base_gravable_total + total_impuestos
```

---

## 9. Generación de PDF

El PDF se genera con **ReportLab** en `services/pdf_service.py`. El documento incluye:

**Encabezado:**
- Nombre de la empresa emisora
- Tipo de documento (FACTURA ELECTRÓNICA DE VENTA / NOTA CRÉDITO / NOTA DÉBITO)
- NIT con dígito de verificación (formato `NIT: 900123456-1`)
- Dirección, ciudad, teléfono, correo
- Régimen tributario de la empresa
- Fecha de emisión y fecha de vencimiento
- Número de factura

**Sección "Facturado a":**
- Nombre del cliente
- Tipo y número de documento
- Régimen tributario del cliente
- Correo y dirección
- Método de pago y estado

**Tabla de productos (7 columnas):**
Producto / Servicio | SKU | Cant. | P. Unit. | Desc % | Base Grav. | IVA

**Totales DIAN:**
- Subtotal bruto
- (−) Descuentos
- Base gravable
- (+) Impuestos
- **Total a Pagar** (resaltado)

**Observaciones** (si existen)

**Pie de página:**
> Documento generado electrónicamente por Factugest · Este documento es válido como soporte de pago.

---

## 10. Referencia de Endpoints

### Facturas

| Método | URL | Nombre | Descripción |
|---|---|---|---|
| GET | `/invoice` | `invoice` | Listado de facturas |
| GET | `/invoice/new` | `new_invoice` | Formulario crear factura |
| POST | `/invoice/new` | `create_invoice` | Guardar nueva factura |
| GET | `/invoice/{id}` | `view_invoice` | Ver detalle de factura |
| POST | `/invoice/{id}/status` | `update_invoice_status` | Cambiar estado de pago |
| GET | `/invoice/{id}/pdf` | `invoice_pdf` | Descargar PDF |
| GET | `/invoice/delete/{id}` | `delete_invoice` | Eliminar factura |

### Clientes

| Método | URL | Nombre |
|---|---|---|
| GET | `/customer` | `customer` |
| GET | `/customer/new` | `new_customer` |
| POST | `/customer/new` | `create_customer` |
| GET | `/customer/edit/{id}` | `edit_customer` |
| POST | `/customer/edit/{id}` | `update_customer` |
| GET | `/customer/delete/{id}` | `delete_customer` |

### Empresas

| Método | URL | Nombre |
|---|---|---|
| GET | `/branches` | `branches` |
| GET | `/branches/new` | `new_branch` |
| POST | `/branches/new` | `create_branch` |
| GET | `/branches/edit/{id}` | `edit_branch` |
| POST | `/branches/edit/{id}` | `update_branch` |
| GET | `/branches/delete/{id}` | `delete_branch` |

### Productos

| Método | URL | Nombre |
|---|---|---|
| GET | `/products` | `products` |
| GET | `/products/new` | `new_product` |
| POST | `/products/new` | `create_product` |
| GET | `/products/edit/{id}` | `edit_product` |
| POST | `/products/edit/{id}` | `update_product` |
| GET | `/products/delete/{id}` | `delete_product` |

> Los demás módulos (usuarios, impuestos, métodos de pago, estados de pago, descuentos) siguen el mismo patrón: `GET /`, `GET /new`, `POST /new`, `GET /edit/{id}`, `POST /edit/{id}`, `GET /delete/{id}`.

---

## 11. Cumplimiento DIAN

Los siguientes campos fueron agregados o reforzados para alinearse con los requisitos de facturación electrónica de la DIAN (Decreto 358/2020 y Resolución 000042/2020):

### Tipos de documento fiscal (`tipo_factura`)
| Código | Descripción |
|---|---|
| `FV` | Factura de Venta |
| `NC` | Nota Crédito Electrónica |
| `ND` | Nota Débito Electrónica |

### Codificación de impuestos (`codigo_dian` en tabla `impuestos`)
| Código | Impuesto |
|---|---|
| `01` | IVA |
| `02` | Impoconsumo (IC) |
| `03` | ICA |
| `05` | Retención en la Fuente |
| `06` | ReteICA |
| `07` | ReteIVA |
| `08` | ReteCREE |
| `ZY` | Exento |

### Emisor (tabla `empresas`)
- `nit` + `dv` — NIT con dígito de verificación (ej: `900123456-1`)
- `regimen_tributario` — Régimen del emisor
- `actividad_economica` — Código CIIU
- `tipo_documento` — Tipo de identificación

### Receptor (tabla `customers`)
- `tipo_persona` — `NATURAL` o `JURIDICA`
- `regimen_tributario` — Régimen del receptor

### Líneas de factura (tabla `detalle_factura`)
- `descuento_porcentaje` / `descuento_valor` — Descuento por ítem
- `impuesto_porcentaje` / `impuesto_valor` — Impuesto por ítem

### Totales en cabecera (tabla `facturas`)
- `subtotal` — Base gravable total
- `total_descuentos` — Suma de todos los descuentos
- `total_impuestos` — Suma de todos los impuestos
- `fecha_vencimiento` — Fecha límite de pago
- `observaciones` — Campo libre

---

## 12. Cambios Realizados vs Versión Anterior

La versión anterior del sistema (migrada de Flask) era de **solo lectura**: únicamente podía listar registros existentes en la base de datos. No tenía formularios funcionales ni lógica de creación/edición.

### Cambios en la base de datos

Se ejecutaron los siguientes `ALTER TABLE` para agregar los campos necesarios:

```sql
-- Detalle de factura
ALTER TABLE detalle_factura MODIFY cod_destalle INT NOT NULL AUTO_INCREMENT;
ALTER TABLE detalle_factura ADD COLUMN descuento_porcentaje DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE detalle_factura ADD COLUMN descuento_valor      DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE detalle_factura ADD COLUMN impuesto_porcentaje  DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE detalle_factura ADD COLUMN impuesto_valor       DOUBLE NOT NULL DEFAULT 0;

-- Cabecera de factura
ALTER TABLE facturas ADD COLUMN subtotal         DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN total_descuentos DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN total_impuestos  DOUBLE NOT NULL DEFAULT 0;
ALTER TABLE facturas ADD COLUMN tipo_factura     VARCHAR(5) NOT NULL DEFAULT 'FV';
ALTER TABLE facturas ADD COLUMN observaciones    TEXT DEFAULT NULL;
ALTER TABLE facturas ADD COLUMN fecha_vencimiento DATE DEFAULT NULL;

-- Empresas emisoras
ALTER TABLE empresas ADD COLUMN dv                   CHAR(1) DEFAULT NULL;
ALTER TABLE empresas ADD COLUMN regimen_tributario   VARCHAR(60) DEFAULT 'RESPONSABLE_IVA';
ALTER TABLE empresas ADD COLUMN actividad_economica  VARCHAR(10) DEFAULT NULL;
ALTER TABLE empresas ADD COLUMN tipo_documento       VARCHAR(20) DEFAULT 'NIT';

-- Clientes
ALTER TABLE customers ADD COLUMN tipo_persona        VARCHAR(20) DEFAULT 'NATURAL';
ALTER TABLE customers ADD COLUMN regimen_tributario  VARCHAR(60) DEFAULT 'NO_RESPONSABLE_IVA';

-- Impuestos
ALTER TABLE impuestos ADD COLUMN codigo_dian VARCHAR(5) DEFAULT NULL;

-- Productos
ALTER TABLE productos ADD COLUMN tipo_item VARCHAR(5) DEFAULT 'IP';
```

### Cambios en el código

**`database.py`** — Se agregaron 4 funciones helper (`execute_query`, `execute_update`, `get_one`, `get_many`) para estandarizar el acceso a datos. Antes no existían y cada servicio manejaba sus propias conexiones de forma inconsistente.

**`services/`** — Todos los servicios fueron reescritos o ampliados:
- `invoice_service.py` — Queries con JOINs completos, funciones de cálculo, `get_dashboard_stats()`
- `customer_service.py` — CRUD completo + campos DIAN
- `branches.py` — CRUD completo + NIT-DV, régimen, CIIU
- `products_service.py` — CRUD completo (antes solo lectura)
- `taxes.py` — CRUD completo + `codigo_dian`
- `payment_methods_service.py` — CRUD completo
- `invoice_payments_service.py` — CRUD completo
- `user_service.py` — CRUD completo
- `discounts.py` — CRUD completo
- `pdf_service.py` — **Nuevo.** Generación de PDF profesional con ReportLab

**`routes/`** — Todos los routers recibieron los endpoints POST/edit/delete que faltaban. `invoice.py` incorporó la lógica de cálculo automático de impuestos por línea.

**`templates/`** — Todos los formularios fueron reescritos desde cero en Jinja2 válido (la versión anterior tenía templates con sintaxis de Thymeleaf/Spring Boot que no funcionaban). Se crearon las vistas de detalle de factura y se modernizó el dashboard.

**`main.py`** — Se conectó `get_dashboard_stats()` al index para mostrar KPIs reales.

**`requirements.txt`** — Se agregó `reportlab==4.2.5`.

---

## 13. Cómo Ejecutar el Proyecto

### Requisitos previos
- Python 3.10+
- MySQL / MariaDB con la base de datos `factugest` ya creada y con los `ALTER TABLE` del punto 12 aplicados

### Instalación

```bash
# 1. Crear entorno virtual
python -m venv .venv

# 2. Activar entorno virtual
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt
```

### Configurar la conexión a la base de datos

Editar `database.py` con los datos de conexión:

```python
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="tu_usuario",
        password="tu_contraseña",
        database="factugest"
    )
```

### Ejecutar el servidor

```bash
# Desde el directorio Factugest/
python main.py

# O directamente con uvicorn:
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

### Acceder al sistema

Abrir el navegador en: `http://127.0.0.1:8000`

La documentación automática de la API (Swagger UI) está disponible en: `http://127.0.0.1:8000/docs`

---

*Generado para Factugest v2.0 — Sistema de Facturación Electrónica Colombia*
