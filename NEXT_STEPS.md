# Dónde quedó el proyecto

Última actualización: **2026-08-20**, rama `api`.

Este archivo es para retomar sin releer el historial. El *porqué* de cada decisión está en
`CLAUDE.md`; aquí solo está el estado y lo que sigue.

---

## Estado

**Cerrado**: las fases 1 a 5 del plan, el track de validación V.1–V.8 y una tanda de puesta
a punto (P.1–P.12) que no estaba prevista.

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

### 4 · Borrar la vista anterior de crear factura

Cuando apruebes la nueva (`/invoice/nueva`). Son cuatro cosas y van en los dos repos:
la plantilla `invoice/form.html`, el GET `/invoice/new`, la entrada del menú y la constante
`VISTAS` en `routes/invoice.py`.

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
