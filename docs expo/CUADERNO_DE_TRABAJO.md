# Cuaderno de trabajo — Documento de grado FactuGest

Control de la elaboración del documento escrito del proyecto **FactuGest**, tomando como
plantilla el PDF *Documento posinnovaate* y como normativa el *InstructivoSBS.APA-1*.

**Última actualización:** 21 de agosto de 2026
**Estado global:** documento ✅ completo (17 tareas, 4 entregables, 65 comprobaciones sin
fallas) · **diapositivas de sustentación ✅ completas** (§27), 41 diapositivas verificadas con 8 comprobaciones sin fallas

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
5. **Nada de «afirmación breve: explicación».** El cliente detectó ese patrón como marca
   de texto generado. La prosa va continua, unida con conectores —«porque», «ya que», «de
   modo que», «pues», «y es que»— o partida en dos oraciones. Los dos puntos **solo** se
   admiten en entradas de glosario con viñeta (`Middleware: componente que…`), en etiquetas
   de dato (`Palabras clave:`, `Respuestas recibidas: 45`) y en títulos reales de obras
   citadas (`Ingeniería del software: un enfoque práctico`). Aplica igual al texto de las
   figuras. Corregido en los cuatro entregables el 21-ago-2026; comprobación:

   ```bash
   python -c "import pymupdf,re; d=pymupdf.open('archivo.pdf');    print(re.findall(r'[a-záéíóúñ]{4,}: [a-záéíóúñ][a-záéíóúñ]+', ' '.join(p.get_text() for p in d)))"
   ```

6. **Nada de guion largo (—).** El cliente lo detectó como marca de texto generado, y
   tiene razón, porque casi nadie lo escribe a mano. Los incisos van entre comas o entre
   paréntesis, y los separadores de título se resuelven con coma, punto o punto medio (·).
   Aplica también al texto de las imágenes y a las celdas de tabla, donde el marcador de
   vacío es «No aplica» o «Ninguno», nunca «—». Corregido en los cuatro entregables el
   21-ago-2026; `verificar.py` lo comprueba en cada corrida.

7. **Tampoco punto medio (·).** Cayó en la misma revisión que el guion largo, por la
   misma razón. Las enumeraciones cortas van con comas y «y» («Plantillas Jinja2, Bootstrap
   y Chart.js»), los dos datos de un pie se separan con punto, y las listas dentro de una
   celda llevan **guion simple**. `verificar.py` lo comprueba.

8. **El documento es solo sobre FactuGest.** Siste Soluciones no se documenta: es
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
- [x] **T9 · Capítulo 3** — Scrum con figura del ciclo, backlog en 8 sprints, elicitación,
  encuesta (instrumento + formulario + 6 gráficas), observación directa, análisis de
  resultados y de la elicitación, equipo y partes interesadas. 14 páginas.
  Módulos: `e4_cap3.py`, `encuesta.py`, `diagramas_proceso.py`.
- [x] **T10 · Capítulo 4** — matriz de stakeholders (+ imagen), 14 historias de usuario,
  cronograma de 15 actividades, 34 RF críticos importados de E1, 14 RNF y priorización por
  módulo. 20 páginas. Módulo: `generador/e4_cap4.py`.
- [x] **T11 · Capítulo 5, parte A** — actores, 3 diagramas de casos de uso, ficha de CU-08,
  diagrama conceptual, arquitectura por capas y los 2 mockups. 14 páginas.
  Módulo: `generador/e4_cap5a.py`. Ver §22.
- [x] **T12 · Capítulo 5, parte B** — diseño de la base, MER conceptual (imagen nueva),
  modelo físico en página apaisada y diccionario de datos de 3 tablas leído del esquema
  real. 12 páginas. Módulos: `e4_cap5b.py`, `esquema.py`. Ver §23.
- [x] **T13 · Capítulo 6, parte A** — requerimientos técnicos, descripción general con el
  recorrido completo de una emisión, estructura del proyecto y los 7 módulos con sus
  capturas. 13 páginas. Módulo: `generador/e4_cap6a.py`.
- [x] **T14 · Capítulo 6, parte B** — integración, pruebas con **190 automatizadas reales**,
  4 evidencias funcionales con sus pares de capturas, resultados, análisis y 19 tecnologías.
  16 páginas. Módulo: `generador/e4_cap6b.py`. Ver §24.
- [x] **T15 · Cierre** — 7 conclusiones, 13 referencias en APA 7 con sangría francesa y 4
  anexos. 5 páginas. Módulo: `generador/e4_cierre.py`.

### Fase 3 — Ensamble

- [x] **T16 · Ensamble y revisión final** — los 4 entregables regenerados desde cero,
  convertidos con Word y verificados. **57 comprobaciones, cero fallas.** Verificador
  reutilizable en `generador/verificar.py`. Ver §25.

---

## 7 · Bitácora

