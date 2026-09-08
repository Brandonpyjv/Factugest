# Dónde quedó el proyecto

Última actualización: **2026-08-25**, rama `api`.

Este archivo es para retomar sin releer el historial. El *porqué* de cada decisión está en
`CLAUDE.md`; aquí solo está el estado y lo que sigue.

---

## ⏭️ Lo primero al retomar — limpiar las tres tablas muertas

**Pendiente, analizado y comprobado el 25-ago-2026.** Sobran tres tablas en los dos
proyectos. No es una sospecha: se clonó `factugest`, se borraron las tres en la copia y
pasaron las 36 rutas GET del panel, `migrate.py` y los 190 tests. MySQL las dejó caer sin
protestar, lo que ya prueba que ninguna FK apuntaba a ellas.

| Tabla | Filas | Usos en código | Qué es |
|---|---:|---:|---|
| `clientes` | 3 | 0 | Del prototipo. La reemplazó `customers`. Trae datos de plantilla venezolana (`tipo_documento = 'V'`, teléfonos `0412-…`). |
| `configuracion` | 0 | 0 | Del prototipo, clave-valor. La reemplazó el `.env`. Nada que ver con la pantalla `/configuracion`, que lee los catálogos. |
| `productos_descuentos` | 2 | 0 | Gemela muerta de `producto_descuento`, a una letra. Tiene las dos únicas filas huérfanas de la base: apuntan a los productos `1` y `3`, y el catálogo va del `77` al `86`. |

Lo que hay que hacer:

1. Una **migración `014`** que las tire si existen, en FactuGest **y en el POS**. Va como
   migración y no como `DROP` suelto: así se aplica sola en cualquier base y queda escrito
   por qué se fueron.
2. Quitarlas también de `base/factugest.sql` en los dos repos. **Si no, una instalación
   limpia las vuelve a crear** — el baseline las declara.

⚠️ `factura_descuento` y `factura_impuesto` **no entran en esta tanda**. También están
vacías y muertas, pero tienen FK y aparecen en dos `DELETE` de
`services/invoice_service.py:426-427`. Borrarlas exige quitar antes esas dos líneas.

**Lo que NO se toca**, aunque el diagrama las muestre sueltas o vacías:

- `schema_migrations` — bitácora de `migrate.py`. Describe la base, no el negocio: atarla
  a algo sería el error. Las versiones saltan de la 005 a la 008 y está bien, la 006 y la
  007 tampoco existen en `MIGRACIONES`.
- `movimientos_inventario` — vacía y correcta. Un proveedor tecnológico no tiene bodega;
  quien la llena es el POS.
- `producto_descuento` — vacía en FactuGest pero **el código la usa**
  (`routes/invoice.py:645`, `services/invoice_service.py:81`); en `sistesoluciones` tiene
  10 filas.
- Los catálogos `municipios` (1.122) y `departamentos` (33): sueltos en el diagrama porque
  son catálogos, consultados en trece sitios.

`BASE_DE_DATOS.md` tiene el análisis largo, pero es del 20-ago: no incluye la comprobación
empírica ni el detalle de que `logs` sobrevivió en `sistesoluciones` (tiene 5 filas, y la
migración 010 solo la borra si está vacía).

---

## Estado

**Cerrado**: las fases 1 a 5 del plan, el track de validación V.1–V.8 y dos tandas de
puesta a punto (P.1–P.17) que no estaban previstas: el catálogo, las tablas y la auditoría
el 19; el documento fiscal y el tablero el 20.

Hay además una lectura completa del esquema en `BASE_DE_DATOS.md` —qué tablas sobran, cuál
es el único hueco real y qué no hay que tocar—, pendiente de leer.

| | FactuGest | Siste Soluciones (POS) |
|---|---|---|
| Ruta | `D:\01. Proyectos\Factugest Python\Factugest` | `D:\01. Proyectos\SisteSoluciones-POS` |
| Rama | `api` | `main` |
| Base de datos | `factugest` | `sistesoluciones` |
| Puerto | 8000 | 8001 |
| Pruebas | **190** | 64 |
| Migraciones | 001–013 | — |

