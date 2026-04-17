# Cambios implementados: Java Spring Boot → Python FastAPI

Este documento describe todos los cambios y mejoras que se portaron desde la versión Java Spring Boot al proyecto Python FastAPI de Factugest.

---

## Índice

1. [Contexto](#1-contexto)
2. [Base de datos — columnas nuevas](#2-base-de-datos--columnas-nuevas)
3. [Variables de entorno](#3-variables-de-entorno)
4. [Sistema de autenticación](#4-sistema-de-autenticación)
5. [Migración automática de contraseñas](#5-migración-automática-de-contraseñas)
6. [Servicio de usuarios actualizado](#6-servicio-de-usuarios-actualizado)
7. [Ruta de facturas actualizada](#7-ruta-de-facturas-actualizada)
8. [Endpoints AJAX para el formulario de factura](#8-endpoints-ajax-para-el-formulario-de-factura)
9. [Servicio de productos actualizado](#9-servicio-de-productos-actualizado)
10. [Archivos nuevos creados](#10-archivos-nuevos-creados)
11. [Archivos modificados](#11-archivos-modificados)
12. [Dependencias nuevas](#12-dependencias-nuevas)
13. [Tabla resumen de equivalencias](#13-tabla-resumen-de-equivalencias)

---

## 1. Contexto

El proyecto Factugest fue desarrollado inicialmente en **Python con Flask y MariaDB**, luego migrado a **Java con Spring Boot y PostgreSQL** donde se implementaron mejoras como:

- Spring Security (autenticación, roles, hasheo de contraseñas)
- Nuevas columnas en varias tablas de la base de datos
- Endpoints AJAX para el formulario de facturas
- Uso del usuario logueado en operaciones

Este documento describe cómo esas mejoras fueron llevadas de vuelta al proyecto Python FastAPI para que ambas versiones sean funcionalmente equivalentes.

---

## 2. Base de datos — columnas nuevas

La versión Java extendió el esquema de la base de datos con nuevas columnas que no existían en el MariaDB original de Python. Se ejecutaron los siguientes `ALTER TABLE` para sincronizar ambas versiones:

### Tabla `customers`
```sql
ALTER TABLE customers
  ADD COLUMN IF NOT EXISTS tipo_persona VARCHAR(20) DEFAULT 'NATURAL',
  ADD COLUMN IF NOT EXISTS regimen_tributario VARCHAR(60) DEFAULT 'NO_RESPONSABLE_IVA';
```
**Para qué sirve:** Clasificar al cliente como persona natural o jurídica y su régimen tributario frente a la DIAN.

### Tabla `empresas`
```sql
ALTER TABLE empresas
  ADD COLUMN IF NOT EXISTS dv VARCHAR(5) DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS regimen_tributario VARCHAR(60) DEFAULT 'RESPONSABLE_IVA',
  ADD COLUMN IF NOT EXISTS actividad_economica VARCHAR(10) DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS tipo_documento VARCHAR(20) DEFAULT 'NIT';
```
**Para qué sirve:** Datos requeridos para la facturación electrónica en Colombia (dígito verificador del NIT, código de actividad económica CIIU, etc.).

### Tabla `facturas`
```sql
ALTER TABLE facturas
  ADD COLUMN IF NOT EXISTS fecha_vencimiento DATE DEFAULT NULL,
  ADD COLUMN IF NOT EXISTS subtotal DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS total_descuentos DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS total_impuestos DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS tipo_factura VARCHAR(5) NOT NULL DEFAULT 'FV',
  ADD COLUMN IF NOT EXISTS observaciones TEXT DEFAULT NULL;
```
**Para qué sirve:** Desglose contable correcto de la factura (base gravable, descuentos, impuestos por separado) y soporte para los tres tipos de documento electrónico: `FV` (Factura de Venta), `NC` (Nota Crédito), `ND` (Nota Débito).

### Tabla `detalle_factura`
```sql
ALTER TABLE detalle_factura
  ADD COLUMN IF NOT EXISTS descuento_porcentaje DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS descuento_valor DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS impuesto_porcentaje DOUBLE NOT NULL DEFAULT 0,
  ADD COLUMN IF NOT EXISTS impuesto_valor DOUBLE NOT NULL DEFAULT 0;
```
**Para qué sirve:** Guardar el desglose de descuentos e impuestos por línea de producto, necesario para el PDF de factura y los reportes contables.

### Tabla `impuestos`
```sql
ALTER TABLE impuestos
  ADD COLUMN IF NOT EXISTS codigo_dian VARCHAR(5) DEFAULT NULL;
```
**Para qué sirve:** Código oficial DIAN para cada tipo de impuesto (ej. `01` = IVA, `05` = RETEFUENTE).

### Tabla `productos`
```sql
ALTER TABLE productos
  ADD COLUMN IF NOT EXISTS tipo_item VARCHAR(5) DEFAULT 'IP';
```
**Para qué sirve:** Clasificar el producto según estándar DIAN: `IP` = bien físico, `IS` = servicio.

---

## 3. Variables de entorno

**Problema anterior:** Las credenciales de la base de datos estaban escritas directamente en `database.py`, lo que significaba que si el código se subía a GitHub, cualquiera podía ver el usuario y contraseña.

**Solución implementada:** Se creó un archivo `.env` que nunca se sube a GitHub.

### Archivos involucrados

**`.env`** (no se sube a GitHub — ignorado por `.gitignore`)
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=factugest
SESSION_SECRET=factugest-secret-key-cambiar-en-produccion
```

**`.env.example`** (sí se sube — es la plantilla pública sin datos reales)
```
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=factugest
SESSION_SECRET=cambia-esta-clave-secreta
```

**`.gitignore`** (creado en la raíz del proyecto)
```
.env
.env.*
!.env.example
__pycache__/
venv/
.venv/
...
```

### Cómo quedó `database.py`

**Antes:**
```python
def create_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="factugest")
```

**Después:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

_DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "user":     os.getenv("DB_USER", "root"),
    "passwd":   os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "factugest"),
}

def create_connection():
    return mysql.connector.connect(**_DB_CONFIG)
```

Los valores entre comillas (`"localhost"`, `"root"`, etc.) son valores por defecto que se usan solo si el `.env` no existe — útil para desarrollo local.

---

## 4. Sistema de autenticación

**Problema anterior:** El proyecto Python no tenía ningún control de acceso. Cualquier persona podía acceder a todas las rutas sin iniciar sesión.

**Solución implementada:** Se creó un sistema equivalente a Spring Security con:
- Página de login
- Sesiones en el servidor
- Hasheo de contraseñas con BCrypt
- Control de acceso por rol

Ver el documento `SEGURIDAD.md` para una explicación detallada de cómo funciona.

**Archivos creados:**
- `auth.py` — Funciones de hasheo y middleware de protección
- `routes/login.py` — Rutas `/login` y `/logout`
- `templates/login.html` — Página de inicio de sesión

---

## 5. Migración automática de contraseñas

**Problema anterior:** Las contraseñas en la base de datos estaban en texto plano (`123456789`). Esto es un riesgo de seguridad grave: si alguien accede a la base de datos, ve todas las contraseñas directamente.

**Solución implementada:** Al arrancar el servidor, `main.py` revisa automáticamente todos los usuarios. Si una contraseña no está hasheada (no empieza con `$2b$`), la hashea y guarda el hash en la base de datos.

```python
@app.on_event("startup")
def migrate_passwords():
    from database import get_many, execute_update
    from auth import hash_password
    users = get_many("SELECT cod_usuario, contrasena FROM usuarios")
    for u in users:
        pwd = u.get("contrasena") or ""
        if pwd and not pwd.startswith("$2"):
            hashed = hash_password(pwd)
            execute_update(
                "UPDATE usuarios SET contrasena=%s WHERE cod_usuario=%s",
                (hashed, u["cod_usuario"]),
            )
```

**Es idempotente:** Si ya están hasheadas, no hace nada. Se puede reiniciar el servidor las veces que sea sin problema.

**Antes en la BD:**
```
| Administrator | 123456789 |
```
**Después en la BD:**
```
| Administrator | $2b$12$KYn/TpNM...8XqZuL |
```

---

## 6. Servicio de usuarios actualizado

**Archivo:** `services/user_service.py`

### Cambios realizados

**1. Hasheo al crear usuario**

**Antes:**
```python
def create_user(nombre, correo, contrasena, rol):
    query = "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (nombre, correo, contrasena, rol))
    # ❌ contrasena se guarda en texto plano
```

**Después:**
```python
def create_user(nombre, correo, contrasena, rol):
    hashed = hash_password(contrasena)  # ✅ hashear primero
    query = "INSERT INTO usuarios (nombre, correo, contrasena, rol) VALUES (%s, %s, %s, %s)"
    return execute_query(query, (nombre, correo, hashed, rol))
```

**2. Hasheo al editar usuario**

```python
def update_user(user_id, nombre, correo, rol, contrasena=None):
    if contrasena:
        hashed = hash_password(contrasena)  # ✅ hashear si se cambia
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s, contrasena=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, hashed, user_id))
    else:
        # Si no se envía contraseña, no la toca
        query = "UPDATE usuarios SET nombre=%s, correo=%s, rol=%s WHERE cod_usuario=%s"
        return execute_update(query, (nombre, correo, rol, user_id))
```

**3. Nueva función: buscar por correo**

Necesaria para el proceso de login (Spring Security buscaba por correo, ahora Python también):
```python
def get_user_by_email(correo: str):
    return get_one("SELECT * FROM usuarios WHERE correo = %s", (correo,))
```

---

## 7. Ruta de facturas actualizada

**Archivo:** `routes/invoice.py`

### Cambio: usuario de sesión en vez de hardcodeado

**Antes:**
```python
invoice_id = create_invoice(
    cod_cliente=cod_cliente,
    cod_usuario=1,  # ❌ siempre el usuario 1, sin importar quién está logueado
    ...
)
```

**Después:**
```python
session_user = request.session.get("user", {})
cod_usuario = session_user.get("cod_usuario", 1)

invoice_id = create_invoice(
    cod_cliente=cod_cliente,
    cod_usuario=cod_usuario,  # ✅ el usuario que está logueado
    ...
)
```

**Por qué importa:** En Java, Spring Security inyecta automáticamente el usuario autenticado. En Python, se lee de la sesión. Esto hace que cada factura quede registrada con el usuario correcto, lo cual es esencial para los logs de auditoría.

---

## 8. Endpoints AJAX para el formulario de factura

**Archivo:** `routes/invoice.py`

La versión Java implementó endpoints REST internos para que el formulario de nueva factura pudiera buscar clientes y productos dinámicamente (sin recargar la página). Se portaron los mismos cuatro endpoints:

### `GET /invoice/api/customers/search?q=`
Busca clientes por nombre o número de documento.
```python
@router.get("/api/customers/search")
def api_customers_search(q: str = ""):
    results = get_many(
        "SELECT customer_id, full_name, document_number FROM customers "
        "WHERE full_name LIKE %s OR document_number LIKE %s ORDER BY full_name LIMIT 10",
        (f"%{q}%", f"%{q}%"),
    )
    return JSONResponse(content=results)
```

### `GET /invoice/api/products/search?q=`
Busca productos activos por SKU o nombre, devuelve precio e impuesto.
```python
@router.get("/api/products/search")
def api_products_search(q: str = ""):
    results = get_many(
        "SELECT p.cod_producto, p.sku, p.nombre, p.precio_unitario, "
        "i.porcentaje AS tax_pct "
        "FROM productos p LEFT JOIN impuestos i ON p.cod_impuesto = i.cod_impuesto "
        "WHERE p.activo = 1 AND (p.sku LIKE %s OR p.nombre LIKE %s) "
        "ORDER BY p.nombre LIMIT 10",
        (f"%{q}%", f"%{q}%"),
    )
    return JSONResponse(content=results)
```

### `GET /invoice/api/products/{id}/discounts`
Devuelve los descuentos configurados para un producto específico.

### `GET /invoice/api/discounts`
Devuelve los descuentos que aplican a nivel de factura completa (`aplica_a_factura = 1`).

---

## 9. Servicio de productos actualizado

**Archivo:** `services/products_service.py`

Se agregó `tipo_item` al `SELECT` de `get_all_products_detailed()`, ya que `invoice_service.py` lo referencia en las consultas de detalle de factura y el PDF lo necesita para clasificar bienes vs servicios.

**Antes:**
```sql
SELECT p.cod_producto, p.sku, p.nombre, ..., p.activo,
       i.descripcion AS tax_name, i.porcentaje AS tax_porcentaje
FROM productos p LEFT JOIN impuestos i ON ...
```

**Después:**
```sql
SELECT p.cod_producto, p.sku, p.nombre, ..., p.activo,
       p.tipo_item,   -- ✅ agregado
       i.descripcion AS tax_name, i.porcentaje AS tax_porcentaje
FROM productos p LEFT JOIN impuestos i ON ...
```

---

## 10. Archivos nuevos creados

| Archivo | Descripción |
|---------|-------------|
| `auth.py` | Hasheo BCrypt + middleware de autenticación |
| `routes/login.py` | Rutas GET/POST `/login` y GET `/logout` |
| `templates/login.html` | Página de login (diseño idéntico a la versión Java) |
| `.env` | Credenciales de BD y clave de sesión (NO se sube a GitHub) |
| `.env.example` | Plantilla pública del `.env` (SÍ se sube a GitHub) |
| `../.gitignore` | Excluye `.env`, `__pycache__`, `venv/`, etc. |

---

## 11. Archivos modificados

| Archivo | Qué cambió |
|---------|------------|
| `database.py` | Lee credenciales desde variables de entorno (`.env`) |
| `main.py` | Agrega `SessionMiddleware`, `AuthMiddleware`, startup de migración de contraseñas, router de login |
| `requirements.txt` | Agrega `bcrypt`, `python-dotenv`, `itsdangerous` |
| `services/user_service.py` | Hasheo en create/update, nueva función `get_user_by_email()` |
| `routes/invoice.py` | Usuario de sesión, endpoints AJAX |
| `services/products_service.py` | Incluye `tipo_item` en SELECT |

---

## 12. Dependencias nuevas

Se agregaron al `requirements.txt`:

| Paquete | Versión | Para qué |
|---------|---------|----------|
| `bcrypt` | 4.2.1 | Hasheo de contraseñas (equivalente a `BCryptPasswordEncoder` de Spring Security) |
| `python-dotenv` | 1.0.1 | Leer el archivo `.env` |
| `itsdangerous` | 2.2.0 | Firmar y verificar las cookies de sesión (usado internamente por `SessionMiddleware`) |

> **Nota importante:** Se usa `bcrypt` directamente, **no** `passlib`. La librería `passlib 1.7.4` es incompatible con `bcrypt >= 4.0.0` y lanza errores al arrancar.

Para instalar:
```bash
pip install -r requirements.txt
```

---

## 13. Tabla resumen de equivalencias

| Concepto | Java Spring Boot | Python FastAPI |
|----------|-----------------|----------------|
| Autenticación | `Spring Security` + `SecurityConfig.java` | `SessionMiddleware` + `AuthMiddleware` en `auth.py` |
| Hasheo de contraseña | `BCryptPasswordEncoder` (Spring Bean) | `bcrypt.hashpw()` en `auth.py` |
| Usuario logueado | `@AuthenticationPrincipal CustomUserPrincipal` | `request.session.get("user")` |
| Login form | `LoginController.java` + `login.html` (Thymeleaf) | `routes/login.py` + `templates/login.html` (Jinja2) |
| Restricción ADMIN | `.requestMatchers("/users/**").hasRole("ADMIN")` | `_ADMIN_PREFIXES` en `AuthMiddleware` |
| Migración de contraseñas | `PasswordMigrationRunner.java` (`ApplicationRunner`) | `@app.on_event("startup")` en `main.py` |
| Variables de entorno | `.env` + `application.properties` con `${VAR}` | `.env` + `python-dotenv` en `database.py` |
| Búsqueda AJAX clientes | `GET /api/customers/search` en `InvoiceController.java` | `GET /invoice/api/customers/search` en `routes/invoice.py` |
| Búsqueda AJAX productos | `GET /api/products/search` en `InvoiceController.java` | `GET /invoice/api/products/search` en `routes/invoice.py` |