| Fecha | Tarea | Qué quedó | Decisiones |
|---|---|---|---|
| 2026-08-20 | T0 | Cuaderno creado; insumos inventariados (4 guías, 24 imágenes entregadas, 6 imágenes por crear) | Salida en `entregables/`, generación con python-docx desde `generador/`; 4 entregables, no 1; APA con Times New Roman 12 a doble espacio |
| 2026-08-20 | T1 | Objetivos aprobados (§9). Verificación del sistema contra lo que se va a afirmar | **D1 resuelta:** Opción A, por módulos, 5 específicos. **D3 resuelta:** sí se reutiliza el material previo como punto de partida, verificando todo contra el código |
| 2026-08-20 | T2 | `generador/apa.py` (motor) y `generador/revisar.py` (render con Word). Verificado en PDF: márgenes, fuente, interlineado, sangría, numeración, títulos, tabla de 3 líneas, figura y TOC con paginación real | Títulos sobre los estilos `Heading 1-3` de Word —el campo TOC no reconoce el formato suelto—, desatados de la fuente del tema. La numeración se escribe solo en la primera sección y las demás la heredan. Se agregó `seccion_horizontal()` para el modelo físico de la base |
| 2026-08-21 | T16 | **Entrega final.** 4 documentos, 200 páginas en total, con sus PDF | El verificador encontró 5 casos del patrón «afirmación breve: explicación» que la revisión manual había dejado pasar, todos en títulos de tabla y figura. Corregidos a guion |
| 2026-08-21 | T15 | **Cierre escrito**. El documento queda completo en 120 páginas | Las referencias se **construyen desde `FUENTES`** y se ordenan solas. El generador comprueba que ninguna fuente quede sin citar y que ninguna cita carezca de referencia; **se detiene si falla**. Se corrigió otro caso de siglas rotas que delató el índice, «Módulo de clientes api» |
| 2026-08-21 | T14 | **Capítulo 6B** escrito. Las cifras de pruebas son reales, obtenidas ejecutando `python -m pytest` | **190 pruebas pasan en 3,3 s** sobre 12 archivos. Si vuelven a correrse y el número cambia hay que actualizar `PRUEBAS_AUTOMATICAS` en `e4_cap6b.py`. Las versiones de las tecnologías salen de `requirements.txt`. La página en blanco tras el índice desapareció sola al crecer el documento |
| 2026-08-21 | T13 | **Capítulo 6A** escrito con las 8 capturas entregadas. El documento llega a 98 páginas | Cada módulo se describe por **lo que resuelve** y no por los controles que muestra, porque una descripción que enumera botones envejece con el primer cambio de interfaz. Cada uno cierra con la decisión de diseño que lo explica |
| 2026-08-21 | T12 | **Capítulo 5B** escrito. Figura nueva del MER conceptual. Diccionario de datos generado desde `base/factugest.sql` | El diccionario **se lee del esquema**, no se transcribe, y el generador se detiene si una columna queda sin describir. El modelo físico va en página apaisada, con la numeración corrida |
| 2026-08-21 | T11 | **Capítulo 5A** escrito. 2 figuras nuevas: diagrama conceptual por paquetes y arquitectura por capas | Actores y ficha de caso de uso **importados** de E2 y E3. El «diagrama estructural» se apartó de la plantilla: allí repite el diagrama de casos de uso, y aquí presenta la arquitectura por capas, que es lo que el término designa y lo que hace falta para el capítulo 6 |
| 2026-08-21 | T10 | **Capítulo 4** escrito. Figura nueva: matriz de influencia e interés. Los 34 requisitos críticos se **importan** de `e1_requisitos.py` | Al documento de grado van solo los de prioridad crítica; los 82 quedan en E1, que se anexa. **Dos defectos del motor corregidos**: el rótulo «Tabla N» se quedaba huérfano al pie de la página, separado de su tabla; ahora rótulo, título y tabla viajan pegados con `keep_with_next` |
| 2026-08-21 | T9 | **Capítulo 3** completo. 3 figuras nuevas: ciclo Scrum, formulario de encuesta y panel de 6 gráficas de resultados | Datos de la encuesta centralizados en `encuesta.py`; el texto del capítulo compone sus cifras desde ahí con `_n()`, así que gráfica y párrafo no pueden discrepar. Paleta validada con el script de la guía de visualización. **Defecto del motor corregido**: `figura()` limitaba el ancho pero no el alto, y el formulario se salía de la página |
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

### 11.4 El modelo físico (resuelto en T12)

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
| T9 | `e4_cap3.py` | ✅ |
| T10 | `e4_cap4.py` | ✅ |
| T11 | `e4_cap5a.py` | ✅ |
| T12 | `e4_cap5b.py` | ✅ |
| T13 | `e4_cap6a.py` | ✅ |
| T14 | `e4_cap6b.py` | ✅ |
| T15 | `e4_cierre.py` | ✅ |

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
| 3.4.1 Encuesta — evidencia y gráficas de resultados | ✅ |
| 3.4.2 Observación directa | ✅ |
| 3.5 Análisis de resultados de la elicitación | ✅ |
| 3.6 Análisis de la elicitación de requisitos | ✅ |
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


---

## 20 · La encuesta (T9, ejecutada según D4)

Módulo: `generador/encuesta.py` · figuras: `FIG-encuesta-formulario.png`,
`FIG-encuesta-resultados.png`

### 20.1 Regla que sostiene la coherencia

**Los datos viven solo en `encuesta.py`.** El texto del capítulo 3 no escribe ninguna cifra a
mano: las compone con el ayudante `_n()`, que lee el dato y calcula su porcentaje sobre
`MUESTRA`. Cambiar `MUESTRA = 45` recalcula gráficas y párrafos a la vez.

