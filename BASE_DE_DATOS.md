# La base de FactuGest — lectura del esquema

Análisis del **20 de agosto de 2026**. Base `factugest`, MySQL, **27 tablas**, **30 claves
foráneas declaradas**, todas InnoDB. No se cambió nada: esto es una lectura.

> Versión con diagramas: https://claude.ai/code/artifact/15c8697a-9a56-406d-b402-dabf7f4fe1b0

---

## 1 · La respuesta corta

Las tablas sueltas que se ven en el diagrama de DataGrip son reales, pero **«suelta» no es
un diagnóstico**: hay cuatro razones distintas por las que una tabla aparece sin líneas, y
tres son sanas.

Un catálogo de municipios está al margen porque es un catálogo. Una tabla del prototipo de
hace dos años está al margen porque nadie la borró. **Se ven igual en el diagrama y no se
parecen en nada.**

De las cinco tablas sin ninguna FK: **tres sobran, una es infraestructura correcta y una
esconde el único hueco real.**

---

## 2 · Cómo está organizada: dos zonas y un puente

Esto explica por qué hay dos tablas para casi todo (dos de documentos, dos de líneas, dos
de terceros). No es duplicación.

| Zona | Tablas | Qué guarda |
|---|---|---|
| **Comercial** | `facturas`, `detalle_factura`, `customers`, `productos` | Nuestras ventas: los planes que vendemos |
| **Middleware** | `clientes_api`, `receptores`, `documentos`, `documento_lineas`, `documento_eventos` | Lo que emitimos por cuenta de terceros |
| **Puente** | `facturas_plan` | Qué mes de qué cliente ya se cobró |
| **Compartida** | `empresas`, `usuarios`, `municipios`, `impuestos` | Emisores y catálogos |

**Por qué la separación no es opcional:** el tablero y los ocho reportes leen `facturas`.
Si un documento emitido para la clínica se guardara ahí, aparecería como ingreso nuestro.

Una fila de `empresas` es un emisor, sea nuestro o de un cliente: por eso es compartida y
no pertenece a una zona. Las dos zonas nunca se consultan juntas; `facturas_plan` es el
único sitio donde se tocan.

---

## 3 · Las cinco tablas sueltas, una por una

| Tabla | Filas | Usos | Qué es | Veredicto |
|---|---:|---:|---|---|
| `schema_migrations` | 11 | solo `migrate.py` | Bitácora del migrador: qué cambios de esquema se aplicaron. Atarla a algo no tendría sentido — no habla del negocio sino de la base. | **correcta** |
| `detalle_factura` | 77 | 13 | Las líneas de nuestras facturas. Le faltan las dos FK. | **hueco real** |
| `clientes` | 3 | 0 | Del prototipo original. Trae «juan perez» y «María García» con tipo de documento `V` y teléfonos `0412-…` (formato venezolano). La reemplazó `customers`. | **sobra** |
| `configuracion` | 0 | 0 | Dos columnas, `clave` y `valor`. Nunca se escribió ni se leyó: la configuración vive en el `.env`. | **sobra** |
| `productos_descuentos` | 2 | 0 | Ver abajo. | **sobra** |

### 3.1 · Hay dos tablas para lo mismo, a una letra de distancia

Existen **`producto_descuento`** y **`productos_descuentos`**. Las dos guardan el mismo par
—qué descuento aplica a qué producto— con las columnas en distinto orden. **El código usa
la primera; la segunda no la toca nadie.**

La muerta tiene **las dos únicas filas huérfanas de toda la base**: apuntan a los productos
`1` y `3`, que ya no existen (hoy el catálogo va del `77` al `85`). Son de otro catálogo,
de otro momento del proyecto.

Un nombre en singular y otro en plural con comportamientos distintos es de lo que más caro
se paga: el día que alguien escriba en la que no es, **no va a fallar nada** — el descuento
simplemente no se aplicará, y nadie sabrá por qué.

### 3.2 · El hueco real: `detalle_factura` sin claves foráneas

Es la única de las cinco que importa. Guarda las líneas de cada factura nuestra y **no
declara ninguna FK**: ni a `facturas` ni a `productos`.

Compárala con su gemela de la otra zona: `documento_lineas` **sí** tiene su clave hacia
`documentos`, con borrado en cascada. La diferencia no es de criterio — es de edad. Las
tablas del middleware se crearon con una migración de este año; `detalle_factura` viene del
esquema original.

La base está limpia hoy: **cero líneas huérfanas sobre 77**. Lo que la sostiene es el
código —la emisión es una transacción y el borrado pasa siempre por el mismo servicio—, no
la base. Funciona, pero es una regla que hay que recordar en vez de una que se aplica sola.

