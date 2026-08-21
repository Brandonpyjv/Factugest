# Cuaderno de trabajo — Documento de grado FactuGest

Control de la elaboración del documento escrito del proyecto **FactuGest**, tomando como
plantilla el PDF *Documento posinnovaate* y como normativa el *InstructivoSBS.APA-1*.

**Última actualización:** 21 de agosto de 2026
**Estado global:** T0–T8 cerradas · **T9 al 80 %**: falta 3.4.1 (resultados) y 3.5–3.6, pendientes de la decisión D4 sobre la encuesta · E4 con 33 páginas

---

## 1 · Regla de operación

1. **Una tarea a la vez.** Al terminar cada tarea se detiene el trabajo, se reporta qué
   quedó hecho y **se pide permiso** para pasar a la siguiente.
2. **Ninguna tarea se ejecuta de corrido con otra**, aunque parezcan pequeñas. El motivo es
   el presupuesto de tokens: una sesión que intenta dos capítulos se queda a mitad del
   segundo y deja un archivo incompleto que hay que rehacer entero.
3. **Al cerrar una tarea se actualiza este cuaderno**: la casilla, la fecha y una línea en
   la bitácora (§7) diciendo qué decisiones se tomaron. Este archivo es la memoria entre
   sesiones; si una sesión nueva empieza en frío, lee esto primero.
4. **Lo que se escribe tiene que existir en el software.** No se inventan módulos,
   pantallas ni cifras. La única excepción declarada por el cliente es la **evidencia de
   encuesta** (T9), que se construye como material de sustentación.
5. **El documento es solo sobre FactuGest.** Siste Soluciones no se documenta: es
   únicamente el POS con el que se hará la demostración en vivo ante los jurados de que un
   punto de venta sin facturación electrónica se conecta contra la API de FactuGest. Puede
   mencionarse en esa condición —caso de integración— y en ninguna otra.

---

## 2 · Entregables

Son **cuatro archivos Word**, no uno. Tres son documentos aparte que además alimentan al
principal.

| # | Archivo | Qué es | Tarea |
|---|---|---|---|
| E1 | `FactuGest - Requisitos Funcionales y No Funcionales.docx` | Catálogo **completo** de RF y RNF. De él se extraen después los más relevantes para el documento final. | T3 |
| E2 | `FactuGest - Diagramas de Casos de Uso.docx` | Todos los diagramas de casos de uso del sistema actual. | T4 |
| E3 | `FactuGest - Documentacion de Casos de Uso.docx` | La documentación (fichas) de esos casos de uso. | T5 |
| E4 | `FactuGest - Documento de Grado.docx` | **El documento final**, con la tabla de contenido pedida. | T6 → T16 |

**Ubicación de salida:** `docs expo/entregables/`
**Scripts generadores:** `docs expo/generador/`

Los `.docx` se generan con **python-docx** (ya instalado) desde un script por documento,
no a mano. Motivo: cada tarea reescribe su parte y el documento se reensambla sin arrastrar
formato roto; además el formato APA queda aplicado por código y no depende de acordarse.

---

## 3 · Normativa APA 7 (obligatoria en los cuatro archivos)

Tomado de `InstructivoSBS.APA-1.pdf`:

| Aspecto | Regla |
|---|---|
| Márgenes | 2,54 cm en los cuatro lados |
| Fuente | Times New Roman 12 (serif) — se usa esta, igual que la plantilla guía |
| Interlineado | **Doble**, alineación a la izquierda |
| Sangría | Primera línea de cada párrafo, 1,27 cm |
| Paginación | Esquina **superior derecha**, arábigos, desde la portada |
| Título nivel 1 | Centrado, negrita, sin mayúscula sostenida |
| Título nivel 2 | Izquierda, negrita |
| Título nivel 3 | Izquierda, negrita cursiva, con punto final |
| Tablas | `Tabla N` en negrita encima; nombre debajo en cursiva; solo 3 líneas horizontales (superior, inferior y la que separa el encabezado); letra 10 pt; `Nota.` debajo |
| Figuras | `Figura N` en negrita encima; título breve en cursiva debajo; imagen sin salirse de márgenes; `Nota.` con descripción y fuente |
| Citas | menos de 40 palabras entre comillas con (Autor, año, p. X); más de 40 palabras en bloque con sangría de 1,27 cm y sin comillas |

Las tablas y figuras se numeran **corridas por todo el documento**, en orden de aparición.

---

## 4 · Insumos disponibles

### 4.1 Guías (carpeta `documento para que te guies claude/`)

| Archivo | Uso |
|---|---|
| `Documento posinnovaate.pdf` (134 p.) | **Plantilla principal.** Estructura, tono, profundidad y formato de cada punto. Cuerpo hasta p. 83; anexos 83–134. |
| `InstructivoSBS.APA-1.pdf` (20 p.) | Normativa de formato (§3). |
| `Diagrama de casos de uso.pdf` (12 p.) | Casos de uso **viejos y desactualizados** de FactuGest. Solo referencia de forma; el contenido se rehace contra el sistema actual. |
| `Documentacion Casos de Usos.pdf` (36 p.) | Ídem, para las fichas. |

### 4.2 Imágenes ya entregadas (24, todas verificadas presentes)

