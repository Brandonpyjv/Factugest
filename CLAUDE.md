# Factugest (Backend)

Sistema de facturación electrónica para Colombia. **Monolito FastAPI** que sirve:

1. Una **app web** con templates Jinja2 (frontend actual, en producción).
2. Una **API JSON** bajo `/api/v1/...` consumida por el **cliente móvil Flutter**.

Ambos frontends conviven apuntando al mismo backend y la misma BD.

---

## Repos relacionados

- **Mobile (Flutter)**: `github.com/Brandonpyjv/Factugest-Mobile`
  - Consume `/api/v1/...` de este backend.
  - Genera sus modelos Dart desde `http://<host>:8000/openapi.json`.

> ⚠️ **Cualquier cambio que rompa el contrato de `/api/v1/...` rompe la app móvil.** Si necesitas hacer breaking changes, saca `/api/v2/...` y deja la v1 funcionando hasta que mobile migre.

---

## Stack

- **FastAPI** (rutas web + API JSON)
- **Jinja2** (templates HTML — frontend web)
- **MySQL** vía `mysql-connector-python` directo (sin ORM)
- **Bootstrap 5.3.2** (frontend web)
- **ReportLab** (generación de PDF de facturas)
- **bcrypt** (hash de contraseñas)
- **starlette SessionMiddleware** (auth de la web Jinja, basada en cookies)
- **JWT** (auth de la API `/api/v1/` consumida por mobile)

---

## Estructura

```
Factugest/
├── main.py                  # app FastAPI, middlewares, registro de routers
├── auth.py                  # AuthMiddleware, hash_password, roles
├── database.py              # helpers: execute_query, execute_update, get_one, get_many
├── templates_config.py      # Jinja2 setup
├── routes/                  # APIRouter por dominio (web Jinja)
│   ├── dashboard.py         # ruta "/" — tablero de control (y variante CAJERO)
│   ├── reports.py           # /reports — 8 reportes + export CSV/PDF
│   ├── inventory.py         # /inventory — panel, kardex, movimientos
│   ├── perfil.py            # /perfil/foto — foto de perfil (fuera de /users a propósito)
│   ├── invoice.py           # incluye también algunos /api/... AJAX legacy
│   ├── customer.py
│   ├── productos.py
│   ├── users.py
│   ├── branches.py
│   ├── discounts.py
│   ├── taxes.py
│   ├── payment_methods.py
│   ├── invoice_payments.py
│   ├── product_discount.py
│   ├── logs.py
│   ├── ubicacion.py
│   ├── login.py
│   └── api/v1/              # ← NUEVO: endpoints JSON para mobile (en construcción)
├── services/                # lógica de negocio reutilizable por web y API
│   ├── calculo_documento.py # aritmética tributaria (pura): bases, descuentos, prorrateo
│   ├── numeracion_service.py# reserva atómica de consecutivos por emisor
│   ├── documento_canonico.py# contrato de entrada de pdf_service y xml_service
│   ├── invoice_service.py   # CRUD facturas + get_dashboard_stats
│   ├── inventory_service.py # kardex, alertas, valorización (único punto de escritura de stock)
│   ├── report_service.py    # métricas del tablero: ventas, cartera, rankings, impuestos
│   ├── export_service.py    # reportes → CSV y PDF
│   ├── avatar_service.py    # valida y normaliza las fotos de perfil
│   ├── pdf_service.py       # generate_invoice_pdf → bytes
│   ├── xml_service.py       # generate_invoice_xml → str (DIAN)
│   ├── cufe_service.py      # generate_cufe
│   ├── customer_service.py
│   ├── products_service.py
│   ├── user_service.py
│   ├── branches.py
│   ├── discounts.py
│   ├── taxes.py
│   ├── payment_methods_service.py
│   ├── invoice_payments_service.py
│   ├── product_discount_service.py
│   ├── logs_service.py
│   └── ubicacion_service.py
├── templates/               # Jinja2: layout.html + carpeta por dominio
└── static/                  # CSS, JS, imágenes
```