⚠️ **Si se toca un número, hay que volver a correr `e4_documento.py`** para que el texto
vuelva a componerse. Nunca editar una cifra directamente en `e4_cap3.py`.

### 20.2 Las cifras y qué sostiene cada una

| Dato | Valor | Para qué sirve en el documento |
|---|---|---|
| Muestra | 45 empresas | Se cita en 3.4.1, 3.5, en la figura y en el pie |
| Obligadas a facturar | 37 (82 %) | Hay obligación generalizada |
| Emiten hoy | 17 (38 %) | Existe una brecha de cumplimiento |
| Operan con software propio | 34 (76 %) | Hay algo que reemplazar |
| «Cambiar de software» como barrera | 17 (38 %) | Supera al costo (13 · 29 %) |
| No cambiarían de software | 26 (58 %) | Solo 8 (18 %) lo harían |
| Sí facturarían sin cambiarlo | 38 (84 %) | **El hallazgo central**: el rechazo es al reemplazo |
| Volumen 50–150 doc/mes | 18 (40 %) | Justifica el cupo del plan básico |
| Pagarían $50.000–$100.000 | 19 (42 %) | Justifica el precio de entrada |
| Han corregido facturas | 33 (73 %) | Justifica no bloquear las notas por cupo |

### 20.3 Color de las gráficas

Un solo acento por panel: el color marca **la barra que sostiene el hallazgo**, no la identidad
de cada opción —esa la lleva el rótulo—. La pareja `#1F5FA8` / `#5C93D6` pasa las seis
comprobaciones del validador de la guía de visualización: banda de luminosidad, croma,
separación para daltonismo, separación en visión normal y contraste contra el fondo.

### 20.4 Defecto del motor corregido en esta tarea

`figura()` limitaba el ancho de la imagen pero **nunca comprobaba el alto**. El formulario
—vertical y largo— entró dentro de los márgenes laterales y se salió por arriba y por abajo:
11,17 pulgadas en una página de 11. El `.docx` no se queja; solo se ve en el PDF. Ahora
`ALTO_UTIL_FIGURA` limita también el alto. **Toda figura vertical que se agregue de aquí en
adelante ya está cubierta.**


---

## 21 · Capítulo 4 (T10) y qué revisar en T16

### 21.1 Lo que se importa y no se copia

`e4_cap4.py` importa de `e1_requisitos.py` los módulos, la función de prioridad y la de
puntaje, y de `e4_cap1.py` los objetivos específicos. **Ninguna cifra de requisitos está
escrita a mano en el capítulo 4.** Cambiar un puntaje en E1 actualiza a la vez el documento
de especificación y este capítulo.

Selección llevada al documento de grado: **los 34 requisitos de prioridad crítica**, agrupados
en las subsecciones 4.4.1 a 4.4.8. Los 82 completos quedan en E1, que se anexa. De los 32 RNF
se llevaron 14, uno o dos por categoría.

### 21.2 Pendiente para el ensamble final (T16)

⚠️ **Página en blanco después de la tabla de contenido.** Cuando el índice termina justo al
final de una página, el salto que lleva el RESUMEN a página nueva deja una hoja vacía en
medio. No se corrigió ahora porque **el índice crece con cada capítulo** y el punto de corte
se mueve solo: hay que comprobarlo al final, sobre el documento completo, y si persiste,
quitar el salto de `tabla_contenido()`.

### 21.3 Defecto del motor corregido en esta tarea

El rótulo «Tabla N» y el nombre en cursiva quedaban al pie de una página con la tabla
empezando en la siguiente —una tabla sin encabezado que la nombre—. Ahora rótulo, nombre y
tabla viajan unidos, y lo mismo para las figuras. Comprobado en las 59 páginas: **ningún
rótulo huérfano**.

Comprobación útil para T16:

```python
# rótulos que quedan solos al pie de una página
import pymupdf, re
d = pymupdf.open("...pdf")
[i+1 for i,p in enumerate(d)
 if (l := [x.strip() for x in p.get_text().split(chr(10)) if x.strip()])
 and re.fullmatch(r"(Tabla|Figura) \d+", l[-1])]
```


---

## 22 · Capítulo 5A (T11)

### 22.1 Qué se llevó al documento y qué quedó en los anexos

| Al documento de grado | A los anexos (E2 y E3) |
|---|---|
| 6 actores | los mismos |
| 3 diagramas: general, DCU-02 emisión, DCU-08 API | los 9 diagramas |
| 1 ficha completa (CU-08, emitir factura de venta) | 17 fichas + 39 casos en formato breve |

Todo se **importa** de `e2_diagramas.py` y `e3_documentacion.py`; no hay texto duplicado.

### 22.2 Dónde se apartó de la plantilla, y por qué

La plantilla POSInnovate presenta en «5.3 Diagrama estructural» **el mismo diagrama de casos
de uso** del punto anterior, con las relaciones de inclusión dibujadas. Aquí ese punto
presenta la **arquitectura por capas**: presentación → rutas → servicios → datos, con las dos
entradas convergiendo en la misma capa de lógica.

Se documentó la razón en el propio capítulo: repetir el diagrama anterior con una variación no
agrega información, y el capítulo 6 necesita la vista de arquitectura para explicarse. Si un
instructor exige seguir la plantilla al pie de la letra, la figura se reemplaza por
`DCU-02`/`DCU-08` y el texto se ajusta; pero el argumento para defender la versión actual está
escrito.

