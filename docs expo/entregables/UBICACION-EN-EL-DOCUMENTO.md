# Dónde está cada artefacto en el Documento de Grado

Levantado el **25-ago-2026** sobre `FactuGest - Documento de Grado.docx` (10,2 MB, del
24-ago). **121 páginas.**

Los números de página se obtuvieron repaginando una copia del `.docx` con Word y se
contrastaron contra el índice del propio documento: **coinciden exactamente**. El PDF de
esta carpeta es del 21-ago pero también tiene 121 páginas, así que la numeración sirve
para los dos.

---

## Resumen

| Sección | Páginas | Tablas | Diagramas |
|---|---|---:|---:|
| 4.2 Historias de usuario | **46 – 47** | 1 | 0 |
| 4.4 Requisitos funcionales | **49 – 57** | 9 | 0 |
| 4.5 Requisitos no funcionales | **58 – 59** | 1 | 0 |
| 5.2 Diagrama de casos de uso | **64 – 69** | 1 | 3 |

---

## 4.2 Historias de usuario — p. 46-47

**Tabla 6**, «Historias de usuario del sistema», p. 46 · 15 filas × 2 columnas =
**14 historias** (HU-01 a HU-14). La tabla cabe entera en la 46; la 47 son los dos
párrafos de cierre.

## 4.4 Requisitos funcionales — p. 49-57

Nueve tablas: una de resumen y ocho de módulo, una por subsección.

| | Tabla | Pág. | Tamaño | Requisitos |
|---|---|---:|---|---:|
| 4.4 | Tabla 8 — Módulos funcionales y distribución | 49 | 10×4 | resumen |
| 4.4.1 | Tabla 9 — RF 1 Clientes API | 50 | 6×4 | 5 |
| 4.4.2 | Tabla 10 — RF 2 Documentos electrónicos | 51 | 9×4 | 8 |
| 4.4.3 | Tabla 11 — RF 3 Consumo y planes | 52 | 6×4 | 5 |
| 4.4.4 | Tabla 12 — RF 4 Facturación y cartera propias | 53 | 3×4 | 2 |
| 4.4.5 | Tabla 13 — RF 5 Reportes y tablero de control | 54 | 4×4 | 3 |
| 4.4.6 | Tabla 14 — RF 6 Configuración y catálogos | 55 | 3×4 | 2 |
| 4.4.7 | Tabla 15 — RF 7 Seguridad y auditoría | 56 | 6×4 | 5 |
| 4.4.8 | Tabla 16 — RF 8 Integración API REST | 57 | 5×4 | 4 |

Los ocho módulos suman **34 requisitos críticos**, que es exactamente lo que anuncia el
texto: de los 82 levantados se presentan los 34 de prioridad crítica. Cuadra.

## 4.5 Requisitos no funcionales — p. 58-59

**Tabla 17**, «Requisitos no funcionales del sistema» · 15 filas × 4 columnas =
**14 RNF** de los 32 especificados. El rótulo va en la 58 y la tabla cae en la 59.
Las columnas son Código · Categoría · Requisito · **Verificación**.

## 5.2 Diagrama de casos de uso — p. 64-69

**Tres diagramas** en el cuerpo:

| Figura | Pág. | Qué es |
|---|---:|---|
| Figura 5 | 65 | Diagrama general de casos de uso de FactuGest |
| Figura 6 | 66 | Módulo de gestión de documentos electrónicos |
| Figura 7 | 67 | Módulo de integración mediante API REST |

Dentro va **5.2.1 Documentación de un caso de uso** (p. 68-69), con **Tabla 21**, la ficha
del **CU-08 «Emitir factura de venta»**, 10×2. El rótulo está en la 68 y la tabla en la 69.

> **Por si lo preguntan en la sustentación:** el análisis identificó **56 casos de uso** y
> **nueve diagramas** (uno general y ocho por módulo). En el cuerpo van solo tres; los
> nueve completos están en el **Anexo B** (`FactuGest - Diagramas de Casos de Uso.docx`) y
> las fichas de los 17 casos críticos en el **Anexo C**.

---

## Los anexos (Tabla 34, p. 121)

| Anexo | Documento | Contenido |
|---|---|---|
| A | Especificación de requisitos | Los 82 RF completos, en ocho módulos |
| B | Diagramas de casos de uso | Los nueve diagramas |
| C | Documentación de casos de uso | Fichas de los 17 casos críticos |
| D | Contrato de la interfaz | OpenAPI de las nueve operaciones, generado por el sistema |