El POS **no genera PDF**: se los pide a FactuGest. Por eso los arreglos del PDF no hubo
que replicarlos allá.

### Lo último que se hizo (2026-08-19 y 20)

- **Descuentos del pie de la factura** (`83c4407`). La fila «(-) Descuentos (0,0 %)» junto a
  un importe real se partió en dos, cada una con su base y su concepto. Migración **013**
  para guardar `documentos.descripcion_descuento_factura`, que la API descartaba.
- **Monograma** (`06278aa`). La empresa sin logo sale con sus dos iniciales sobre su color,
  igual en el PDF que en el panel, desde `services/monograma.py`. De paso se arregló que el
  nombre del emisor se montaba encima del NIT (interlineado del estilo base).
- **Investigación de Factus** (`2caa2ed`). Ver `FACTUS.md`.

### Cómo levantar la demo

MySQL arriba, y en cada repo `python main.py`. Instalación limpia:
importar `base/factugest.sql` → `python migrate.py` → `python seed_proveedor.py`
(imprime las llaves una sola vez; la del autoservicio va al `.env`).

---

## Pendientes, en orden

### 1 · Mandar el mensaje a Factus — bloquea todo lo demás

Está redactado y listo para copiar en `docs/factus/pregunta-whatsapp.md`, en tres mensajes.

**La pregunta que importa**: si una cuenta de Factus puede emitir por cuenta de varias
empresas con NIT distinto, o si hace falta una cuenta por cliente. De eso depende cómo se
construye el adaptador, así que conviene preguntarlo antes de escribir código.

### 2 · Implementar `ProveedorFactus`

Todo el análisis está en **`FACTUS.md`**, con el contrato de la factura, las tablas de
códigos y los tres choques con lo que ya tenemos. Resumen de los choques:

- **La numeración deja de ser nuestra.** Factus asigna el consecutivo desde su rango; hoy
  lo asigna `numeracion_service` dentro de la transacción. Recomendación: que mande Factus
  y partir la emisión en dos pasos (`PENDIENTE` → transmitido). El estado ya existe.
- **Una cuenta = una empresa** (pendiente de confirmar, punto 1).
- **El CUFE y el XML propios pasan a ser de mentira**: los reales los firma Factus. Los
  nuestros se quedan solo para el proveedor `simulado`.

Y una buena: `POST /v2/bills/:number/send-email` acepta **nuestro** PDF en base64, así que
el membrete por emisor, el logo y el monograma siguen siendo lo que recibe el comprador.

La costura ya está hecha en `services/dian_proveedor.py`: hay una interfaz `ProveedorDian`,
un `RespuestaDian` que ya contempla que el proveedor devuelva su propio número y CUFE, y
`get_proveedor()` ya nombra `factus` como pendiente.

**Orden sugerido**: credenciales de sandbox → tabla de traducción de códigos →
`ProveedorFactus` con pruebas sin red → partir la emisión en dos pasos → una factura real
en sandbox comparando totales → correo con nuestro PDF → notas → producción.

### 3 · Fase 6 — salir de local

Dockerfile por aplicación, `docker-compose` con MySQL y proxy HTTPS, configuración
externalizada. **Todo esto se puede hacer ya**; contratar servidor y dominio depende de una
decisión tuya.

---

## Documentos vivos

| Dónde | Qué |
|---|---|
| `CLAUDE.md` | Las reglas que no se rompen. Se lee antes de programar. |
| `FACTUS.md` | Todo lo de Factus y el análisis de qué hay que cambiar. |
| `docs/factus/skill-factus-crear-factura.md` | El contrato de la factura, publicado por Factus. |
| `docs/factus/tablas-de-referencia-dian.txt` | Los códigos DIAN. |
| `docs/factus/pregunta-whatsapp.md` | El mensaje por enviar. |
| Cuaderno de Ruta *(artifact)* | La bitácora: cada fase y cada defecto. |
| Anatomía de FactuGest *(artifact)* | Cómo está hecho por dentro. |

Los dos artifacts se actualizan al cerrar cada tanda de trabajo. **Todavía no reflejan la
investigación de Factus**: eso queda para la próxima sesión.