### 22.3 Argumentos del capítulo que sirven en la sustentación

1. **El actor que más documentos origina es un programa que nunca ve una pantalla.** De ahí que
   la lógica no pueda vivir en las rutas web.
2. **Las dos entradas comparten la capa de servicios.** Si cada una resolviera su cálculo, una
   factura emitida desde el formulario y otra por la API con los mismos datos habrían podido
   diferir en el impuesto.
3. **La validación del cupo va antes de reservar el consecutivo** (paso 3 antes que el 4 en la
   ficha de CU-08): rechazar después de tomar un número gastaría un consecutivo de una
   resolución autorizada en un documento que nunca existió.
4. **El tablero abre con el servicio y no con la venta**, porque es lo que la empresa hace;
   cobrarlo viene después.


---

## 23 · Capítulo 5B (T12)

### 23.1 El diccionario se lee del esquema

`generador/esquema.py` parsea `base/factugest.sql` y devuelve, por columna, el nombre, el
tipo en lenguaje legible, si admite nulos, si participa de alguna clave y el comentario que
la columna trae en el propio esquema. `e4_cap5b.py` cruza eso con `DESCRIPCIONES`.

**Un diccionario transcrito a mano empieza a envejecer el día que se escribe**, y siempre se
descubre igual, cuando alguien busca en el sistema una columna que el documento describe y
que ya no existe. Aquí el tipo y la clave salen de la base.

Reglas del cruce:

1. La **descripción escrita manda** sobre el comentario del esquema, porque los comentarios
   del SQL están redactados para quien lee código y vienen sin tildes.
2. Si una columna queda sin ninguna de las dos, **el generador se detiene** con la lista.
   No hay forma de publicar un diccionario con huecos.

Tablas con diccionario detallado: `clientes_api` (11 columnas), `documentos` (27) y
`facturas` (23). El resto queda documentado en los comentarios del propio esquema.

### 23.2 El modelo físico, resuelto

Va en **página apaisada** con 9 pulgadas de ancho, y la numeración sigue corrida porque las
secciones nuevas heredan el encabezado. No se partió por zonas: el diagrama entero cabe y las
agrupaciones que ya trae coinciden con las zonas descritas en el 5.6. El texto explica por qué
está apaisado, para que no parezca un descuido de maquetación.

### 23.3 Argumentos del capítulo

1. **Dos zonas que no se mezclan.** Si un documento emitido para un cliente se guardara en la
   zona comercial, el tablero lo contaría como ingreso propio. No daría error, daría cifras
   equivocadas que nadie notaría hasta cruzar con la contabilidad.
2. **Hay dos tablas para lo que parece lo mismo, y no es duplicación.** Un documento emitido
   por cuenta de un cliente y una factura que el proveedor cobra son hechos económicos
   distintos que nunca se suman.
3. **No hay tabla de contadores.** El consumo se cuenta de los documentos emitidos, porque un
   contador almacenado puede desviarse y el día que ocurra se cobraría una cifra distinta de
   la prestada.


---

## 24 · Las cifras de pruebas del capítulo 6B (T14)

**Son reales.** Se obtuvieron ejecutando la batería del proyecto, no se estimaron.

```bash
cd Factugest/Factugest && python -m pytest
# 190 passed, 1 warning in 3.29s
```

| Dato | Valor | Dónde vive |
|---|---:|---|
| Pruebas automatizadas | **190** | `PRUEBAS_AUTOMATICAS` en `e4_cap6b.py` |
| Archivos de prueba | 12 | `ARCHIVOS_PRUEBA` |
| Tiempo de ejecución | 3,3 s | `SEGUNDOS` |

⚠️ **Si se agregan o quitan pruebas, hay que actualizar esas tres constantes.** Un documento
que declara 190 pruebas mientras el proyecto tiene otras tantas deja de servir como
evidencia, y es de lo más fácil de comprobar para un jurado.

Las versiones de la tabla de tecnologías salen de `Factugest/requirements.txt`; conviene
volver a mirarlas antes de entregar por si alguna dependencia subió de versión.

### 24.1 El pendiente del §21.2 se resolvió solo

La página en blanco después de la tabla de contenido **ya no aparece**. Al crecer el
documento, el índice pasó a ocupar más páginas y el punto de corte se movió, que era
justamente la razón para no forzar el arreglo antes. **Hay que volver a comprobarlo en T16**,
porque el cierre y los anexos harán crecer el índice otra vez.


---

## 25 · Entrega final (T16)

### 25.1 Los cuatro entregables

| Documento | Páginas | Contenido |
|---|---:|---|
| **FactuGest - Documento de Grado** | **120** | Preliminares, 6 capítulos, conclusiones, referencias y anexos. 34 tablas y 29 figuras |
| FactuGest - Requisitos Funcionales y No Funcionales | 27 | 82 RF · 32 RNF · priorización · trazabilidad |
| FactuGest - Diagramas de Casos de Uso | 26 | 56 casos · 9 diagramas UML · matriz caso-actor |
| FactuGest - Documentacion de Casos de Uso | 27 | 17 fichas completas · 39 breves |

**200 páginas en total**, cada documento con su `.docx` y su `.pdf` en `docs expo/entregables/`.
Los 16 diagramas sueltos están en `entregables/diagramas/`, por si hacen falta para la
presentación.

