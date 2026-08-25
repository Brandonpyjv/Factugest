# Factugest — Sistema de Facturación Electrónica 🇨🇴

Sistema de facturación electrónica para Colombia. Este documento explica cómo levantar el proyecto y los cambios de la migración de **Flask → FastAPI**.

> **¿Buscas cómo funciona el sistema?** Está en la **Guía técnica «Anatomía de FactuGest»**:
> arquitectura, el recorrido de una factura paso a paso, el modelo de datos, por qué se
> eligió cada herramienta y las preguntas de sustentación con su respuesta.
> Reemplaza al antiguo `DOCUMENTACION.md`, que describía el sistema antes del inventario,
> los reportes, las validaciones y la API, y a estas alturas engañaba más de lo que ayudaba.
>
> Para el estado del trabajo y lo que falta, el **Cuaderno de Ruta**.
> Para las reglas que hay que respetar al programar, `CLAUDE.md`.

---

## Índice

1. [Requisitos](#requisitos)
2. [Instalación](#instalación)
3. [Cómo iniciar el proyecto](#cómo-iniciar-el-proyecto)

4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Migración Flask → FastAPI: qué cambió](#migración-flask--fastapi-qué-cambió)
6. [Guía de adaptación para el equipo](#guía-de-adaptación-para-el-equipo)
7. [Por qué FastAPI](#por-qué-fastapi)  

---

## Requisitos

- Python 3.10 o superior — [descargar en python.org](https://www.python.org/downloads/)
- XAMPP (incluye MySQL y phpMyAdmin) — [descargar en apachefriends.org](https://www.apachefriends.org/es/index.html)
- Git — [descargar en git-scm.com](https://git-scm.com/downloads)

---

## Instalación

El orden importa: **importar el SQL → migrar → sembrar**. El archivo `base\factugest.sql`
es un baseline liviano —estructura y catálogos— que se quedó en la migración `003`; las
migraciones de la `004` a la `013` las aplica `migrate.py`, y la operación de demostración
(clientes, documentos, facturas) la genera `seed_proveedor.py`. Saltarse un paso deja la
base a medias y el panel arranca con errores de columnas que no existen.

### Paso 1 — Clonar el repositorio

```powershell
git clone <url-del-repositorio>
cd "Factugest Python\Factugest\Factugest"
```

Todos los comandos de aquí en adelante se corren desde esa carpeta `Factugest\`, la que
contiene `main.py`.

### Paso 2 — Crear la base de datos vacía

1. Abre XAMPP y arranca **Apache** y **MySQL**
2. Entra a **phpMyAdmin** en `http://localhost/phpmyadmin`
3. Pestaña **Bases de datos** → crea una llamada `factugest` con cotejamiento
   `utf8mb4_general_ci`

> El `.sql` no trae `CREATE DATABASE`: espera encontrar la base ya creada y seleccionada.

### Paso 3 — Importar el baseline

1. Selecciona `factugest` en el panel izquierdo
2. Pestaña **Importar** → **Seleccionar archivo** → `base\factugest.sql`
3. **Importar**

Si phpMyAdmin se queja por el tamaño del archivo, desde la consola de XAMPP:

```powershell
C:\xampp\mysql\bin\mysql -u root factugest < "base\factugest.sql"
```

> ⚠️ **Nunca reemplaces `base\factugest.sql` con un export de tu base local.** Le meterías
> los miles de documentos sembrados y borrarías catálogos que tú no tengas. Un cambio de
> esquema se agrega como migración en `migrate.py`; solo entonces se empalma el bloque
> nuevo de estructura en el dump.

### Paso 4 — Crear el entorno virtual e instalar dependencias

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Sabrás que el entorno está activo porque el prompt muestra `(.venv)` al inicio. No instales
los paquetes uno por uno — este comando los instala todos con las versiones probadas.

### Paso 5 — Crear el archivo `.env`

`.env` no está en el repositorio (lleva secretos): cada quien crea el suyo copiando la
plantilla, que sí está y documenta cada variable.

```powershell
copy .env.example .env
```

Lo mínimo para arrancar en local con XAMPP:

| Variable | Valor en local |
|---|---|
| `DB_HOST` / `DB_USER` / `DB_NAME` | `localhost` / `root` / `factugest` |
| `DB_PASSWORD` | vacío (XAMPP trae `root` sin contraseña) |
| `SESSION_SECRET` | cualquier cadena larga, distinta en cada máquina |
| `DIAN_PROVEEDOR` | `simulado` |
| `FACTUGEST_API_KEY` | se llena en el paso 7 |

### Paso 6 — Aplicar las migraciones

```powershell
python migrate.py
```

Aplica de la `004` a la `013` —tipos de documento DIAN, líneas de concepto, QR, facturación
de planes, auditoría, logo y color por empresa, concepto del descuento— y las anota en
`schema_migrations`. Es idempotente: correrlo de nuevo imprime `[=] ya aplicada` y no toca
nada. Cada vez que alguien suba una migración nueva, basta con volver a correrlo.

### Paso 7 — Sembrar los datos de demostración

```powershell
python seed_proveedor.py
```

Crea la empresa emisora FactuGest S.A.S., el catálogo de planes, catorce empresas
suscritas, tres meses de documentos emitidos por cuenta de terceros y seis meses de
mensualidades. Sin esto el tablero abre vacío.

Al terminar imprime **las llaves de API una sola vez**. Copia la del autoservicio al `.env`:

```
FACTUGEST_API_KEY=fg_live_xxxxxxxx.<secreto>
```

Es la llave con la que FactuGest se factura a sí mismo la mensualidad de cada cliente; sin
ella, el botón de cobrar en `/consumo` falla. Si se pierde, se rota desde el panel en
**Plataforma › Clientes API**.

Para volver al estado anterior: `python seed_proveedor.py --limpiar` deshace exactamente lo
que sembró. **No usar en producción.**

### Paso 8 — Arrancar y entrar

```powershell
python main.py
```

En `http://127.0.0.1:8000`. Los usuarios del panel vienen en el baseline
(`administrador@factugest.com` y los del equipo); las contraseñas están hasheadas con
bcrypt, así que pídeselas a quien administra el repositorio.

### Paso 9 — Configurar el intérprete en PyCharm (opcional)

1. `File → Settings → Project: Factugest → Python Interpreter`
2. Engranaje ⚙ → **Add New Interpreter → Add Local Interpreter**
3. **Virtualenv Environment → Existing**
4. En **Location**, el `.venv` dentro del proyecto: `C:\ruta\al\proyecto\Factugest\.venv`
5. **OK**

### Si algo falla

| Síntoma | Causa |
|---|---|
| `Unknown database 'factugest'` | Falta el paso 2, o `DB_NAME` del `.env` no coincide |
| `Access denied for user 'root'` | `DB_PASSWORD` en el `.env` no corresponde con el MySQL de XAMPP |
| `Unknown column` al abrir una pantalla | Falta correr `python migrate.py` |
| El tablero abre en ceros | Falta correr `python seed_proveedor.py` |
| `Ya hay datos sembrados` | El manifiesto existe: `--limpiar` primero |
| Cobrar la mensualidad falla | `FACTUGEST_API_KEY` vacía en el `.env`, o el servidor apagado |

### Para correr las pruebas

```powershell
pip install -r requirements-dev.txt
python -m pytest
```

No necesitan base de datos: cubren la aritmética tributaria, el documento canónico y el
membrete del PDF.

---

## Cómo iniciar el proyecto

Asegúrate de que MySQL esté corriendo en XAMPP, luego desde la carpeta `Factugest\` (donde está `main.py`) con el entorno virtual activo:

### Modo desarrollo (con recarga automática)
```powershell
uvicorn main:app --reload
```

### Modo simple
```powershell
python main.py
```

La aplicación estará disponible en: **http://127.0.0.1:8000**

### Bonus: documentación automática de la API
FastAPI genera documentación interactiva de forma automática, sin configuración extra:

| URL | Descripción |
|-----|-------------|
| http://127.0.0.1:8000/docs | Swagger UI — prueba los endpoints directamente |
| http://127.0.0.1:8000/redoc | ReDoc — documentación más detallada |

---

## Estructura del proyecto

```
Factugest/
├── main.py                  # Punto de entrada de la app (antes app.py con Flask)
├── database.py              # Conexión a MySQL (sin cambios)
├── templates_config.py      # Instancia compartida de Jinja2Templates (nuevo)
├── requirements.txt         # Dependencias del proyecto
├── routes/                  # Endpoints de cada módulo (antes Blueprints, ahora APIRouter)
│   ├── users.py
│   ├── invoice.py
│   ├── customer.py
│   ├── payment_methods.py
│   ├── discounts.py
│   ├── taxes.py
│   ├── branches.py
│   ├── invoice_payments.py
│   ├── productos.py
│   ├── logs.py
│   └── product_discount.py
├── services/                # Lógica de negocio y consultas SQL (sin cambios)
│   ├── user_service.py
│   ├── invoice_service.py
│   └── ...
├── templates/               # HTML con Jinja2 (diseño sin cambios)
│   ├── layout.html          # Template base con navbar y sidebar
│   ├── index.html
│   ├── invoice/
│   ├── customer/
│   └── ...
└── static/                  # CSS, imágenes, JS (sin cambios)
```

---

## Migración Flask → FastAPI: qué cambió

### 1. Punto de entrada — `main.py`

**Flask (antes):**
```python
from flask import Flask, render_template

app = Flask(__name__)
app.register_blueprint(users_bp)
app.register_blueprint(invoice_bp)
# ...

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
```

**FastAPI (ahora):**
```python
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from templates_config import templates
 
app = FastAPI(title="Factugest")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users_router)
app.include_router(invoice_router)
# ...

# Permite usar url_for() en los templates igual que en Flask
templates.env.globals["url_for"] = app.url_path_for

@app.get("/", name="index")
def index(request: Request):
    return templates.TemplateResponse(request, "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

### 2. Rutas — de Blueprint a APIRouter

**Flask (antes):**
```python
from flask import render_template, Blueprint
from services.user_service import get_all_users

users_bp = Blueprint('users', __name__)

@users_bp.route('/users')
def users():
    data = get_all_users()
    return render_template('users/index.html', usuarios=data)

@users_bp.route('/users/new')
def new_user():
    return render_template('users/form.html')
```

**FastAPI (ahora):**
```python
from fastapi import APIRouter, Request
from services.user_service import get_all_users
from templates_config import templates

router = APIRouter()

@router.get("/users", name="users")
def users(request: Request):
    data = get_all_users()
    return templates.TemplateResponse(request, "users/index.html", {"usuarios": data})

@router.get("/users/new", name="new_user")
def new_user(request: Request):
    return templates.TemplateResponse(request, "users/form.html")
```

**Diferencias clave:**
| Concepto | Flask | FastAPI |
|----------|-------|---------|
| Módulo de rutas | `Blueprint('name', __name__)` | `APIRouter()` |
| Decorador | `@bp.route('/path')` | `@router.get('/path', name='...')` |
| Render template | `render_template('x.html', var=val)` | `templates.TemplateResponse(request, 'x.html', {'var': val})` |
| Request | No se recibe como parámetro | Se recibe como parámetro: `request: Request` |
| Registro en app | `app.register_blueprint(bp)` | `app.include_router(router)` |

> **Importante:** El parámetro `name=` en FastAPI es el nombre del endpoint que se usa en los templates con `url_for()`. Siempre ponlo.

---

### 3. Templates HTML — `url_for()`

El diseño visual **no cambió nada**. Solo se actualizó la forma de generar las URLs.

**Flask (antes):**
```html
<!-- Blueprint + endpoint -->
<a href="{{ url_for('users.new_user') }}">Nuevo usuario</a>

<!-- Archivos estáticos -->
<link href="{{ url_for('static', filename='css/main.css') }}">
```

**FastAPI (ahora):**
```html
<!-- Solo el nombre del endpoint (sin prefijo de blueprint) -->
<a href="{{ url_for('new_user') }}">Nuevo usuario</a>

<!-- Archivos estáticos: filename → path -->
<link href="{{ url_for('static', path='css/main.css') }}">
```

**Tabla de conversión completa:**

| Flask `url_for` | FastAPI `url_for` |
|-----------------|-------------------|
| `url_for('users.users')` | `url_for('users')` |
| `url_for('users.new_user')` | `url_for('new_user')` |
| `url_for('invoice.invoice')` | `url_for('invoice')` |
| `url_for('invoice.new_invoice')` | `url_for('new_invoice')` |
| `url_for('customer.customer')` | `url_for('customer')` |
| `url_for('customer.new_customer')` | `url_for('new_customer')` |
| `url_for('products.product')` | `url_for('product')` |
| `url_for('products.product/new')` | `url_for('product_new')` |
| `url_for('discount.discount')` | `url_for('discount')` |
| `url_for('discount.new_discount')` | `url_for('new_discount')` |
| `url_for('taxes.invoice_taxes')` | `url_for('invoice_taxes')` |
| `url_for('branches.branches')` | `url_for('branches')` |
| `url_for('branches.new_branch')` | `url_for('new_branch')` |
| `url_for('invoice_payments.invoice_payments')` | `url_for('invoice_payments')` |
| `url_for('invoice_payments./invoice_payments/new')` | `url_for('invoice_payments_new')` |
| `url_for('payment_methods.payment_methods')` | `url_for('payment_methods')` |
| `url_for('payment_methods./payment_methods/new')` | `url_for('payment_methods_new')` |
| `url_for('product_discount.product_discounts')` | `url_for('product_discounts')` |
| `url_for('product_discount.new_product_discounts')` | `url_for('new_product_discounts')` |
| `url_for('logs.logs')` | `url_for('logs')` |
| `url_for('setting')` | `url_for('setting')` |
| `url_for('static', filename='x')` | `url_for('static', path='x')` |

---

### 4. Archivos estáticos

En Flask, los archivos estáticos son servidos automáticamente. En FastAPI se montan explícitamente en `main.py`:

```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

Esto es transparente para el equipo — solo afecta a `main.py`, que ya está configurado.

---

### 5. Servicios y base de datos — sin cambios

Los archivos en `services/` y `database.py` **no se modificaron**. La lógica de negocio y las consultas SQL siguen igual.

```python
# services/user_service.py — exactamente igual que antes
from database import get_all_from_table

def get_all_users():
    return get_all_from_table("usuarios")
```

---

## Guía de adaptación para el equipo

### Crear un nuevo endpoint

1. **En el archivo de rutas correspondiente** (ej. `routes/users.py`):

```python
@router.get("/users/{user_id}", name="user_detail")
def user_detail(request: Request, user_id: int):
    data = get_user_by_id(user_id)  # función en services/
    return templates.TemplateResponse(request, "users/detail.html", {"user": data})
```

2. **En el template**, usa el `name=` que pusiste en el decorador:

```html
<a href="{{ url_for('user_detail', user_id=5) }}">Ver usuario</a>
```

3. **El router ya está registrado en `main.py`**, no hay que tocar nada más.

### Crear un endpoint POST (para formularios)

```python
from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse

@router.post("/users/save", name="save_user")
def save_user(request: Request, nombre: str = Form(...), correo: str = Form(...)):
    # lógica para guardar...
    return RedirectResponse(url=str(app.url_path_for("users")), status_code=303)
```

En el template HTML, el formulario apunta al endpoint por nombre:

```html
<form action="{{ url_for('save_user') }}" method="POST">
    <input name="nombre" type="text">
    <input name="correo" type="email">
    <button type="submit">Guardar</button>
</form>
```

### Rutas con parámetro de URL

```python
@router.get("/invoice/{invoice_id}", name="invoice_detail")
def invoice_detail(request: Request, invoice_id: int):
    ...
```

```html
<a href="{{ url_for('invoice_detail', invoice_id=factura.cod_factura) }}">Ver</a>
```

---

## Por qué FastAPI

| Aspecto | Flask | FastAPI |
|---------|-------|---------|
| **Velocidad** | Síncrono | Uno de los frameworks Python más rápidos (comparable a Node.js y Go) |
| **Documentación API** | Manual (Flask-RESTx, etc.) | Automática en `/docs` y `/redoc` |
| **Validación de datos** | Manual | Automática con tipos de Python |
| **Soporte async** | Limitado | Nativo (`async def`) |
| **Mantenimiento** | Maduro, desarrollo lento | Activo, actualizaciones frecuentes |
| **Curva de aprendizaje** | Baja | Baja (similar a Flask) |

Para un sistema de facturación que necesita respuesta rápida en cada transacción, FastAPI ofrece mejor rendimiento sin sacrificar la simplicidad que tenía Flask.

---

## Notas finales

- El diseño visual (templates, CSS, imágenes) **no cambió** respecto a la versión Flask.
- La base de datos y las consultas SQL **no cambiaron**.
- Si modificas la estructura de la BD, exporta el archivo SQL y reemplaza `base\factugest.sql` antes de hacer commit.
- Para cualquier duda sobre la migración Flask → FastAPI, revisar primero este documento.