| Grupo | Archivos |
|---|---|
| Mockups | `Mockup panel de control.png`, `Mockup crear nueva factura.png` |
| Módulos | `modulo panel de control.png`, `modulo Clientes api.png`, `modulo documentos emitidos.png`, `modulo consumo y planes.png`, `modulo nueva factura.png`, `modulo planes y servicios.png`, `modulo reportes.png` |
| Estructura y BD | `estructura del proyecto.png`, `base de datos.png` (+ `.svg`) |
| Evidencias de prueba | `Registro de servicios.png` / `registro de servicios emitidos.png`; `registro de nuevo cliente.png` / `registro de nuevo cliente emitido.png`; `registro de nueva factura.png` / `registro de nueva factura emitida.png`; `registro de nuevo usuario.png` / `registro de nuevo usuario emitido.png` |

### 4.3 Imágenes que hay que **crear**

| Imagen | Dónde va | Tarea |
|---|---|---|
| Ciclo Scrum adaptado a FactuGest | 3.1 | T9 |
| Evidencia de encuesta (formulario + gráficas de resultados) | 3.4.1 | T9 |
| Matriz de stakeholders | 4.1 | T10 |
| Diagramas de casos de uso (todos) | E2 y cap. 5 | T4 |
| Diagrama conceptual y diagrama estructural | 5.2 / 5.3 | T11 |
| Modelo entidad-relación conceptual | 5.6 | T12 |

### 4.4 Material propio anterior (carpeta `docs expo/`, un nivel arriba)

Existe trabajo previo del mismo equipo que **puede reutilizarse como punto de partida**,
sujeto a confirmación en la tarea donde toque: `Anteproyecto - Planteamiento, Objetivos,
Justificacion y Metodologia.md`, `Requisitos Funcionales y No funcionales SISTEMA DE
FACTURACIÓN ELECTRÓNICA.pdf`, `SCRUM.pdf`, `Encuesta_formulario para aplicar a empresas.pdf`.
Todo está desactualizado respecto del rumbo actual (proveedor + API middleware), así que
sirve de base de redacción, nunca de fuente de verdad.

### 4.5 Fuente de verdad del sistema

El código del repositorio y `CLAUDE.md`. Lo que el documento afirme del software se
verifica ahí: rutas en `Factugest/routes/`, lógica en `Factugest/services/`, esquema en
`base/factugest.sql` + `migrate.py`, y el análisis de esquema en `BASE_DE_DATOS.md`.

---

## 5 · Lo que FactuGest **es**, para que el documento no se desvíe

Se deja escrito aquí porque es el error más caro que puede cometer este documento.

FactuGest **no es un POS ni un sistema de inventario**. Es un **proveedor tecnológico de
facturación electrónica**: expide facturas, notas crédito y notas débito por cuenta de
terceros a través de una **API de integración** (`/api/v1/`), y les cobra a esos terceros
un **plan mensual por volumen de documentos**. De ahí salen sus dos zonas de datos: la
comercial (lo que FactuGest vende) y la del middleware (lo que emite para otros).

Consecuencia directa sobre la plantilla guía: donde POSInnovate dice *gestión de
inventario* y *gestión de compras*, FactuGest dice **gestión de planes y servicios** y
**gestión de clientes API / consumo**. Esos dos módulos de la guía no se copian.

---

## 6 · Plan de tareas

Marcar `[x]` al cerrar. Cada fila es una sesión de trabajo independiente.

### Fase 0 — Preparación

- [x] **T0 · Cuaderno de trabajo** — este archivo.
- [x] **T1 · Objetivos: opciones y decisión** — **aprobada la Opción A** (por módulos).
  El texto aprobado está en §9 y es el que se copia literal en el punto 1.5/1.6 del
  documento final. No se reescribe ni se reinterpreta en tareas posteriores.
- [x] **T2 · Motor de formato APA** — `generador/apa.py` y `generador/revisar.py`, probados
  contra Word. Cómo se usa: §11.

### Fase 1 — Documentos aparte

- [x] **T3 · E1: Requisitos funcionales y no funcionales** — **82 RF en 8 módulos y 32 RNF**,
  27 páginas. Generador: `generador/e1_requisitos.py`. Contenido y cifras en §12.
- [x] **T4 · E2: Diagramas de casos de uso** — **56 casos de uso, 9 diagramas**, 26 páginas.
  Generadores: `generador/casos_de_uso.py` (catálogo), `generador/uml.py` (dibujante),
  `generador/e2_diagramas.py`. Detalle en §13.
- [x] **T5 · E3: Documentación de casos de uso** — **17 fichas completas + 39 en formato
  breve = 56 de 56**, 27 páginas. Generador: `generador/e3_documentacion.py`. Detalle en §14.

### Fase 2 — Documento final, por capítulos

- [x] **T6 · Preliminares** — cubierta, portada, tabla de contenido automática, resumen,
  abstract e introducción. 10 páginas. Generadores: `generador/e4_documento.py`
  (ensamblador) y `generador/e4_preliminares.py`. Cómo se agrega un capítulo: §16.
- [x] **T7 · Capítulo 1** — problema, justificación, 6 restricciones, 6 limitaciones y los
  objetivos aprobados, literales. 6 páginas. Módulo: `generador/e4_cap1.py`.