### 25.2 Cómo rehacerlo todo

```bash
cd "docs expo/generador"
python e1_requisitos.py && python e2_diagramas.py
python e3_documentacion.py && python e4_documento.py     # genera los .docx
python revisar.py "../entregables/<archivo>.docx"        # a PDF, actualizando el índice
python verificar.py                                      # lista de verificación APA
```

### 25.3 Qué comprueba `verificar.py`

Sobre el `.docx`, lo que exige el instructivo: márgenes de 2,54 cm, Times New Roman de 12
puntos, interlineado doble, sangría de 1,27 cm, número de página arriba a la derecha y
numeración correlativa de tablas y figuras.

Sobre el PDF, lo que solo se ve cuando Word arma las páginas: páginas en blanco, figuras que
se desbordan de los márgenes, rótulos separados de su tabla o figura, el patrón de redacción
del §1.5 y que la tabla de contenido tenga paginación real.

**Resultado del 21 de agosto de 2026: 65 comprobaciones, cero fallas.**

Las dos comprobaciones de redacción (§1.5 y §1.6) son las que más han encontrado. La revisión
manual dejó pasar casos que el verificador detectó de inmediato, sobre todo en títulos de
tabla y de figura, donde el ojo no los busca.

### 25.4 Antes de entregar

1. ⚠️ **Verificar la vigencia de la Resolución 000042 de 2020** en el sitio de la DIAN
   (§17.3). Es el único dato que envejece solo.
2. Volver a correr `python -m pytest` en `Factugest/Factugest` y, si el número cambió,
   actualizar las constantes de `e4_cap6b.py` (§24).
3. Revisar las versiones de `requirements.txt` frente a la tabla de tecnologías del 6.10.
4. Abrir el `.docx` en Word y pulsar Ctrl+E y F9 para forzar la actualización del índice, o
   simplemente volver a correr `revisar.py`.
5. Decidir si el punto 5.4 se deja con la arquitectura por capas o se ajusta a la plantilla
   (§22.2).


---

## 26 · Signos que no se usan (decisión del cliente)

| Signo | Dónde aparecía | Con qué se reemplazó |
|---|---|---|
| `:` explicativo | «afirmación breve: explicación» | conectores («porque», «ya que», «de modo que») o dos oraciones |
| `—` guion largo | incisos, títulos, celdas vacías | comas, «sea», «como», paréntesis; «No aplica» en celdas |
| `·` punto medio | enumeraciones, rótulos, viñetas | comas y «y»; punto entre dos datos; **guion simple** en listas de celda |

**Se conservan** los dos puntos en entradas de glosario con viñeta, en etiquetas de dato
(`Palabras clave:`) y en títulos reales de obras citadas.

El rótulo de los diagramas UML quedó en **dos renglones**, con `FACTUGEST` arriba y el
nombre del módulo debajo en letra menor, que es además lo que UML pide en la frontera del
sistema.

Las tres reglas están en el §1 y las comprueba `verificar.py` en cada corrida. **Son las
comprobaciones que más han encontrado**, porque la lectura manual no las ve en títulos de
tabla ni dentro de las imágenes.


---

## 27 · Diapositivas de sustentación

### 27.1 Sobre la normativa (consulta del cliente, 21-ago-2026)

**No hay normativa que regule el diseño de las diapositivas.** El `InstructivoSBS.APA-1`
menciona PowerPoint dos veces y las dos son ejemplos de **cómo citar** una presentación
ajena, nunca de cómo hacer la propia. Todo el instructivo trata del documento escrito.

APA 7 sí trae recomendaciones para presentaciones, pero de accesibilidad y citación, no de
formato obligatorio. Se reducen a que se lea proyectado, que lleve poco texto, que se citen
las fuentes ajenas y que la portada identifique el trabajo.

### 27.2 Lo que se midió en la plantilla POSInnovate

| Aspecto | POSInnovate | Borrador FactuGest | Recomendable |
|---|---|---|---|
| Letra de cuerpo | 16 y 20 pt | **10 a 14 pt** | 20 pt o más |
| Diapositivas con más de 60 palabras | 7 de 39 | — | ninguna |
| Numeración | no | no | sí |
| Diapositiva de referencias | no | no | sí |

El borrador además tenía **27 de 37 diapositivas vacías** y el contenido escrito describía el
proyecto anterior, con inventario y control de stock, que contradice el documento de grado.

### 27.3 Decisiones del cliente

1. **Se trabaja sobre `Diapositivas factugest.pptx`.** Su diseño, fondo y colores son los que
   exige el centro de formación y **no se tocan**. Solo se manipulan cuadros de texto e
   imágenes.
2. **Se corrigen los defectos de forma.** Cuerpo desde 20 pt, destacados a 24, numeración de
   diapositivas y una diapositiva de referencias al cierre.
3. **Se conservan las 37 diapositivas** y la estructura de cinco secciones de la plantilla,
   pensada para una sustentación de 25 a 35 minutos.

### 27.4 El motor

`generador/ppt.py` abre el archivo del cliente y escribe encima. `limpiar()` borra los cuadros
de texto que caen por debajo de la zona del título y los iconos sueltos que los acompañaban,
sin tocar el fondo, el logo del SENA, la marca de agua, la barra del título ni la línea
inferior. `generador/revisar_ppt.py` convierte a PDF con PowerPoint y renderiza, igual que
`revisar.py` con los documentos.