**Patrón clave**: `routes/` son thin wrappers; toda la lógica vive en `services/`. Esto permite que el mismo `service` alimente la ruta HTML y la ruta JSON sin duplicar código.

---

## Helpers de base de datos (`database.py`)

```python
execute_query(q, params)   # INSERT → retorna last_insert_id
execute_update(q, params)  # UPDATE/DELETE
get_one(q, params)         # SELECT un registro → dict | None
get_many(q, params)        # SELECT múltiples → list[dict]
```

**No usar ORM.** El proyecto está diseñado intencionalmente con SQL directo y queries explícitas.

---

## Autenticación

### Web (Jinja) — sesiones
- `SessionMiddleware` + cookies.
- `AuthMiddleware` en `auth.py` protege todas las rutas excepto `/login` y `/static`.
- Bloqueos por rol vía `_ADMIN_ONLY_PREFIXES` y `_CAJERO_BLOCKED_PREFIXES`.

### API (`/api/v1/`) — JWT
- `POST /api/v1/auth/login` → `{access_token, token_type, user}`.
- Dependency `get_current_user()` valida el `Authorization: Bearer <token>`.
- El payload del JWT debe incluir `cod_usuario`, `rol`, `cod_empresa` para los gates por rol.
- CORS habilitado para el cliente Flutter.

### Roles (compartidos entre web y API)
```python
ROLE_HIERARCHY = {
    "ADMIN":       4,
    "JEFE_TIENDA": 3,
    "SUPERVISOR":  2,
    "CAJERO":      1,
}
ADMIN_ROLES = {"ADMIN", "SUPERVISOR", "JEFE_TIENDA"}  # acceso completo
# CAJERO → solo facturación
```

---

## Base de datos

- **Local**: `localhost`, user `root` sin contraseña, db `factugest`.
- Configurable vía `.env` (variables que lee `database.py`).
- **Migraciones**: `python migrate.py` aplica los cambios de esquema versionados y
  registra lo aplicado en `schema_migrations`. Cada migración es idempotente.
  Al agregar columnas o tablas, añade una migración ahí y regenera `base/factugest.sql`.

> ⚠️ **`base/factugest.sql` es un baseline liviano**, no un respaldo: trae los catálogos
> completos (municipios, departamentos, impuestos, estados y métodos de pago) pero solo
> un puñado de facturas, clientes y productos de ejemplo. **No lo reemplaces con un
> export completo de tu base local**: le meterías los cientos de documentos que generó
> `seed_demo.py` y borrarías filas de catálogo que tú no tengas. Cuando agregues tablas,
> empalma solo los bloques nuevos de estructura.

### Dos zonas de datos

La base tiene dos zonas que no se mezclan:

| Zona | Tablas | Qué guarda |
|---|---|---|
| **Comercial** | `facturas`, `detalle_factura`, `customers`, `productos` | Nuestras propias ventas: los planes de facturación que vendemos. |
| **Middleware** | `clientes_api`, `receptores`, `documentos`, `documento_lineas`, `documento_eventos` | Lo que emitimos por cuenta de terceros a través de `/api/v1/`. |
| **Compartida** | `empresas`, `municipios`, `impuestos` | Emisores y catálogos. Una fila de `empresas` es un emisor, sea nuestro o de un cliente. |

**Nunca guardes en `facturas` un documento emitido para un tercero**: el tablero y los
ocho reportes leen esa tabla, así que aparecería como ingreso nuestro. `documentos` es su
lugar, y `clientes_api` es el puente entre una fila de `customers` (a quién le facturamos
el plan) y una de `empresas` (con qué NIT y resolución emite).

El consumo por cliente y por mes **se cuenta de `documentos`**; no hay tabla de
contadores, justamente para que no pueda desviarse de la realidad.