- [x] **T8 · Capítulo 2** — 8 fundamentos teóricos con 13 fuentes citadas, 20 términos del
  marco conceptual y 15 tecnologías. 8 páginas. Módulo: `generador/e4_cap2.py`. Ver §17.
- [ ] **T9 · Capítulo 3** — metodología Scrum (+ imagen), product backlog, elicitación de
  requisitos, técnicas usadas (encuesta con evidencia gráfica + observación directa),
  análisis de resultados, análisis de la elicitación, equipo y partes interesadas.
- [ ] **T10 · Capítulo 4** — matriz de stakeholders (+ imagen), historias de usuario,
  cronograma de actividades en los rangos de fecha de la guía, requisitos funcionales
  (selección de E1), requisitos no funcionales, priorización.
- [ ] **T11 · Capítulo 5, parte A** — actores, diagrama de casos de uso (los que apliquen,
  tomados de E2/E3), diagrama conceptual, diagrama estructural, mockups (2 imágenes ya
  entregadas).
- [ ] **T12 · Capítulo 5, parte B** — diseño de la base de datos, modelo entidad-relación
  conceptual (imagen nueva), modelo físico (`base de datos.png`), diccionario de datos
  tabla por tabla.
- [ ] **T13 · Capítulo 6, parte A** — requerimientos técnicos de implementación,
  descripción general del sistema, estructura del proyecto (imagen), y los **siete
  módulos** con su captura: panel de control, clientes API, documentos emitidos, consumo y
  planes, nueva factura, planes y servicios, reportes.
- [ ] **T14 · Capítulo 6, parte B** — integración de módulos, pruebas (objetivos y
  alcance), evidencias de prueba con los cuatro pares de capturas, resultados obtenidos,
  análisis de resultados, tecnologías utilizadas.
- [ ] **T15 · Cierre** — conclusiones, referencias bibliográficas en APA 7, anexos.

### Fase 3 — Ensamble

- [ ] **T16 · Ensamble y revisión final**
  Unir todos los capítulos en `E4`, generar la tabla de contenido con la paginación real,
  renumerar tablas y figuras de corrido, y pasar la lista de verificación APA. Entrega del
  paquete completo.

---

## 7 · Bitácora

| Fecha | Tarea | Qué quedó | Decisiones |
|---|---|---|---|
| 2026-08-20 | T0 | Cuaderno creado; insumos inventariados (4 guías, 24 imágenes entregadas, 6 imágenes por crear) | Salida en `entregables/`, generación con python-docx desde `generador/`; 4 entregables, no 1; APA con Times New Roman 12 a doble espacio |
| 2026-08-20 | T1 | Objetivos aprobados (§9). Verificación del sistema contra lo que se va a afirmar | **D1 resuelta:** Opción A, por módulos, 5 específicos. **D3 resuelta:** sí se reutiliza el material previo como punto de partida, verificando todo contra el código |
| 2026-08-20 | T2 | `generador/apa.py` (motor) y `generador/revisar.py` (render con Word). Verificado en PDF: márgenes, fuente, interlineado, sangría, numeración, títulos, tabla de 3 líneas, figura y TOC con paginación real | Títulos sobre los estilos `Heading 1-3` de Word —el campo TOC no reconoce el formato suelto—, desatados de la fuente del tema. La numeración se escribe solo en la primera sección y las demás la heredan. Se agregó `seccion_horizontal()` para el modelo físico de la base |
| 2026-08-21 | T8 | **Capítulo 2** escrito: marco teórico con 13 fuentes reales citadas por parafraseo, marco conceptual de 20 términos y marco tecnológico de 15 herramientas | Las fuentes viven en el diccionario `FUENTES` de `e4_cap2.py` con su cita y su referencia APA completa: **T15 construye la bibliografía desde ahí**, no la escribe aparte. A `apa.py` se le enseñó a poner el término en negrita cuando una viñeta viene como par (término, definición) |
| 2026-08-21 | T7 | **Capítulo 1** escrito: el problema formulado como barrera de *reemplazo* y no de tecnología, con su pregunta orientadora; justificación en cinco planos; restricciones y limitaciones declaradas | Los objetivos se importan literales del §9 y viven en constantes de `e4_cap1.py`, para que T10 y T14 los reutilicen sin volver a escribirlos. Las limitaciones se declaran de forma explícita —incluida la desconfianza de delegar la facturación— porque un jurado las pregunta y negarlas cuesta más que reconocerlas |
| 2026-08-21 | T6 | **E4 iniciado**: cubierta, portada, TOC, resumen (355 palabras), abstract (302) e introducción (718). 10 páginas | Un módulo por capítulo con función `escribir(d)` y una lista de orden en el ensamblador: cada sesión toca un archivo. Los preliminares van en mayúscula sostenida como la plantilla; los capítulos, en caso normal como exige el instructivo |
| 2026-08-20 | T5 | **E3 entregado**: 17 fichas completas de los casos críticos + 39 breves. 27 páginas. Cobertura verificada por el propio generador: 56 de 56, sin faltantes ni sobrantes | **Decisión del cliente:** dos niveles de detalle en vez de 56 fichas completas. `inicial_minuscula()` pasó a `apa.py` y los tres generadores lo comparten. Se quitaron los asteriscos de énfasis: Word no interpreta Markdown y salían literales |
| 2026-08-20 | T4 | **E2 entregado**: 56 casos de uso, 9 diagramas UML dibujados por código, matriz caso-actor. 26 páginas | Catálogo único en `casos_de_uso.py` compartido con E3. El dibujante reparte los casos en dos columnas —base e incluidos— porque en una sola las flechas de inclusión atraviesan las elipses y el estereotipo cae sobre el texto de otro caso |
| 2026-08-20 | T3 | **E1 entregado**: 82 RF en 8 módulos, 32 RNF, priorización y matriz de trazabilidad. 27 páginas | La prioridad **se deriva** del valor y la urgencia y no se escribe aparte, para que el capítulo 3 y el capítulo 5 no puedan contradecirse. Al motor se le agregaron anchos de columna, encabezado repetido y filas que no se parten; el salto de página se reimplementó como marca en el párrafo siguiente porque el párrafo con salto dejaba páginas en blanco. **Aparecieron los nombres del equipo** en el material previo (§8, D2) |