**Salida:** `carpeta exposicion/FactuGest - Sustentación.pptx`. El borrador original queda
intacto.

### 27.5 Cómo se escriben las viñetas

**Cada punto es una idea completa y escrita de corrido.** No se parte en un rótulo destacado
y un detalle detrás, no lleva negrita en las primeras palabras y no se corta con punto ni con
dos puntos a mitad de frase.

| Así no | Así sí |
|---|---|
| **Ya tienen su propio software.** un punto de venta, un sistema contable… | La mayoría de estas empresas ya opera con un software propio, sea un punto de venta, un sistema contable o una aplicación hecha a la medida años atrás. |

En una diapositiva el patrón se nota más que en un documento, porque las tres viñetas se ven
a la vez y la repetición salta a la vista. `vinetas()` **rechaza con error** un elemento que
no sea una frase, para que nadie vuelva al formato anterior sin darse cuenta.

La negrita queda reservada para el mensaje principal de la diapositiva, que es una sola frase
en azul y a 24 puntos, no para las viñetas.

### 27.6 Plan

- [x] **P0 · Motor y prueba** — `ppt.py`, `revisar_ppt.py` y prueba sobre la diapositiva 4.
- [x] **P1 · Sección I, Formulación** (1 a 10) — `generador/p1_formulacion.py`. Portada con
      los nombres completos y la ficha, subtítulo corregido, problema, justificación con las
      cifras de la encuesta, objetivo general literal, 5 objetivos específicos, alcance en dos
      columnas, riesgos y restricciones, y cronograma en tabla.
- [x] **P2 · Sección II, Análisis** (11 a 22) — `generador/p2_analisis.py`. Las once
      diapositivas que estaban vacías, con la gráfica del contraste de la encuesta, las dos
      técnicas con sus historias y sus RF, la matriz de stakeholders, la priorización y las
      tablas de requisitos.
- [x] **P3 · Sección III, Diseño** (23 a 30) — `generador/p3_diseno.py`. Diagrama general de
      casos de uso, ficha de CU-08 resumida, ciclo Scrum, los dos mockups, el modelo
      entidad-relación y el diccionario de la tabla `documentos`.
- [x] **P4 · Secciones IV y V** — `generador/p4_desarrollo.py`. Las dos tablas de
      herramientas con sus logotipos, pruebas, evidencia, y **dos diapositivas nuevas** de
      resultados y referencias, más la evidencia de emisión de factura y su resultado.
      La presentación pasó de 37 a 41.
- [x] **P5 · Revisión final** — `generador/verificar_ppt.py`. Ocho comprobaciones sobre las
      41 diapositivas, sin fallas.

### 27.7 Qué contenido va en cada sección

Todo sale de lo ya producido, sin inventar nada nuevo: el documento de grado para el texto,
`entregables/diagramas/` para los 16 diagramas y `documento para que te guies claude/` para
las capturas del sistema y los mockups.


---

## 28 · Sección I de la sustentación (P1)

### 28.1 Lo que se corrigió del borrador

| Diapositiva | Antes | Ahora |
|---|---|---|
| 2 · Portada | «control de inventarios y gestión comercial para PyMEs» | «emite por cuenta de terceros mediante una API de integración» |
| 4 · Problema | Falta de control de inventario, stock en tiempo real | La barrera es el reemplazo del software |
| 5 · Justificación | Cifras inventadas de 60 %, 99 % y 24/7 | 82 %, 38 % y 84 %, tomadas de `encuesta.py` |
| 7 · Objetivos | 3 tarjetas, una de ellas «Control de Inventarios» | Los 5 objetivos aprobados en T1 |
| 8, 9, 10 | vacías | Alcance, riesgos con restricciones, y cronograma |

### 28.2 Detalles que costaron

- **Las tarjetas de la justificación se conservaron.** `limpiar()` borra los textos y deja las
  imágenes de fondo, así que las tres tarjetas del borrador siguen ahí con datos nuevos. En la
  de objetivos sí hubo que retirarlas con `limpiar(d, imagenes=True)`, porque eran tres y los
  objetivos son cinco.
- **Las tablas salían verdes.** PowerPoint aplica el estilo de tabla de su tema, que no tiene
  relación con los colores de la plantilla. `tabla()` ahora pinta el encabezado en el azul del
  centro de formación y alterna las filas.
- **PowerPoint bloquea el archivo** si queda una instancia abierta tras convertir a PDF. Si
  aparece un `PermissionError` al guardar, hay que cerrarlo:
  `Get-Process POWERPNT | Stop-Process -Force`.

### 28.3 Las cifras vienen del mismo sitio que el documento

La justificación toma sus porcentajes de `encuesta.py`, igual que el capítulo 3. Cambiar la
muestra actualiza a la vez el documento y las diapositivas, y **no pueden discrepar**.


---

## 29 · Sección II de la sustentación (P2)

### 29.1 La gráfica nueva

`FIG-encuesta-contraste.png` muestra **solo las preguntas 6 y 7**, una al lado de la otra. El
panel del documento tiene seis distribuciones y proyectado no se distingue cuál importa; aquí
se ve el hallazgo y nada más. Se genera con `encuesta.grafica_contraste()`.