### Invariante de numeración

Los consecutivos se reservan con `services/numeracion_service.reservar_numero()`, que lo
hace en una sola sentencia `UPDATE`. Nunca leas `consecutivo_actual` y lo actualices por
separado: con dos peticiones simultáneas ambas leen el mismo valor, y dos documentos con
el mismo número de la resolución son dos rechazos de la DIAN. La tabla `documentos` tiene
además un índice único por `(cod_empresa, tipo, numero)` como red de seguridad.

### Invariante de emisión atómica

Emitir es una sola operación: reservar el número, guardar la cabecera, guardar el detalle
y mover el inventario van dentro de un `database.transaction()`, de modo que un fallo a
mitad no deja rastro y el consecutivo queda libre. Los servicios de escritura
(`invoice_service`, `inventory_service`, `numeracion_service`) aceptan `cursor=` para
participar de la transacción de quien emite.

### Invariante de cálculo

La aritmética tributaria vive en `services/calculo_documento.py` y en ningún otro lugar.
No recalcules bases, descuentos ni prorrateo de IVA dentro de una ruta: es la única
implementación que alimenta tanto el formulario web como la API, y está cubierta por
pruebas. El contrato de entrada de `pdf_service` y `xml_service` está en
`services/documento_canonico.py`.

### Invariante de inventario

Toda modificación de `productos.stock` pasa por `services/inventory_service.py`.
Nunca un `UPDATE productos SET stock = ...` suelto: cada cambio deja su fila en
`movimientos_inventario` (kardex), de modo que el saldo siempre es reconstruible.
Los productos con `controla_stock = 0` (servicios, intangibles) se ignoran sin error.

---

## Cómo correr

```bash
# Desde Factugest/Factugest/
python main.py
# o
uvicorn main:app --reload
```

Servidor en `http://127.0.0.1:8000`. Swagger en `/docs`.

### Pruebas

```bash
pip install -r requirements-dev.txt   # pytest no está en requirements.txt
python -m pytest                      # desde Factugest/Factugest/
```

Las pruebas cubren lo que no necesita base de datos: la aritmética tributaria, el
contrato del documento canónico y los puntos del XML donde el emisor cambia la salida.

---

## Convenciones

- **Rutas web (Jinja)**: `routes/<dominio>.py` con `APIRouter(prefix="/<dominio>")`. Retornan `TemplateResponse`.
- **Rutas API JSON**: `routes/api/v1/<dominio>.py` con `APIRouter(prefix="/api/v1/<dominio>")`. Retornan `JSONResponse` o un Pydantic model.
- **Templates** heredan de `layout.html`: `{% extends "layout.html" %}`.
- **Links en HTML**: usar `url_for('nombre_ruta')`, nunca hardcodear paths.
- **Validación de inputs**:
  - Web: `Form(...)` de FastAPI.
  - API: Pydantic `BaseModel` (obligatorio — habilita validación automática y docs en Swagger).
- **Sin comentarios obvios**. Solo *por qué*, no *qué*.

---

## CRUD implementado

CRUD completo para: Facturas, Clientes, Usuarios, Productos, Empresas (sucursales), Descuentos, Impuestos, Métodos de Pago, Estados de Pago.

**Funcionalidades especiales:**
- Generación de **PDF** (`services/pdf_service.py`) y **XML DIAN** (`services/xml_service.py`).
- **CUFE** (`services/cufe_service.py`) — actualmente simulado, no enviado a DIAN real.
- **Notas Crédito** y **Notas Débito** con referencia a la factura origen.
- **Prorrateo de IVA** sobre descuentos de factura.
- Consecutivos de factura/NC/ND por empresa.
- **Control de inventario**: facturar descuenta stock, la NC lo reingresa, kardex
  completo con alertas por bajo mínimo y valorización.
- **Tablero de control** con filtros de periodo y empresa, gráficas Chart.js y
  comparativa contra el periodo anterior. Vista reducida para CAJERO.