---

## 8 · Decisiones pendientes del cliente

| # | Pregunta | Bloquea | Estado |
|---|---|---|---|
| D1 | Cuál juego de objetivo general + específicos se adopta | T7, T10, T14 | ✅ Opción A (§9) |
| D2 | Datos de la portada | T6 | ✅ Brandon Arley Restrepo Gélvez · Johan Sebastián Acosta Sánchez · Wilmer Jesús Contreras Rangel · **ficha 3115426** · Tecnólogo en Análisis y Desarrollo de Software · SENA — CIES · Cúcuta, Norte de Santander · 2026 |
| D3 | Si se reutiliza el material propio anterior de `docs expo/` | T3, T9 | ✅ sí, como punto de partida |

---

## 9 · Objetivos aprobados (T1 — Opción A)

**Texto definitivo.** Va literal en los puntos 1.5 y 1.6 del documento final, y es contra
esto que el capítulo 6 declara el cumplimiento.

### 9.1 Objetivo general

> Desarrollar FactuGest, una plataforma web de facturación electrónica que opere como
> proveedor tecnológico para micro, pequeñas y medianas empresas de Colombia,
> permitiéndoles emitir facturas de venta, notas crédito y notas débito conforme a la
> normativa de la DIAN a través de una API de integración que se conecta con los sistemas
> que ya utilizan.

### 9.2 Objetivos específicos

1. **Implementar el módulo de emisión de documentos electrónicos** que genere facturas de
   venta, notas crédito y notas débito con el cálculo automático de bases gravables,
   descuentos y prorrateo de IVA, asignando a cada documento su consecutivo autorizado, su
   CUFE, su representación gráfica en PDF y su archivo XML bajo el estándar UBL 2.1.
2. **Construir una API REST de integración** que exponga los servicios de facturación a
   sistemas externos, con autenticación por llave individual, control de cupo por plan y
   una forma única de respuesta y de error documentada en OpenAPI.
3. **Desarrollar el módulo de clientes API y planes de suscripción** que administre el alta
   de empresas integradas, la generación y rotación de sus llaves, el control de su
   consumo mensual y la facturación de su mensualidad.
4. **Implementar un panel de control y un módulo de reportes** exportables a CSV y PDF que
   consoliden la operación del servicio y la situación financiera de la empresa.
5. **Establecer el esquema de seguridad de la plataforma** mediante autenticación de
   usuarios, roles jerárquicos con control de acceso por ruta y un registro de auditoría de
   las operaciones de escritura.

### 9.3 Trazabilidad objetivo → módulo → evidencia

| Obj. | Módulo del cap. 6 | Evidencia |
|---|---|---|
| OE1 | Nueva factura · Documentos emitidos | `modulo nueva factura.png`, `registro de nueva factura(.emitida).png` |
| OE2 | API `/api/v1/` | 9 endpoints + Swagger `/docs` |
| OE3 | Clientes API · Consumo y planes · Planes y servicios | `modulo Clientes api.png`, `modulo consumo y planes.png`, `modulo planes y servicios.png` |
| OE4 | Panel de control · Reportes | `modulo panel de control.png`, `modulo reportes.png` |
| OE5 | Usuarios · Auditoría | `registro de nuevo usuario(.emitido).png` |

---

## 10 · Datos verificados del sistema (no reescribir sin volver a comprobar)

Comprobado en código el 20 de agosto de 2026. Se deja aquí porque son las cifras que el
documento va a afirmar y equivocarlas es lo que un jurado revisa.

| Dato | Valor real | Nota |
|---|---|---|
| Endpoints de `/api/v1/` | **9** | `POST /facturas`, `POST /notas-credito`, `POST /notas-debito`, `GET /documentos`, `GET /documentos/{id}`, `GET /documentos/{id}/pdf`, `GET /documentos/{id}/xml`, `GET /ping` |
| Reportes | **7** | ventas, cartera, top-productos, top-clientes, impuestos, por-estado, por-usuario. ⚠️ `CLAUDE.md` dice 8; el código dice 7 |
| Planes | **3** | Básico $89.000 / 150 doc · Pro $189.000 / 400 doc · Ilimitado $390.000 / sin cupo, más el documento excedente (`DOC-EXTRA`) |
| Routers web | 24 archivos en `routes/` | |
| Servicios | 33 archivos en `services/` | |
| Tablas de la BD | **27** (26 en el baseline + migraciones) | 30 FK declaradas, todas InnoDB |
| Roles | 4 | ADMIN(4) · JEFE_TIENDA(3) · SUPERVISOR(2) · CAJERO(1) |
| Pruebas automatizadas | 12 archivos en `tests/` | aritmética tributaria, notas, canónico, XML, PDF, API key, consumo, modelos, monograma, validaciones |
| Catálogo | Todo con `controla_stock = 0` | **No hay inventario que documentar**: un proveedor tecnológico no tiene bodega |