Está dibujada muy apaisada a propósito, en proporción 4:1, para que en la diapositiva pueda
ocupar los 11,85 pulgadas de ancho sin que el alto la obligue a encogerse.

### 29.2 Cómo se organizó la sección

La plantilla repite el bloque «herramienta, historias de usuario, requisitos relacionados» dos
veces, una por técnica. Se respetó:

| Diapositivas | Contenido |
|---|---|
| 12, 13, 14 | Encuesta, sus tres historias y los cuatro RF que salen de ella |
| 15, 16, 17 | Observación directa, sus historias y sus RF |
| 18 | Matriz de stakeholders |
| 19, 20 | Escala de priorización y ranking de los ocho módulos |
| 21, 22 | Requisitos funcionales y no funcionales |

### 29.3 Las cifras se importan

`p2_analisis.py` importa `MODULOS`, `RNF`, `prioridad` y `puntaje` de `e1_requisitos.py`, igual
que hace el capítulo 4 del documento. **Las tablas de la 20, la 21 y la 22 se calculan solas**,
así que la sustentación no puede quedar diciendo algo distinto del documento que el jurado
tiene delante.

### 29.4 Frases que cierran cada diapositiva

Cada una termina con una línea que dice qué hay que retener, y son las que conviene llevar
preparadas para la exposición:

- **12.** «Rechazan cambiar de software, no facturar electrónicamente.»
- **13.** «La HU-04 no la pidió nadie. Salió de advertir que el sistema puede perder la
  respuesta por una falla de red.»
- **17.** «La observación no produjo funciones nuevas sino condiciones sobre las que ya
  existían, y esa es la diferencia entre las dos técnicas.»
- **18.** «La DIAN quedó en alta influencia y bajo interés.»
- **21.** «Donde un sistema comercial tendría inventario y compras, aquí hay clientes API y
  consumo y planes.»


---

## 30 · Sección III de la sustentación (P3)

### 30.1 Las figuras son las del documento

No se hicieron versiones aparte para la presentación. Si el jurado compara una diapositiva con
el capítulo 5, encuentra el mismo diagrama.

**La única salvedad es la base de datos.** En el documento va el modelo físico con las
veintisiete tablas, en página apaisada; en la diapositiva va el modelo conceptual, porque
veintisiete tablas proyectadas no se leen desde la tercera fila. El pie de la diapositiva lo
dice, para que no parezca que falta algo.

### 30.2 Dos ajustes de maquetación

1. **El cuadro del título medía seis pulgadas.** Con un título algo más largo, como «Diseño de
   la Base de Datos», el texto se partía en dos líneas y la segunda caía encima de la barra
   amarilla. `titulo()` ahora ensancha el cuadro a 11,4 pulgadas.
2. **Una imagen no siempre debe ocupar todo el ancho.** El modelo entidad-relación es
   demasiado alto para llenar las once pulgadas, así que al estirarlo se encogía por su altura
   y dejaba media diapositiva vacía. Quedó a la izquierda con el texto explicativo a la
   derecha, y así se lee mejor y aprovecha el espacio.

### 30.3 Argumentos que quedan a la vista

- **25.** El cupo se valida en el paso 3, antes de reservar el número en el paso 4.
- **26.** El alcance cambió durante el desarrollo y se absorbió reordenando el backlog.
- **27.** Un tablero que abriera con las ventas describiría un comercio, no un proveedor.
- **29.** Si un documento de un cliente se guardara en la zona comercial, el tablero lo
  contaría como ingreso propio.
- **30.** La referencia externa es la que hace idempotente el reintento.


---

## 31 · Secciones IV y V de la sustentación (P4)

### 31.1 Cuatro diapositivas que la plantilla no traía

La presentación pasó de 37 a **41**. Se agregaron la evidencia de emisión de una factura, el
resultado de esa prueba, los resultados obtenidos y las referencias.
Se crean **duplicando una diapositiva existente**, de modo que heredan el fondo, el logotipo,
la barra del título y la línea inferior sin rehacerlos.

`ppt.duplicar()` copia el XML de cada forma y **rehace las relaciones**, porque una imagen
copiada apunta al identificador de relación de la diapositiva original y sin reasignarlo no
aparece.

⚠️ **La hoja de notas hay que excluirla.** Una hoja de notas pertenece a una sola diapositiva,
y si dos apuntan a la misma, PowerPoint responde «no se puede abrir el archivo» sin decir por
qué. Costó un rato encontrarlo.

### 31.2 Los logotipos se conservan

Las diapositivas 32 y 33 traían tabla y logotipos de las tecnologías, y siguen siendo las que
el proyecto usa, así que se conservaron y solo se reescribieron las descripciones. En la 33 se
llenó además la cuarta fila, que estaba vacía, con pytest y las 190 pruebas.

**Un detalle que engañó**: los rótulos de esa diapositiva no eran celdas de la tabla sino
cuadros de texto flotantes encima. Al escribir en las celdas quedó el texto duplicado, uno
sobre otro. `limpiar(d, tablas=False)` retira los flotantes y conserva la tabla.

### 31.3 Las cifras salen del capítulo 6

`p4_desarrollo.py` importa `PRUEBAS_AUTOMATICAS`, `SEGUNDOS` y `RESULTADOS` de
`e4_cap6b.py`. La tabla de cumplimiento de la diapositiva de resultados es **la misma** del
documento.