- **Reportes exportables** a CSV y PDF (`/reports`).

### Datos de demostración

`python seed_demo.py` genera seis meses de operación (ventas, notas crédito y
débito, compras, mermas, cartera en todos los tramos) para poder mostrar el
tablero y los reportes con contenido. `python seed_demo.py --limpiar` lo deshace
exactamente. Es determinista y se verifica a sí mismo. **No usar en producción.**

### Alcance por rol

- `ADMIN` / `JEFE_TIENDA` / `SUPERVISOR` → tablero completo, inventario y reportes,
  limitados a su propia empresa. Solo `ADMIN` puede consolidar todas las empresas.
- `CAJERO` → panel operativo (facturar, clientes, consultar productos). Sin cifras
  financieras. `/inventory` y `/reports` están en `_ADMIN_ONLY_PREFIXES`.

**Fotos de perfil**: `puede_cambiar_foto` permite a cada quien la suya y a un
superior las de sus inferiores. La excepción del propio usuario no es un descuido:
`can_manage` exige un rol estrictamente mayor y sin ella ningún ADMIN podría tener
foto. Por eso las rutas viven en `/perfil` y no bajo `/users`, que es solo para
roles administrativos.

---

## Cosas a tener en cuenta al modificar el backend

### ⚠️ Si tocas algo bajo `/api/v1/...`
1. ¿Es breaking? Si cambias forma de respuesta, nombres de campos, requeridos → **rompe Flutter**.
2. Para breaking changes: crear `/api/v2/<endpoint>` y mantener v1 hasta que mobile migre.
3. Después del cambio, actualizar el cliente mobile (regenerar modelos Dart desde `/openapi.json`).

### ⚠️ Si tocas algo en `services/`
- Probablemente afecta **ambos frontends** (web y mobile). Verificar los dos flujos.

### ⚠️ Si tocas la BD
- Agregar una migración en `migrate.py` en lugar de un ALTER suelto, y regenerar
  `base/factugest.sql`.
- Verificar que ambos frontends sigan funcionando.

### ⚠️ Si tocas el stock
- Usar `inventory_service`, nunca un UPDATE directo (ver el invariante de inventario).
- Una factura que falla por falta de stock **no debe consumir un consecutivo**: la
  numeración de la resolución DIAN es un recurso autorizado y finito.

---

## Decisión arquitectónica clave

El backend nació como monolito FastAPI con frontend Jinja. Cuando se necesitó soporte móvil, se evaluó:

1. Reescribir todo en Flutter → descartado (perdíamos toda la lógica probada).
2. **Agregar API JSON paralela** + cliente Flutter en repo separado → **elegido**.
3. Migrar el frontend web a SPA → fuera de alcance.

**Resultado**: el backend tiene dos "caras" — Jinja (web actual) y JSON (mobile nuevo) — alimentadas por la misma capa de `services/`. La web sigue intacta; la API es aditiva.

---

## Objetivos específicos del anteproyecto

| Objetivo | Estado |
|---|---|
| 1 — Emisión de FV/NC/ND con PDF, XML UBL 2.1 y CUFE | ✅ (CUFE en pre-producción) |
| 2 — Control de inventarios con alertas y kardex | ✅ |
| 3 — Tablero de control con métricas y reportes exportables | ✅ |
| API REST de integración (`/api/v1/`) | ⏳ fuera del alcance actual |

---

## TODOs / Pendientes conocidos

- [ ] Construir endpoints `/api/v1/` para todos los dominios (en progreso).
- [ ] Implementar JWT auth en `/api/v1/auth/login`.
- [ ] Habilitar CORS para el origen de Flutter.
- [ ] DIAN real: el CUFE actual es de pruebas.
- [ ] Migrar contraseñas legacy (ya hay un `migrate_passwords` en `main.py` que hashea al arrancar).