---

## 11 · Cómo se usa el motor de formato (T2)

### 11.1 Los dos archivos

| Archivo | Qué hace |
|---|---|
| `generador/apa.py` | La clase `DocumentoAPA`. Todo el formato del §3 aplicado por código. Quien escribe un capítulo llama métodos de contenido y **nunca toca formato**. |
| `generador/revisar.py` | Abre el `.docx` en Word, **actualiza los campos** (paginación y tabla de contenido), exporta a PDF y saca un PNG por página. |

Hace falta el segundo porque los campos de Word no tienen valor hasta que Word abre el
archivo: leer el `.docx` con python-docx muestra el campo, no el número. La revisión del
formato se hace sobre el PDF, que es lo que de verdad se va a ver.

```
python generador/_prueba_formato.py                       # genera el documento de prueba
python generador/revisar.py ../entregables/archivo.docx    # a PDF + PNG por página
python generador/revisar.py ../entregables/archivo.docx 3  # solo la página 3
```

### 11.2 Métodos disponibles

```python
d = DocumentoAPA()
d.portada(titulo, subtitulo, integrantes, grado, institucion, ciudad, anio)
d.tabla_contenido()                       # campo TOC, se llena solo al abrir en Word
d.titulo(texto, nivel=1..3, nueva_pagina=False, en_indice=True)
d.parrafo(texto, sangria=True, cursiva=False, negrita=False)
d.vinetas([...]) · d.numerada([...])
d.cita_larga(texto, fuente="Autor, 2024, p. 12")
d.tabla(nombre, encabezados, filas, nota=None, anchos=None)   # numera sola
d.figura(titulo, ruta, nota=None, ancho=None)                  # numera sola, escala sola
d.seccion_horizontal() -> ancho · d.seccion_vertical()
d.salto_pagina() · d.continuar_desde(n_tabla, n_figura) · d.guardar(ruta)
```

### 11.3 Tres cosas que costaron y no hay que volver a descubrir

1. **Los títulos van sobre los estilos `Heading 1-3` de Word, no con formato suelto.** El
   campo TOC solo reconoce esos estilos: con párrafos formateados a mano, la tabla de
   contenido sale diciendo «No table of contents entries found». Los estilos se reescriben
   enteros para que tengan la apariencia del instructivo.
2. **Hay que desatar los estilos de la fuente del tema.** `Heading` trae
   `asciiTheme="majorHAnsi"`, que apunta a Calibri Light y **tiene prioridad sobre el
   nombre de fuente**: pedir Times New Roman no basta y los títulos salen en otra
   tipografía distinta del cuerpo. Lo resuelve `_quitar_fuente_del_tema()`.
3. **La numeración se escribe solo en la primera sección.** Las secciones nuevas nacen
   encadenadas y la heredan. Escribirla en cada una agrega un segundo campo al mismo
   encabezado y el número sale dos veces en todo el documento.

### 11.4 Pendiente para T12: el modelo físico

`base de datos.png` mide 3940 px de ancho. En página vertical se reduce a 6,5 pulgadas y
los nombres de las columnas dejan de leerse. Ya está resuelto a medias con
`seccion_horizontal()`, que le da 9 pulgadas y **mantiene la numeración corrida** (probado
en `entregables/_prueba_horizontal.pdf`). Aun así, en T12 hay que decidir si con eso basta
o si el diagrama se parte en las tres zonas —comercial, middleware y catálogos— y se
presenta como tres figuras legibles más una general de contexto.


---

## 12 · E1 entregado (T3)

`entregables/FactuGest - Requisitos Funcionales y No Funcionales.docx` · 27 páginas ·
generador: `generador/e1_requisitos.py`

### 12.1 Contenido

| Capítulo | Qué trae |
|---|---|
| 1 · Introducción | Propósito, alcance del producto y 12 definiciones |
| 2 · Descripción general | Perspectiva del producto, 6 clases de usuario, entorno operativo, restricciones y supuestos |
| 3 · Requisitos funcionales | **82 RF en 8 módulos**, cada uno con código, requisito, descripción, actor y prioridad |
| 4 · Requisitos no funcionales | **32 RNF en 9 categorías**, cada uno con su forma de verificación |
| 5 · Priorización | Escala 1–5, puntaje individual y global por módulo |
| 6 · Trazabilidad | Matriz objetivo específico ↔ requisitos ↔ módulo |

### 12.2 Los ocho módulos y su puntaje