---

## 4 · Dos tablas vacías que el código solo sabe borrar

`factura_descuento` y `factura_impuesto` **sí tienen FK** —por eso no salen como sueltas—
pero están vacías desde el principio. En todo el proyecto aparecen en **dos líneas, y las
dos son `DELETE`**: se limpian al actualizar una factura. Nunca se inserta ni se lee.

Son de un modelo anterior donde impuestos y descuentos se guardaban aparte. Hoy viven como
columnas dentro de `detalle_factura` y `facturas`. **Están conectadas y no se usan**, que
es el caso contrario al de los catálogos: sueltas y utilísimas.

| Tabla | Filas | Por qué está vacía |
|---|---:|---|
| `factura_descuento` | 0 | Reemplazada por `facturas.cod_descuento_factura` y las columnas de descuento de cada línea |
| `factura_impuesto` | 0 | Reemplazada por `detalle_factura.impuesto_porcentaje` e `impuesto_valor` |
| `producto_descuento` | 0 | Viva en el código, sin datos: los planes no llevan descuento por producto |
| `movimientos_inventario` | 0 | **Correcto.** Es el kardex, y FactuGest no mueve existencias: sus productos son servicios con `controla_stock = 0`. Quien la llena es el POS, en su base |

---

## 5 · Las relaciones que existen sin estar declaradas

Ocho relaciones viven en las consultas pero no en el esquema, así que la base no las
vigila. Comprobadas contra los datos reales:

| Relación no declarada | Huérfanos | |
|---|---:|---|
| `detalle_factura.cod_factura` → `facturas` | 0 de 77 | íntegra |
| `detalle_factura.cod_producto` → `productos` | 0 | íntegra |
| `facturas.cod_factura_referencia` → `facturas` (notas) | 0 | íntegra |
| `facturas.cod_descuento_factura` → `descuentos` | 0 | íntegra |
| `receptores.cod_municipio` → `municipios` | 0 de 269 | íntegra |
| `movimientos_inventario.cod_factura` → `facturas` | 0 | íntegra |
| `producto_descuento.cod_producto` → `productos` | 0 | íntegra |
| `productos_descuentos.cod_producto` → `productos` | **2 de 2** | **rota** |

Dice dos cosas. La tranquilizadora: **la única relación rota está dentro de la tabla que
sobra**; lo que se usa está íntegro.

La otra conviene no perderla de vista: *íntegra* no es lo mismo que *protegida*. Que hoy no
haya huérfanos se lo debemos al código. La base no lo impide — lo permite, y da la
casualidad de que nadie lo ha hecho.

> **Detalle menor:** la clave primaria de `detalle_factura` se llama `cod_destalle`. Es una
> errata de hace años y está en el `ORDER BY` de todas las consultas que leen líneas.
> Inofensiva; renombrarla toca varios sitios. Anotada, no urgente.

---

## 6 · Si algún día se toca

Nada de esto es urgente y nada rompe hoy. Por relación entre coste y lo que evita:

1. **Borrar `productos_descuentos`.** La más barata y la que más confusión evita: cero
   usos, dos filas huérfanas y un nombre a una letra de la que sí se usa.
2. **Borrar `clientes` y `configuracion`.** Cero usos, cero relaciones. Lo único que
   aportan es hacerte preguntar qué son cada vez que abres el diagrama.
3. **Añadir las dos FK de `detalle_factura`.** La única con valor técnico real. Los datos
   ya están limpios, así que entraría sin conflicto. Convierte una regla que hay que
   recordar en una que la base aplica sola.
4. **Decidir sobre `factura_descuento` y `factura_impuesto`.** O se borran, o se documenta
   por qué se quedan.

### Lo que no tocaría

- **Los catálogos, aunque parezcan sueltos.** `municipios` (1.122 filas) y `departamentos`
  (33) casi no tienen líneas hacia la operación: eso es lo normal en un catálogo, y en un
  diagrama automático siempre quedan en un rincón. `municipios` se consulta en trece sitios.
- **`movimientos_inventario` vacía.** Es correcta y hay que saber defenderla: un proveedor
  tecnológico no tiene bodega. Existe porque el código de inventario es el mismo que usa el
  POS, y ahí sí se llena.
- **Unificar las dos zonas.** Es la pregunta que puede caer en la sustentación —«¿por qué
  dos tablas de documentos?»— y la respuesta es que mezclarlas haría que las ventas de
  nuestros clientes aparecieran como ingresos nuestros en el tablero y en los ocho reportes.
