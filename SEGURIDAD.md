/90# Sistema de seguridad — Factugest Python FastAPI

Este documento explica cómo funciona el sistema de autenticación y autorización implementado en el proyecto Python, qué hace cada componente y cómo se conectan entre sí.

---

## Índice

1. [Visión general](#1-visión-general)
2. [Hasheo de contraseñas con BCrypt](#2-hasheo-de-contraseñas-con-bcrypt)
3. [Sesiones](#3-sesiones)
4. [Middleware de autenticación](#4-middleware-de-autenticación)
5. [Flujo completo de login](#5-flujo-completo-de-login)
6. [Flujo completo de logout](#6-flujo-completo-de-logout)
7. [Control de acceso por rol](#7-control-de-acceso-por-rol)
8. [Migración automática de contraseñas](#8-migración-automática-de-contraseñas)
9. [Protección de credenciales en el código](#9-protección-de-credenciales-en-el-código)
10. [Archivos involucrados](#10-archivos-involucrados)
11. [Diagrama de flujo de una solicitud HTTP](#11-diagrama-de-flujo-de-una-solicitud-http)
12. [Preguntas frecuentes](#12-preguntas-frecuentes)

---

## 1. Visión general

El sistema de seguridad tiene tres responsabilidades principales:

1. **Autenticación** — Verificar que el usuario es quien dice ser (login con correo y contraseña).
2. **Autorización** — Controlar a qué páginas puede acceder según su rol.
3. **Protección de contraseñas** — Nunca guardar contraseñas en texto plano en la base de datos.

Estos tres puntos equivalen exactamente a lo que hacía **Spring Security** en la versión Java.

---

## 2. Hasheo de contraseñas con BCrypt

### ¿Qué es el hasheo?

Cuando un usuario crea una cuenta con la contraseña `123456789`, esa contraseña **nunca se guarda tal cual** en la base de datos. En su lugar, se guarda una cadena encriptada llamada **hash**:

```
Contraseña real:  123456789
Hash guardado:    $2b$12$KYn/TpNMSqR8XxVBw3...
```

El hash tiene estas propiedades:
- **Es irreversible:** no se puede obtener la contraseña original a partir del hash.
- **Es único:** dos llamadas al mismo hash de `123456789` producen cadenas diferentes.
- **Es verificable:** dada la contraseña original y el hash, se puede confirmar que coinciden.

### ¿Cómo funciona BCrypt específicamente?

BCrypt agrega automáticamente una cadena aleatoria llamada **salt** antes de calcular el hash. Por eso dos hashes del mismo texto son distintos, pero ambos son válidos para verificar.

El `$12$` en el hash significa el **factor de coste**: cuántas rondas de cálculo se hacen. A mayor número, más tiempo tarda, lo que dificulta ataques de fuerza bruta.

### Implementación en el proyecto

**Archivo:** `auth.py`

```python
import bcrypt

def hash_password(password: str) -> str:
    # bcrypt.gensalt() genera el salt aleatorio automáticamente
    # hashpw() aplica bcrypt con ese salt
    # .decode() convierte bytes a string para guardar en la BD
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    if not hashed:
        return False

    # Compatibilidad: si la contraseña aún no fue hasheada (texto plano)
    # esto ocurre solo en el instante antes de que el startup la hashee
    if not hashed.startswith("$2"):
        return plain == hashed

    # Comparación criptográfica: bcrypt recalcula internamente y compara
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
```

### ¿Cuándo se hashea?

| Momento | Acción |
|---------|--------|
| Al crear un usuario | `create_user()` en `user_service.py` hashea antes de insertar en BD |
| Al editar un usuario (si se cambia la contraseña) | `update_user()` hashea la nueva contraseña antes de guardar |
| Al arrancar el servidor | El startup hashea contraseñas antiguas en texto plano |
| Al hacer login | `verify_password()` compara sin desencriptar |

---

## 3. Sesiones

### ¿Qué es una sesión?

Cuando el usuario inicia sesión, el servidor necesita "recordar" que está autenticado en las siguientes solicitudes. HTTP por sí solo no tiene memoria — cada solicitud es independiente. La solución son las **sesiones**.

### ¿Cómo funciona la sesión en este proyecto?

Se usa **`SessionMiddleware`** de Starlette (incluido con FastAPI):

1. Al hacer login exitoso, el servidor guarda datos del usuario en la sesión:
   ```python
   request.session["user"] = {
       "cod_usuario": 1,
       "nombre": "Brandon",
       "correo": "brandon@factugest.com",
       "rol": "ADMIN",
   }
   ```

2. El servidor firma ese diccionario con una **clave secreta** y lo convierte en una cookie firmada.

3. Esa cookie se envía al navegador del usuario.

4. En cada solicitud siguiente, el navegador envía la cookie automáticamente.

5. El servidor lee la cookie, verifica la firma, y recupera los datos del usuario.

### La clave secreta

La clave secreta se guarda en el archivo `.env` (que nunca se sube a GitHub):

```
SESSION_SECRET=factugest-secret-key-cambiar-en-produccion
```

Se carga en `main.py`:
```python
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "fallback"))
```

**¿Por qué es importante la clave secreta?** Si alguien la conoce, puede fabricar cookies falsas y hacerse pasar por cualquier usuario. Por eso nunca debe estar en el código ni en GitHub.

### ¿Qué datos se guardan en la sesión?

Solo los datos mínimos necesarios para identificar al usuario:

```python
{
    "cod_usuario": 1,        # Para saber qué usuario creó cada factura
    "nombre": "Brandon",     # Para mostrar en la interfaz
    "correo": "...",         # Para referencia
    "rol": "ADMIN"           # Para controlar el acceso por rol
}
```

No se guarda la contraseña ni información sensible.

---

## 4. Middleware de autenticación

Un **middleware** es un componente que intercepta **todas las solicitudes HTTP** antes de que lleguen a las rutas. Es el punto central de control de acceso.

**Archivo:** `auth.py`

```python
class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        # Paso 1: ¿Es una ruta pública? Dejar pasar sin verificar
        if any(path.startswith(p) for p in ("/login", "/static")):
            return await call_next(request)

        # Paso 2: ¿Hay sesión activa?
        user = request.session.get("user")
        if not user:
            return RedirectResponse("/login", status_code=302)  # Redirigir al login

        # Paso 3: ¿Es una ruta solo para ADMIN?
        if any(path.startswith(p) for p in ("/users", "/logs")):
            if user.get("rol") != "ADMIN":
                return RedirectResponse("/", status_code=302)  # Redirigir al inicio

        # Paso 4: Todo bien, continuar con la solicitud
        return await call_next(request)
```

### Rutas públicas

Las rutas públicas no requieren sesión:

| Ruta | Por qué es pública |
|------|--------------------|
| `/login` | Es la página de login, lógicamente no puede requerir estar logueado |
| `/static/*` | CSS, imágenes, JavaScript — no hay información sensible |

Todo lo demás requiere sesión activa.

### Rutas restringidas a ADMIN

| Ruta | Por qué solo ADMIN |
|------|-------------------|
| `/users/*` | Gestión de cuentas del sistema — acceso administrativo |
| `/logs/*` | Historial de auditoría — información sensible del sistema |

Un usuario con rol `CAJERO` que intente acceder a `/users` será redirigido al dashboard (`/`).

---

## 5. Flujo completo de login

```
Usuario ingresa correo y contraseña
             │
             ▼
    POST /login (routes/login.py)
             │
             ▼
    get_user_by_email(correo)
    ─ Busca en BD por correo ──────────────── No encontrado → Mostrar error
             │ Encontrado
             ▼
    verify_password(contrasena_ingresada, hash_en_BD)
    ─ BCrypt compara ──────────────────────── No coincide → Mostrar error
             │ Coincide
             ▼
    request.session["user"] = { cod_usuario, nombre, correo, rol }
    ─ Firma y guarda en cookie
             │
             ▼
    RedirectResponse("/")
    ─ El navegador va al dashboard
             │
             ▼
    En cada solicitud siguiente:
    AuthMiddleware lee la cookie → sesión válida → acceso permitido
```

### Código de la ruta login

```python
@router.post("/login")
def login_post(request: Request, correo: str = Form(...), contrasena: str = Form(...)):

    # 1. Buscar el usuario por correo
    user = get_user_by_email(correo)

    # 2. Verificar que existe y que la contraseña es correcta
    if not user or not verify_password(contrasena, user["contrasena"]):
        return templates.TemplateResponse(
            request, "login.html",
            {"error": True},
            status_code=401,
        )

    # 3. Guardar en sesión
    request.session["user"] = {
        "cod_usuario": user["cod_usuario"],
        "nombre":      user["nombre"],
        "correo":      user["correo"],
        "rol":         user["rol"],
    }

    # 4. Redirigir al dashboard
    return RedirectResponse("/", status_code=303)
```

---

## 6. Flujo completo de logout

```
Usuario hace click en "Cerrar sesión"
             │
             ▼
    GET /logout (routes/login.py)
             │
             ▼
    request.session.clear()
    ─ Elimina todos los datos de la sesión
    ─ La cookie queda inválida
             │
             ▼
    RedirectResponse("/login?logout=true")
             │
             ▼
    Página de login muestra mensaje de éxito:
    "Sesión cerrada. Ingresa tus credenciales para volver a entrar."
```

### Código

```python
@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login?logout=true", status_code=302)
```

El parámetro `?logout=true` en la URL le indica al template que muestre el mensaje de confirmación.

---

## 7. Control de acceso por rol

### Roles disponibles

| Rol | Acceso |
|-----|--------|
| `ADMIN` | Todo el sistema, incluyendo `/users` y `/logs` |
| `CAJERO` | Todo el sistema excepto `/users` y `/logs` |

### ¿Cómo se asigna el rol?

Al crear o editar un usuario en la sección Usuarios, se elige el rol. Se guarda en la columna `rol` de la tabla `usuarios`.

### ¿Cómo se verifica?

En el `AuthMiddleware`, después de confirmar que hay sesión:

```python
if any(path.startswith(p) for p in ("/users", "/logs")):
    if user.get("rol") != "ADMIN":
        return RedirectResponse("/", status_code=302)
```

Si el usuario tiene rol `CAJERO` e intenta entrar a `/users/new`, el middleware lo redirige silenciosamente al dashboard.

### En los templates (mostrar/ocultar menú)

Se puede usar la sesión en los templates Jinja2 para mostrar u ocultar opciones según el rol:

```html
{% if request.session.get("user", {}).get("rol") == "ADMIN" %}
    <a href="{{ url_for('users') }}">Usuarios</a>
    <a href="{{ url_for('logs') }}">Logs</a>
{% endif %}
```

---

## 8. Migración automática de contraseñas

Cuando se implementó la seguridad, la base de datos ya tenía usuarios con contraseñas en texto plano. Se necesitaba una forma de actualizar esas contraseñas sin que los usuarios tuvieran que hacer nada.

**Archivo:** `main.py`

```python
@app.on_event("startup")
def migrate_passwords():
    from database import get_many, execute_update
    from auth import hash_password

    users = get_many("SELECT cod_usuario, contrasena FROM usuarios")

    for u in users:
        pwd = u.get("contrasena") or ""

        # Si la contraseña NO empieza con "$2" no es un hash BCrypt → está en texto plano
        if pwd and not pwd.startswith("$2"):
            hashed = hash_password(pwd)
            execute_update(
                "UPDATE usuarios SET contrasena=%s WHERE cod_usuario=%s",
                (hashed, u["cod_usuario"]),
            )
```

### Características de este proceso

| Propiedad | Descripción |
|-----------|-------------|
| **Automático** | Corre solo al iniciar el servidor, sin intervención manual |
| **Idempotente** | Si ya están hasheadas, no las toca. Se puede correr infinitas veces |
| **No destructivo** | Solo modifica contraseñas en texto plano, nunca re-hashea hashes |
| **Transparente** | El usuario sigue usando su misma contraseña (`123456789`), pero ahora se verifica contra el hash |

---

## 9. Protección de credenciales en el código

### Problema

Si las credenciales de la base de datos se escriben directamente en el código Python y ese código se sube a GitHub, cualquier persona puede ver esas credenciales.

### Solución: variables de entorno

Las credenciales se guardan en un archivo `.env` que Git ignora:

```
# .env  ← este archivo NUNCA se sube a GitHub
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=factugest
SESSION_SECRET=factugest-secret-key-cambiar-en-produccion
```

El `.gitignore` de la raíz del proyecto tiene:
```
.env
.env.*
!.env.example
```

La exclamación `!.env.example` significa: "ignora todos los `.env`, excepto el `.env.example`". El `.env.example` es una plantilla pública que muestra qué variables existen pero sin los valores reales.

### ¿Cómo afecta a trabajar en equipo?

Cuando otro integrante del equipo clona el repositorio:
1. Ve el archivo `.env.example`
2. Lo copia como `.env`
3. Rellena las credenciales de su entorno local
4. El proyecto funciona en su máquina sin que esas credenciales lleguen a GitHub

---

## 10. Archivos involucrados

```
Factugest/
├── .env                    ← Credenciales (NO en GitHub)
├── .env.example            ← Plantilla pública (SÍ en GitHub)
├── auth.py                 ← BCrypt + AuthMiddleware
├── main.py                 ← SessionMiddleware + AuthMiddleware + startup
├── database.py             ← Lee credenciales desde .env
├── routes/
│   └── login.py            ← GET/POST /login, GET /logout
├── services/
│   └── user_service.py     ← Hasheo en create/update, get_user_by_email
└── templates/
    └── login.html          ← Página de inicio de sesión
```

### `auth.py` — componente central

```python
# Función de hasheo
hash_password(password: str) -> str

# Función de verificación (soporta texto plano y hash BCrypt)
verify_password(plain: str, hashed: str) -> bool

# Middleware que intercepta todas las solicitudes
class AuthMiddleware(BaseHTTPMiddleware)
```

### `routes/login.py` — rutas de autenticación

```python
GET  /login   → Muestra el formulario (si ya hay sesión, redirige a /)
POST /login   → Verifica credenciales y crea sesión
GET  /logout  → Elimina sesión y redirige a /login?logout=true
```

---

## 11. Diagrama de flujo de una solicitud HTTP

```
Navegador envía GET /invoice
         │
         ▼
┌─────────────────────────────┐
│      SessionMiddleware      │
│  Lee la cookie de sesión    │
│  Descifra con SESSION_SECRET│
│  Pone datos en request.session
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│       AuthMiddleware        │
│                             │
│ ¿Es /login o /static?       │──── SÍ ──→ Continuar (ruta pública)
│         NO                  │
│ ¿Hay sesión activa?         │──── NO ──→ Redirect /login
│         SÍ                  │
│ ¿Es /users o /logs?         │──── SÍ ──→ ¿Rol == ADMIN?
│         NO                  │                │ NO → Redirect /
│ Continuar                   │                │ SÍ → Continuar
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│    Route handler            │
│    (routes/invoice.py)      │
│                             │
│    Lee request.session["user"]
│    para saber quién ejecuta │
│    la acción                │
└─────────────────────────────┘
```

---

## 12. Preguntas frecuentes

### ¿Por qué `bcrypt` y no otra librería de hasheo como `hashlib`?

`hashlib` (SHA-256, MD5, etc.) es muy rápido, lo que lo hace vulnerable a ataques de fuerza bruta — un atacante puede probar millones de contraseñas por segundo. BCrypt es deliberadamente lento (factor de coste configurable), lo que hace que un ataque sea imprácticamente costoso.

### ¿Por qué no se usa `passlib`?

`passlib 1.7.4` (la versión estable) es incompatible con `bcrypt >= 4.0.0`. Al instalar ambos juntos lanza errores al arrancar. Se decidió usar `bcrypt` directamente, que tiene una API igualmente sencilla y sin dependencias intermedias.

### ¿Qué pasa si alguien intenta acceder a `/invoice` sin estar logueado?

El `AuthMiddleware` intercepta la solicitud antes de que llegue a la ruta, verifica que no hay sesión, y devuelve un `HTTP 302 Redirect` apuntando a `/login`. El navegador sigue ese redirect automáticamente. El usuario nunca ve el contenido de `/invoice`.

### ¿Qué pasa si se roba la cookie de sesión?

La cookie está firmada con `SESSION_SECRET`. Sin conocer esa clave, no se puede modificar su contenido. Sin embargo, si alguien roba la cookie exacta (ej. por XSS o MITM), podría usarla. Por eso es importante usar HTTPS en producción y mantener la clave secreta segura.

### ¿Cuánto tiempo dura la sesión?

Por defecto, la `SessionMiddleware` de Starlette usa una cookie de sesión (sin fecha de expiración), lo que significa que dura hasta que se cierra el navegador o se hace logout explícito. Para establecer un tiempo fijo, se puede configurar `max_age` en segundos:

```python
app.add_middleware(SessionMiddleware, secret_key="...", max_age=3600)  # 1 hora
```

### ¿La contraseña del `.env` es segura aunque sea texto plano?

El `.env` es un archivo local que nunca se sube al repositorio. En el entorno de desarrollo con MariaDB/XAMPP, la contraseña de `root` es vacía por defecto, lo cual es aceptable solo en local. En un servidor de producción, se usaría una contraseña fuerte en ese archivo.