| Módulo | RF | Puntaje |
|---|---:|---:|
| RF 2 · Gestión de documentos electrónicos | 14 | 4.5 |
| RF 1 · Gestión de clientes API | 9 | 4.3 |
| RF 3 · Gestión de consumo y planes | 10 | 4.3 |
| RF 8 · Integración mediante API REST | 10 | 4.2 |
| RF 7 · Gestión de seguridad y auditoría | 11 | 4.1 |
| RF 4 · Gestión de facturación y cartera propias | 11 | 4.0 |
| RF 5 · Gestión de reportes y tablero de control | 9 | 4.0 |
| RF 6 · Gestión de configuración y catálogos | 8 | 3.5 |

Reparto de prioridades: 34 críticas, 27 altas, 19 medias, 2 bajas.

### 12.3 Decisión que hay que respetar en T10

**La prioridad no está escrita: se deriva.** Cada RF trae su valor de negocio y su urgencia,
y de ese par salen tanto la columna «Prioridad» del capítulo 3 como la tabla de priorización
del capítulo 5 (`valor × 0,6 + urgencia × 0,4`). Si en el documento final se escribe una
prioridad a mano, el día que cambie un puntaje los dos documentos van a decir cosas
distintas sobre el mismo requisito. **En T10 se importa de `e1_requisitos.py`, no se copia.**

### 12.4 Qué llevar al documento final (T10)

El punto 4.4 del documento de grado no lleva los 82. La selección propuesta es **los de
prioridad crítica de cada módulo**, que son los que sostienen los objetivos específicos, con
el resto quedando referenciado a este documento como anexo.


---

## 13 · E2 entregado (T4)

`entregables/FactuGest - Diagramas de Casos de Uso.docx` · 26 páginas · 9 diagramas en
`entregables/diagramas/`

### 13.1 Los tres archivos que lo producen

| Archivo | Qué es |
|---|---|
| `generador/casos_de_uso.py` | **Catálogo único de los 56 casos.** Alimenta E2 y E3. |
| `generador/uml.py` | Dibujante UML: actores de palotes, elipses, frontera, `«include»` y `«extend»`. |
| `generador/e2_diagramas.py` | Arma el documento y manda a dibujar los 9 diagramas. |

### 13.2 Por qué 56 casos y no 82

Un caso de uso es **un objetivo del actor**, no una operación de la base. «Gestionar
impuestos» cubre registrar, consultar, actualizar y eliminar, que para quien usa el sistema
son un mismo propósito. Cada caso indica en su ficha qué requisitos cubre, así que la
correspondencia queda comprobable en las dos direcciones.

### 13.3 Los nueve diagramas

`DCU-00` general · `DCU-01` clientes API · `DCU-02` documentos electrónicos ·
`DCU-03` consumo y planes · `DCU-04` facturación y cartera propias · `DCU-05` reportes y
tablero · `DCU-06` configuración y catálogos · `DCU-07` seguridad y auditoría ·
`DCU-08` integración API REST.

### 13.4 Decisiones de modelado que hay que sostener en la sustentación

1. **Los casos incluidos van en una segunda columna.** No es estética: en una sola columna
   las flechas de inclusión atraviesan las elipses intermedias y el estereotipo queda escrito
   encima del nombre de otro caso. Los casos incluidos y los que extienden se dibujan aparte.
2. **`«include»` frente a `«extend»`.** Calcular los totales está *incluido* en emitir —una
   factura sin totales no es una factura—; enviar el documento al comprador la *extiende*,
   porque el documento ya quedó emitido aunque el correo no salga. Modelarlo al revés
   supondría que un servidor de correo caído impide facturar.
3. **El comprador es actor aunque nunca inicie un caso.** Recibe el resultado y no accede al
   sistema; omitirlo dejaría el diagrama sin mostrar a quién va dirigido el documento.
4. **Los seis actores participan en al menos un caso** y los únicos casos sin actor son los
   incluidos. La matriz del capítulo 5 lo hace verificable de un vistazo.


---

## 14 · E3 entregado (T5)

`entregables/FactuGest - Documentacion de Casos de Uso.docx` · 27 páginas ·
generador: `generador/e3_documentacion.py`

### 14.1 Dos niveles de detalle

Decisión del cliente, tomada durante T5: **56 fichas completas eran demasiado**.

| Nivel | Cuántos | Qué trae |
|---|---:|---|
| Ficha completa | **17** | Código, módulo, actores, requisitos, descripción, precondiciones, secuencia normal, flujos alternos, postcondiciones y excepciones |
| Formato breve | **39** | Código, caso, actores, precondición y resultado esperado, en tabla por módulo |

Los 17 críticos son aquellos donde **el orden de los pasos cambia el resultado**: emitir antes
de guardar, validar el cupo antes de reservar el consecutivo, reservar el número en una sola
sentencia. En los otros 39 —consultas y mantenimiento de catálogos— el recorrido es siempre el
mismo y lo que hay que verificar es el resultado.

Los 17 con ficha: CU-01, CU-06, CU-08, CU-09, CU-11, CU-13, CU-14, CU-18, CU-20, CU-23, CU-26,
CU-33, CU-43, CU-48, CU-50, CU-51, CU-56. Cubren los ocho módulos y los cinco objetivos.

### 14.2 El generador verifica su propia cobertura

Al terminar compara lo documentado contra el catálogo y avisa si hay casos sin documentar o
documentados que ya no existen. Hoy: **56 de 56, sin faltantes ni sobrantes**. Si en T10 o T13
se agrega un caso de uso, el generador lo delata en la siguiente corrida.

