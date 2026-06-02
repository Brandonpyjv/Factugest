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
│   ├── invoice_service.py   # CRUD facturas + get_dashboard_stats
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
- **No hay migraciones formales** — el esquema se mantiene manualmente. Cuando agregues columnas, documenta el ALTER en el PR.

---

## Cómo correr

```bash
# Desde Factugest/Factugest/
python main.py
# o
uvicorn main:app --reload
```

Servidor en `http://127.0.0.1:8000`. Swagger en `/docs`.

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
- **Dashboard** con KPIs en tiempo real (`services/invoice_service.py::get_dashboard_stats`).
- **Prorrateo de IVA** sobre descuentos de factura.
- Consecutivos de factura/NC/ND por empresa.

---

## Cosas a tener en cuenta al modificar el backend

### ⚠️ Si tocas algo bajo `/api/v1/...`
1. ¿Es breaking? Si cambias forma de respuesta, nombres de campos, requeridos → **rompe Flutter**.
2. Para breaking changes: crear `/api/v2/<endpoint>` y mantener v1 hasta que mobile migre.
3. Después del cambio, actualizar el cliente mobile (regenerar modelos Dart desde `/openapi.json`).

### ⚠️ Si tocas algo en `services/`
- Probablemente afecta **ambos frontends** (web y mobile). Verificar los dos flujos.

### ⚠️ Si tocas la BD
- Documentar el `ALTER TABLE` en el PR.
- Verificar que ambos frontends sigan funcionando.

---

## Decisión arquitectónica clave

El backend nació como monolito FastAPI con frontend Jinja. Cuando se necesitó soporte móvil, se evaluó:

1. Reescribir todo en Flutter → descartado (perdíamos toda la lógica probada).
2. **Agregar API JSON paralela** + cliente Flutter en repo separado → **elegido**.
3. Migrar el frontend web a SPA → fuera de alcance.

**Resultado**: el backend tiene dos "caras" — Jinja (web actual) y JSON (mobile nuevo) — alimentadas por la misma capa de `services/`. La web sigue intacta; la API es aditiva.

---

## TODOs / Pendientes conocidos

- [ ] Construir endpoints `/api/v1/` para todos los dominios (en progreso).
- [ ] Implementar JWT auth en `/api/v1/auth/login`.
- [ ] Habilitar CORS para el origen de Flutter.
- [ ] DIAN real: el CUFE actual es de pruebas.
- [ ] Migrar contraseñas legacy (ya hay un `migrate_passwords` en `main.py` que hashea al arrancar).