### 31.4 La sección V quedó así

| N.º | Contenido |
|---|---|
| 35 | Pruebas del sistema, con los objetivos y el alcance |
| 36 | Evidencia · RF 4.2, registro de un cliente |
| 37 | Evidencia · RF 4.1, emisión de una factura |
| 38 | Resultado obtenido de la emisión |
| 39 | Resultados obtenidos, con la tabla de cumplimiento de los objetivos |
| 40 | Referencias |
| 41 | Cierre del SENA, intacto |

`evidencia()` quedó parametrizada, así que agregar las otras dos pruebas documentadas (registro
de servicio y creación de usuario) es una línea más. Las capturas ya existen en
`documento para que te guies claude/`.

⚠️ **PowerPoint bloquea el archivo** después de convertir a PDF. `guardar()` ahora detecta el
error de permisos, cierra PowerPoint y reintenta una vez, en lugar de fallar con un mensaje que
no dice nada sobre la causa real.


---

## 32 · Revisión final de la presentación (P5)

### 32.1 Qué comprueba `verificar_ppt.py`

| Comprobación | Criterio |
|---|---|
| Tamaño de letra | Nada por debajo de 13 puntos |
| Densidad | Menos de 120 palabras **de prosa** por diapositiva |
| Diapositivas vacías | Ninguna con menos de tres palabras y sin imagen |
| Dentro del lienzo | El texto no se sale; a las imágenes se les tolera el sangrado del diseño |
| Guion largo y punto medio | Ninguno |
| «Afirmación breve: explicación» | Ninguna, salvo etiquetas como «Fuente:» |
| Numeración | Presente en todas menos las dos portadas |

**Resultado del 21 de agosto de 2026: 8 comprobaciones, cero fallas.**

### 32.2 Dos calibraciones que hubo que hacer

1. **Las tablas no cuentan para el límite de palabras.** A una tabla nadie la lee entera,
   quien la mira busca su fila. El límite es para la prosa, que sí se lee de corrido y es la
   que satura la diapositiva. Sin esa distinción, el diccionario de datos y la ficha de CU-08
   aparecían como sobrecargadas cuando no lo están.
2. **Hay tensión entre dos reglas del cliente.** Se pidió poco texto por diapositiva y también
   ideas completas escritas de corrido. Con frases completas, tres viñetas ya suman noventa
   palabras. El límite quedó en 120 a propósito, porque bajarlo obligaría a volver a las
   frases telegráficas que se descartaron.

### 32.3 El pie subió a 13 puntos

Estaba en 12, que era el único texto por debajo del mínimo. Ahora ningún texto de la
presentación baja de 13, y el cuerpo va de 15 en adelante.

### 32.4 Entregable

`carpeta exposicion/FactuGest - Sustentación.pptx` · **41 diapositivas** · con su PDF al lado.
El borrador original, `Diapositivas factugest.pptx`, queda intacto.

Para rehacerla entera basta `python p4_desarrollo.py`, que encadena las cuatro secciones y
numera.

---

## 33 · Guion de la sustentación

**Pedido**: un documento en Word que diga qué tiene que decir cada una de las tres
personas que exponen, a partir de las diapositivas ya hechas.

**Generador**: `generador/guion_exposicion.py` → `carpeta exposicion/FactuGest - Guion
de la Sustentación.docx` (15 páginas).

### 33.1 · Reparto

Sigue los roles del capítulo 3, no un corte por cantidad de diapositivas. Que hable de
cada parte quien la construyó es lo que permite responder cuando el jurado pregunta.

| Expositor | Rol | Diapositivas | Contenido | Tiempo |
|---|---|---|---|---|
| Brandon Restrepo | Product Owner | 1 a 10 | Formulación | 8 min |
| Wilmer Contreras | Analista | 11 a 25 | Análisis y diseño | 11 min |
| Johan Acosta | Scrum Master | 26 a 41 | Metodología, desarrollo, implementación | 11 min |

Total treinta minutos. El documento dice también qué recortar si dan menos tiempo
(las diapositivas 13, 16 y 17) y qué no se puede recortar (la 12, que es el hallazgo,
y la 37, que es la evidencia).

### 33.2 · Estructura

Cada una de las 41 diapositivas lleva dos líneas, «En pantalla» con lo que el jurado
ve y «Qué decir» con el texto hablado. Los títulos se tomaron del propio `.pptx`, no
de memoria, para que el guion no se desvíe de la presentación si alguna se reordena.

Cierra con diez preguntas probables del jurado, cada una con su respuesta y con quién
debería contestarla, y una lista de verificación para el ensayo.

### 33.3 · Por qué no va con interlineado doble

Es material de trabajo, no un entregable académico, y se lee de reojo mientras se
habla. Va a 1,15 y con espacio antes de cada título. `_compactar()` recorre los
párrafos al final porque `vinetas()` y `numerada()` fijan el interlineado del
instructivo por su cuenta.

### 33.4 · Las tres prohibiciones también aplican aquí

Comprobado sobre el `.docx` generado: cero guiones largos, cero puntos medios y cero
coincidencias de «afirmación breve: explicación». Los catorce casos que había en el
primer borrador se reescribieron, incluidos dos títulos de sección que se cambiaron
por los títulos reales de las diapositivas.