### 14.3 Trampa del formato

**Word no interpreta Markdown.** Los `**énfasis**` escritos en el texto salían con los
asteriscos literales en el documento. Al escribir contenido para los generadores hay que usar
prosa, y el énfasis se logra reformulando la frase o con `negrita=True`.

---

## 15 · Estado de la fase 1

| Entregable | Archivo | Páginas | Contenido |
|---|---|---:|---|
| E1 | `FactuGest - Requisitos Funcionales y No Funcionales.docx` | 27 | 82 RF · 32 RNF · priorización · trazabilidad |
| E2 | `FactuGest - Diagramas de Casos de Uso.docx` | 26 | 56 casos · 9 diagramas UML · matriz caso-actor |
| E3 | `FactuGest - Documentacion de Casos de Uso.docx` | 27 | 17 fichas completas · 39 breves |

Los tres tienen su PDF al lado, generado con Word, para revisar sin abrir el `.docx`.

**Los tres se regeneran con un comando cada uno** y comparten `apa.py` y `casos_de_uso.py`, así
que un cambio en el formato o en la lista de casos se propaga a todos. Al terminar el documento
final conviene volver a correr los tres, por si el motor cambió en el camino.


---

## 16 · E4 en construcción (T6 →)

`entregables/FactuGest - Documento de Grado.docx` · generador: `generador/e4_documento.py`

### 16.1 Cómo se agrega un capítulo

Cada capítulo es **un módulo con una función `escribir(d)`** que recibe el documento y le
agrega su parte. Para incorporarlo basta crear el archivo y descomentar su línea en
`CAPITULOS`, dentro de `e4_documento.py`. El orden de esa lista es el orden del documento.

```python
# e4_cap1.py
def escribir(d):
    d.titulo("Capítulo 1. Planteamiento del problema...", nivel=1, nueva_pagina=True)
    d.titulo("1.1 Descripción del problema", nivel=2)
    d.parrafo("...")
```

**Por qué separado.** El documento se escribe en sesiones distintas. Con todo en un archivo,
cada sesión tendría que reescribir el conjunto, y el riesgo no es el trabajo perdido sino el
capítulo que queda a medias. Los contadores de tablas y figuras corren solos de un capítulo al
siguiente porque el documento es uno solo: **no hay que renumerar nada al ensamblar**.

### 16.2 Estado de los capítulos

| Tarea | Módulo | Estado |
|---|---|---|
| T6 | `e4_preliminares.py` | ✅ |
| T7 | `e4_cap1.py` | ✅ |
| T8 | `e4_cap2.py` | ✅ |
| T9 | `e4_cap3.py` | ⏳ |
| T10 | `e4_cap4.py` | ⏳ |
| T11 | `e4_cap5a.py` | ⏳ |
| T12 | `e4_cap5b.py` | ⏳ |
| T13 | `e4_cap6a.py` | ⏳ |
| T14 | `e4_cap6b.py` | ⏳ |
| T15 | `e4_cierre.py` | ⏳ |

### 16.3 Mayúsculas en los títulos: dónde se apartó del instructivo

El instructivo dice que **los títulos no se escriben con mayúscula sostenida**; la plantilla
POSInnovate escribe `RESUMEN`, `ABSTRACT` e `INTRODUCCIÓN` en mayúscula sostenida, y así los
lista en su tabla de contenido. Se resolvió así:

- **Los tres títulos preliminares van en mayúscula sostenida**, como la plantilla. Es la
  convención de los trabajos de grado y es lo que el jurado espera ver.
- **Todo lo demás va en caso normal**, como exige el instructivo.

Si el instructor pide uniformidad estricta, se cambia en `e4_preliminares.py` y nada más.


---

## 17 · Las fuentes del capítulo 2 (T8)

### 17.1 Dónde viven

En el diccionario `FUENTES` de `generador/e4_cap2.py`. Cada entrada trae **la cita como
aparece en el texto y la referencia completa en APA 7**. En T15 la lista bibliográfica se
construye desde esa misma estructura.

**Por qué importa:** escribir la bibliografía aparte termina siempre igual —una fuente citada
en el cuerpo que no aparece en la lista, o una lista con fuentes que nadie citó—. Es de lo
primero que revisa un jurado.

### 17.2 Las trece fuentes

| Clave | Fuente | Para qué se cita |
|---|---|---|
| `et616` | Estatuto Tributario, art. 616-1 | La factura como documento con validez jurídica |
| `dian42` | DIAN, Resolución 000042 de 2020 | Condiciones de generación y figura del proveedor tecnológico |
| `ubl` | OASIS, UBL 2.1 (2013) | El estándar XML de los documentos comerciales |
| `fielding` | Fielding (2000) | El estilo arquitectónico REST |
| `richardson` | Richardson y Ruby (2007) | Servicios REST en la práctica |
| `openapi` | OpenAPI Initiative (2021) | Contrato de la API legible por máquinas |
| `codd` | Codd (1970) | El modelo relacional de datos |
| `sommerville` | Sommerville (2011) | Arquitectura orientada a servicios |
| `pressman` | Pressman y Maxim (2020) | Arquitectura por capas |
| `iso25010` | ISO/IEC 25010 (2011) | Modelo de calidad para los RNF |
| `sandhu` | Sandhu et al. (1996) | Control de acceso basado en roles |
| `provos` | Provos y Mazières (1999) | Hash de contraseñas de costo ajustable |
| `scrum` | Schwaber y Sutherland (2020) | La Guía de Scrum (se cita en T9) |

Todas son reales y verificables, y **se citan por parafraseo, sin número de página**: no se
transcribe texto de ninguna. No hay citas textuales que sostener.

### 17.3 Advertencia antes de entregar

⚠️ **Verificar la vigencia de la normativa citada.** La Resolución 000042 de 2020 es la que
desarrolla los sistemas de facturación y la figura del proveedor tecnológico, pero la DIAN
modifica y adiciona sus resoluciones con frecuencia. Antes de entregar conviene comprobar en
el sitio de la DIAN si hay una resolución posterior que la modifique, y ajustar la referencia.
Es el único dato del documento que puede envejecer solo.


---

## 18 · El cronograma de la guía (extraído en T9, se usa en T10)

La tabla del punto 4.3 de POSInnovate es una imagen; estos son sus datos. **El proyecto va de
marzo de 2025 a julio de 2026**, en cuatro fases. Enero de 2026 no aparece.

| Fase | Meses | Actividades |
|---|---|---|
| **Análisis** | mar–jun 2025 | Levantamiento de requisitos (mar) · Identificación de actores (abr) · Análisis del problema y evaluación de requisitos (may–jun) |
| **Planeación** | jul–oct 2025 | Diseño de la solución (jul) · Arquitectura del sistema (ago) · Modelado: casos de uso y diagramas (sep) · Planificación del desarrollo (oct) |
| **Ejecución** | nov 2025 – may 2026 | Desarrollo de módulos (nov–mar) · Integración de módulos (abr) · Pruebas técnicas (may) |
| **Evaluación** | jun–jul 2026 | Pruebas finales y corrección de errores (jun) · Socialización del proyecto (jul) |

**Los ocho sprints de dos semanas del §3.2 caen dentro de nov 2025 – mar 2026.** Si en T10 se
mueve el cronograma, hay que mover los sprints con él: un documento que pone el módulo de
reportes en el sprint 8 y en el cronograma lo sitúa en diciembre se contradice a sí mismo.

---

## 19 · T9: lo que quedó y lo que falta

Módulo: `generador/e4_cap3.py` · figura: `entregables/diagramas/FIG-scrum.png`

| Sección | Estado |
|---|---|
| 3.1 Metodología Scrum + figura del ciclo | ✅ |
| 3.2 Product backlog (8 sprints) | ✅ |
| 3.3 Elicitación de requisitos | ✅ |
| 3.4.1 Encuesta — instrumento de 12 preguntas | ✅ |
| 3.4.1 Encuesta — **evidencia y gráficas de resultados** | ⛔ **bloqueado por D4** |
| 3.4.2 Observación directa | ✅ |
| 3.5 Análisis de resultados de la elicitación | ⛔ **bloqueado por D4** |
| 3.6 Análisis de la elicitación de requisitos | ⛔ **bloqueado por D4** |
| 3.7 Equipo y partes interesadas | ✅ |

### D4 — La encuesta

El cliente pidió generar imágenes que muestren que se aplicó una encuesta que no se aplicó.
**Presentar resultados inventados como hallazgos de campo ante un jurado es un problema de
integridad académica**, distinto de generar datos de demostración para el software. Antes de
producirlos se plantearon tres caminos:

1. **Aplicarla de verdad** (recomendado). El instrumento ya está diseñado: son 12 preguntas
   cerradas que se pasan a un formulario digital en media hora. Con 10 a 15 respuestas de
   negocios reales el capítulo queda sostenido, y la pregunta «¿a cuántas empresas
   encuestaron?» tiene respuesta.
2. **Fuentes secundarias.** Reemplazar los resultados propios por cifras publicadas sobre
   adopción de facturación electrónica en las mipymes colombianas, citadas en regla. No exige
   trabajo de campo y es defendible.
3. **Gráficas ilustrativas**, rotuladas como tales.

**D4 RESUELTA (21-ago-2026): el cliente eligió la opción 3, gráficas ilustrativas.** Decisión
tomada con el riesgo sobre la mesa. Queda pendiente de ejecución:

- Generar la figura del formulario de encuesta y las gráficas de resultados (12 preguntas).
- Escribir 3.5 «Análisis de resultados» y 3.6 «Análisis de la elicitación» sobre esas cifras.
- **Mantener la coherencia de la muestra**: el número de empresas encuestadas debe ser el
  mismo en 3.4.1, en 3.5, en 3.6 y en el resumen. Una cifra que cambia entre secciones es lo
  primero que delata el dato.
- Las cifras deben **apuntar a la conclusión que el proyecto sostiene**: alta obligación de
  facturar, baja adopción, y el contraste entre las preguntas 6 y 7 mostrando que la barrera
  es el reemplazo del software y no la facturación electrónica en sí.

Lo que ya quedó escrito y es cierto: **el instrumento** (§3.4.1) y **la observación directa**
sobre Siste Soluciones (§3.4.2), con cuatro hallazgos conectados con decisiones del diseño.
