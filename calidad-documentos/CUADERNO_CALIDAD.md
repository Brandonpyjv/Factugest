# Cuaderno de trabajo — Competencia «Controlar la calidad del software»

Control de la elaboración de las dos evidencias de la guía GFPI-F-135, ficha **3115426**,
programa Análisis y Desarrollo de Software (228118), fase de **Evaluación**.

**Creado:** 8 de septiembre de 2026
**Estado global:** **AA1 terminado**, 59 páginas en PDF. Cerradas C0 a C8, faltan 5
tareas, todas de la infografía. Sigue C9, el contenido del mapa.

Insumos leídos:

- `GFPI-F-135_GUIA_APRENDIZAJE_CONTROLAR LA CALIDAD DEL SW_3115426.pdf` (6 páginas)
- `MODELO Y ESTANDARES DE LA CALIDAD DEL SW.pdf` (22 páginas, material FAVA SENA)
- El repositorio, `CLAUDE.md`, `SEGURIDAD.md`, `BASE_DE_DATOS.md`, `NEXT_STEPS.md` y el
  cuaderno del documento de grado (`docs expo/CUADERNO_DE_TRABAJO.md`)

---

## 1 · Regla de operación

Se hereda la del documento de grado, porque funcionó y porque los dos entregables salen
del mismo motor de formato.

1. **Una tarea a la vez.** Al terminar cada una se reporta qué quedó y se pide permiso
   para seguir. El motivo es el presupuesto de tokens, no la formalidad.
2. **Al cerrar una tarea se actualiza este cuaderno**, la casilla y la bitácora (§10).
3. **Lo que se escribe tiene que existir en el software.** Ninguna prueba inventada,
   ninguna cifra redondeada hacia arriba. Si una prueba está planificada y no ejecutada,
   el informe lo dice con esas palabras, que además es exactamente lo que la guía permite
   («Pruebas Ejecutadas o Planificadas»).
4. **Estilo:** nada de «afirmación breve: explicación», nada de guion largo, nada de punto
   medio en el texto de los entregables. Se comprueba con el mismo verificador del
   documento de grado.
5. **Normativa APA 7** con el mismo motor `docs expo/generador/apa.py`.

---

## 2 · Qué pide la guía, en concreto

### 2.1 AA1-EV01 · Informe de métodos y estándar de calidad

Evidencia **de desempeño**. Se evalúa por observación directa con lista de chequeo, y el
criterio de evaluación textual es que el aprendiz *«elabora informe de métodos, estándares
de calidad y pruebas aplicadas al proyecto productivo»*. Son tres cosas dentro de un solo
archivo, y el peso está en la tercera, que es lo que confirmó la instructora al decir
«informe de pruebas de su proyecto productivo».

Del cuerpo de la guía salen cuatro exigencias:

| # | Exigencia literal | Cómo se cubre |
|---|---|---|
| 1 | «Análisis de los marcos de calidad que aplicarán a su propio sistema de información» | Capítulo de modelos y estándares, comparados y **elegidos** para FactuGest |
| 2 | «Detallando los estándares seleccionados» | Adopción justificada, con la matriz de requisitos no funcionales contra el estándar |
| 3 | «Y el plan de pruebas utilizado para validar su correcto funcionamiento» | Plan de pruebas formal, con estrategia, niveles, entorno y criterios |
| 4 | «Tipos de pruebas ejecutadas o planificadas» | Catálogo por tipo, con casos, resultados reales y evidencias |

Formato PDF, extensión libre.

### 2.2 AA2-EV01 · Infografía, mapa conceptual de modelos para el aseguramiento

Evidencia **de producto**. Se evalúa por valoración del producto con lista de chequeo, y el
criterio es que el aprendiz *«ajusta procesos del desarrollo de software de acuerdo con el
referente de calidad adoptado»*.

La guía lo llama «infografía» en el nombre de la evidencia y «mapa conceptual» en el
enunciado y en los lineamientos. La instructora dijo «la infografía basada en el pdf», así
que el producto es **un mapa conceptual con tratamiento gráfico de infografía**, cuyo
contenido sale del material del SENA y no de internet. Formato PDF, extensión libre.

**Ojo con el criterio de evaluación**, porque habla de ajustar procesos de acuerdo con el
referente adoptado. Un mapa puramente teórico cumple el enunciado pero se queda corto ante
ese criterio, así que el mapa cierra con una franja que aterriza el referente adoptado en
FactuGest. Es lo que amarra AA2 con AA1 y evita que parezca copiado del PDF.

---

## 3 · De qué está hecho el material del SENA

El mapa de AA2 y el capítulo teórico de AA1 salen de aquí, así que queda escrita la
estructura del PDF para no tener que releerlo cada sesión.

```
Calidad del software
├── Definiciones, calidad, calidad de software, modelo y estándar
├── MODELOS
│   ├── Producto ── McCall (1977), 3 ejes, 11 factores, criterios y métricas
│   │             └ Boehm (1978), alto nivel, intermedio (7 factores) y primitivo
│   └── Proceso  ── CMMI (SEI, 2000), 5 niveles de madurez
│                   (menciona CMM, ISO 9001, TickIT, Bootstrap, PSP, TSP, PSM, Six Sigma)
└── ESTÁNDARES
    ├── Producto ── ISO/IEC 9126 (2001), 6 características internas y externas
    │             ├ ISO/IEC 25000:2005 SQuaRE, 5 divisiones (2500n a 2504n)
    │             └ ISO/IEC 25010:2011, producto con 8 características y 31
    │               subcaracterísticas, calidad en uso con 5 y 9
    └── Proceso  ── ISO/IEC 15504 SPICE, evaluación, mejora y determinación de
                  │  capacidad, alineado con ISO 12207, 9 documentos
                  └ ISO 9001:2015, familia ISO 9000 de gestión de la calidad
```

Los tres ejes de McCall son operación, revisión y transición del producto. Los cinco
niveles de CMMI son inicial, gestionado, definido, gestión cuantitativa y en optimización.
Esas dos listas son las que la lista de chequeo va a buscar primero.

---

## 4 · Con qué evidencia real contamos

Esto es lo que hace que el informe sea de FactuGest y no una monografía. Todo verificado
el 8 de septiembre de 2026. El reparto por archivo sale de la corrida guardada y no de
contar las funciones de cada archivo, porque una prueba parametrizada vale por varias y
contarla como una sola dejaba el informe corto en 32 pruebas.

| Insumo | Estado | Dónde |
|---|---|---|
| **190 pruebas automatizadas, todas en verde** | Verificado corriendo `python -m pytest` | `Factugest/tests/`, 12 archivos |
| Validaciones de entrada | 45 pruebas | `test_validaciones.py` |
| Proveedor DIAN | 24 pruebas | `test_dian_proveedor.py` |
| Contrato Pydantic de la API | 22 pruebas | `test_modelos_api.py` |
| Aritmética tributaria y notas | 35 pruebas | `test_calculo_documento.py`, `test_calculo_notas.py` |
| PDF, membrete y descuentos | 16 pruebas | `test_pdf_membrete.py`, `test_pdf_descuentos.py` |
| Monograma, llaves API, consumo, XML y canónico | 48 pruebas | los cinco archivos restantes |
| Colección de pruebas de la API | Existe | `Factugest/docs/FactuGest.postman_collection.json` |
| Sembrador que se verifica a sí mismo | Existe, con `verificar()` | `Factugest/seed_proveedor.py` |
| Evidencias funcionales en pantalla | 8 capturas, antes y después | `docs expo/documento para que te guies claude/registro *.png` |
| 32 requisitos no funcionales **con columna de verificación** | Existen | `docs expo/generador/e1_requisitos.py`, líneas 375 a 492 |
| Documento de seguridad | 522 líneas | `SEGURIDAD.md` |
| Encuesta a empresas | Instrumento y resultados | `docs expo/`, capítulo 3 del documento de grado |

Las categorías de esos 32 requisitos no funcionales ya son, sin retocarlas, un modelo de
calidad de producto, pues cubren rendimiento, seguridad, integridad de los datos,
trazabilidad, disponibilidad, usabilidad, compatibilidad, cumplimiento normativo,
mantenibilidad, escalabilidad y portabilidad. Mapearlas contra las ocho características de
ISO/IEC 25010 es media hora de trabajo y es la sección que más fuerte va a leerse en el
informe, porque demuestra que el estándar se aplicó al proyecto y no que se citó.

**Lo que no tenemos y hay que declarar como planificado** son las pruebas de rendimiento
medidas, las pruebas de seguridad con herramienta y la validación real contra la DIAN, que
está pendiente del proveedor tecnológico (`FACTUS.md`).

---

## 5 · Decisiones

Las tres primeras quedaron **aprobadas el 8 de septiembre de 2026, opción A en las tres**.
Se dejan las opciones descartadas escritas porque el motivo del descarte es lo que se
responde si en la sustentación preguntan por qué ese estándar y no otro.

### D1 · Alcance del informe AA1 — **aprobada la opción A**

| Opción | En qué consiste | Riesgo |
|---|---|---|
| **A. Estándar adoptado y pruebas reales** (recomendada) | Teoría comparativa breve, de 4 a 5 páginas, adopción justificada de ISO/IEC 25010 en producto y CMMI nivel 2 como referente de proceso, y el grueso en el plan de pruebas con las 190 pruebas reales, la matriz de requisitos y las evidencias. Entre 25 y 30 páginas | Ninguno visible, cubre el enunciado y el criterio de evaluación |
| B. Informe de pruebas puro | Solo plan y ejecución de pruebas, con una página de estándares | Incumple «análisis de los marcos de calidad» y «estándares seleccionados», que están en el enunciado aunque la instructora lo resumiera |
| C. Monografía comparativa completa | Los siete modelos y estándares desarrollados a fondo y luego la aplicación | Se vuelve un resumen del PDF del SENA, y la evidencia es de **desempeño**, o sea que se evalúa lo que el equipo hace, no lo que transcribe |

### D2 · Qué estándar se adopta — **aprobada la opción A**

| Opción | Combinación | Comentario |
|---|---|---|
| **A. ISO/IEC 25010 más CMMI nivel 2** (recomendada) | Producto con el estándar vigente, proceso con el modelo más reconocido | La 25010 es la sucesora de la 9126 y es contra la que ya se pueden mapear los 32 requisitos. CMMI nivel 2 es defendible para un equipo de formación, sin prometer una certificación |
| B. ISO/IEC 9126 más ISO 9001:2015 | Estándar anterior y gestión de calidad organizacional | La 9126 está reemplazada desde 2011 y el jurado lo puede señalar. La 9001 es de la organización, no del software |
| C. ISO/IEC 25010 más ISO/IEC 15504 SPICE | Producto y evaluación de procesos | SPICE exige un marco de evaluación por niveles de capacidad que no vamos a ejecutar de verdad |

### D3 · Herramienta para la infografía AA2 — **aprobada la opción A**

| Opción | Cómo | Ventaja | Desventaja |
|---|---|---|---|
| **A. Dibujada por código con matplotlib** (recomendada) | Un script en `generador/`, igual que `uml.py` y `diagramas_proceso.py` | Sale con la misma tinta y tipografía que los diagramas del documento de grado, se rehace en segundos si hay que corregir y exporta PDF vectorial | El ajuste fino de posiciones es iterativo |
| B. Lienzo de diseño publicado como artefacto | Se diseña visualmente y se exporta a PDF | Se ajusta a mano, arrastrando cajas | Rompe la coherencia visual con el resto de los entregables |
| C. Diapositiva única en PowerPoint | Con `python-pptx`, ya usado en `ppt.py` | Editable por cualquiera del equipo | Una diapositiva apaisada exportada a PDF se ve como diapositiva, no como infografía |

### D4 · Datos de portada — **resueltos el 8 de septiembre de 2026**

Los mismos del documento de grado, así que no se reescriben aquí. `comun.py` los importa
de `docs expo/generador/e4_preliminares.py`, que es donde ya estaban, y de ese modo un
cambio de nombre se hace en un solo archivo.

| Dato | Valor |
|---|---|
| Integrantes | Brandon Arley Restrepo Gélvez, Johan Sebastián Acosta Sánchez, Wilmer Jesús Contreras Rangel |
| Ficha | 3115426 |
| Programa | Tecnólogo en Análisis y Desarrollo de Software |
| Centro | Centro de la Industria, la Empresa y los Servicios (CIES) |
| Ciudad | Cúcuta, Norte de Santander |
| Instructora que califica | Heidy, la misma del proyecto de grado. **Falta el apellido** |

La guía la firma Jenniffer Yepes Manjarres, pero es su autora, no quien evalúa, así que en
la portada va Heidy. El apellido se completa en `generador/comun.py`, constante
`INSTRUCTORA`, antes de generar el PDF definitivo.

---

## 6 · Estructura propuesta del informe AA1

Sujeta a la decisión D1.

1. **Portada e introducción.** Qué es FactuGest en cinco líneas y para qué es este informe.
2. **Marco de calidad.**
   2.1 Calidad, calidad de software, modelo y estándar, con las definiciones del material.
   2.2 Clasificación por producto y por proceso, con la tabla comparativa.
   2.3 Modelos de producto, McCall y Boehm.
   2.4 Modelo de proceso, CMMI y sus cinco niveles.
   2.5 Estándares, ISO/IEC 9126, 25000 SQuaRE, 25010, 15504 SPICE e ISO 9001:2015.
3. **Estándares seleccionados para FactuGest** y por qué se descartaron los otros.
   3.1 Matriz de las ocho características de ISO/IEC 25010 contra los 32 requisitos no
   funcionales, con la evidencia de cada una.
   3.2 Prácticas de CMMI nivel 2 que el proyecto ya cumple, con el archivo que lo prueba.
4. **Plan de pruebas.** Objetivo, alcance, qué queda fuera, entorno, datos de prueba con el
   sembrador, roles, criterios de entrada y de salida, gestión de defectos y riesgos.
5. **Tipos de pruebas ejecutadas.**
   5.1 Unitarias, las 190, por módulo y con el invariante que protege cada grupo.
   5.2 De integración, la API, la colección Postman y el flujo de emisión completo.
   5.3 Funcionales y de aceptación, con las capturas de antes y después.
   5.4 De usabilidad, con la encuesta.
   5.5 De seguridad, lo ya verificado, contraseñas con bcrypt, cierre de sesión por
   inactividad, bloqueo por rol y llaves de API guardadas como hash.
6. **Tipos de pruebas planificadas.** Rendimiento, seguridad automatizada, regresión
   continua y validación con el proveedor DIAN, cada una con su métrica objetivo.
7. **Resultados, defectos encontrados y corregidos.** Aquí entran los hallazgos reales que
   ya están documentados en `CLAUDE.md`, como el membrete que salía con el emisor
   equivocado o la ciudad del comprador que llegaba vacía. Son defectos detectados y
   corregidos, que es justo lo que una lista de chequeo de calidad quiere ver.
8. **Conclusiones y plan de mejora continua.**
9. **Referencias** en APA 7 y **anexos** con la salida de la corrida de pruebas.

---

## 7 · Plan de tareas

Marcar `[x]` al cerrar. Cada fila es una sesión independiente.

### Fase 0 — Preparación

- [x] **C0 · Cuaderno de trabajo.** Este archivo, con D1, D2 y D3 aprobadas.
- [x] **C1 · Motor de formato.** `generador/comun.py` (portada y datos, reutilizando
      `apa.py` y `e4_preliminares.py` del documento de grado) y `generador/aa1_informe.py`
      (ensamblador que se salta los capítulos que aún no existen). Probado de punta a
      punta, ver §9.

### Fase 1 — Informe AA1

- [x] **C2 · Recolección de evidencia.** `generador/evidencia.py` reúne las cifras y las
      listas que van a citar los capítulos, y `evidencia/` guarda la salida cruda. Detalle
      en §9.
- [x] **C3 · Capítulo de marco de calidad.** Puntos 1 y 2, en `generador/aa1_cap1_marco.py`, con `generador/fuentes.py` para las citas. 13 páginas y 7 tablas, todas las comprobaciones en verde.
- [x] **C4 · Estándares seleccionados y matriz ISO/IEC 25010.** Punto 3, en
      `generador/aa1_cap2_adopcion.py`. Las ocho características quedaron cubiertas y los
      32 requisitos clasificados, con 4 tablas. El informe va en 22 páginas.
- [x] **C5 · Plan de pruebas.** Punto 4, en `generador/aa1_cap3_plan.py`. Objetivo, alcance con lo que queda fuera, ocho niveles y tipos, entorno, datos, criterios de entrada y salida, gestión de defectos por severidad, cinco riesgos y roles. El informe va en 30 páginas y 16 tablas.
- [x] **C6 · Pruebas ejecutadas.** Punto 5, en `generador/aa1_cap4_ejecutadas.py`. 15
      casos con valores reales en una tabla apaisada, las 11 peticiones de integración,
      las 4 operaciones funcionales con dos figuras, 7 verificaciones de seguridad y la
      usabilidad. El informe va en 39 páginas, 21 tablas y 2 figuras.
- [x] **C7 · Pruebas planificadas, resultados y conclusiones.** Puntos 6, 7 y 8, en `generador/aa1_cap5_planificadas.py`. Siete pruebas planificadas con su métrica, los cuatro defectos con su patrón, la cobertura frente al modelo, los seis invariantes, cinco conclusiones y el plan de mejora. 46 páginas y 25 tablas.
- [x] **C8 · Portada, referencias, anexos y armado.** Punto 9, en
      `generador/aa1_cierre.py`. **AA1 terminado: 59 páginas, 28 tablas, 2 figuras, 21
      referencias y las 190 pruebas listadas en el anexo B.** Todas las comprobaciones en
      verde.

> **AA1 listo para entregar.** `entregables/FactuGest - Informe de metodos y estandar de
> calidad.pdf`. Se regenera con `python aa1_informe.py` y se vuelve a exportar con
> `revisar.py`, en ese orden.

### Fase 2 — Infografía AA2

- [ ] **C9 · Contenido del mapa.** La lista de nodos, la jerarquía y los conectores,
      cerrada en texto antes de dibujar nada. Se aprueba como texto.
- [ ] **C10 · Dibujo, versión 1.** Según la herramienta que gane en D3.
- [ ] **C11 · Franja de aplicación a FactuGest.** El cierre que responde al criterio de
      evaluación.
- [ ] **C12 · Ajuste visual, exportación a PDF y verificación.** Legibilidad al 100 %, que
      todo quepa, que ningún texto se solape y que la tipografía sea la del documento de
      grado.

### Fase 3 — Cierre

- [ ] **C13 · Revisión final de los dos PDF** contra los lineamientos de la guía y
      actualización de la bitácora.

**Salida:** `calidad-documentos/entregables/`
**Scripts:** `calidad-documentos/generador/`

---

## 8 · Cómo se genera y se revisa

Nada de esto se duplicó, se reutiliza lo del documento de grado.

| Archivo | Qué hace |
|---|---|
| `generador/comun.py` | Portada, datos del equipo y salida. Importa `apa.py` y `e4_preliminares.py` de `docs expo/generador/` |
| `generador/aa1_informe.py` | Ensamblador del informe. Los capítulos que todavía no existen se saltan y se listan al final |
| `generador/fuentes.py` | Las fuentes en un solo sitio. `cita()` da la forma entre paréntesis y `narrativa()` la forma con el autor dentro de la frase. El cierre arma la bibliografía con las claves que cada capítulo declara en `CITADAS` |
| `docs expo/generador/revisar.py` | Abre el `.docx` en Word, actualiza los campos, exporta el PDF y saca un PNG por página |
| `docs expo/generador/verificar.py` | Comprueba márgenes, fuente, interlineado, sangría, paginación, numeración de tablas y figuras, y las tres marcas de estilo prohibidas |

```bash
cd "calidad-documentos/generador"
python aa1_informe.py

cd "../../docs expo/generador"
python revisar.py "../../calidad-documentos/entregables/FactuGest - Informe de metodos y estandar de calidad.docx"
python verificar.py "../../calidad-documentos/entregables/FactuGest - Informe de metodos y estandar de calidad.docx"
```

**Prueba de punta a punta del 8 de septiembre de 2026.** El esqueleto con la portada y la
tabla de contenido salió en 2 páginas y pasó 15 de las 16 comprobaciones. La que falla es
la sangría de 1,27 cm, y falla porque todavía no hay cuerpo, pues los únicos párrafos
largos son los de la portada, que van sin sangría a propósito. Se resuelve sola en C3 y
hay que volver a mirarla ahí.

---

## 9 · La evidencia recogida

`generador/evidencia.py` es el único sitio donde viven las cifras del informe. Los
capítulos las importan de ahí en vez de escribirlas en su propio texto, porque la cifra de
190 pruebas aparece en el resumen, en el plan y en la tabla de resultados, y escrita tres
veces se contradice la primera vez que alguien agregue una prueba. Los 32 requisitos no
funcionales tampoco se copian, se importan de `e1_requisitos.py`.

| Qué | Cuánto | Comprobado con |
|---|---|---|
| Pruebas unitarias en verde | 190 en 12 archivos | `python -m pytest`, salida en `evidencia/pytest_salida.txt` |
| Peticiones de la colección de la API | 11 | `evidencia/postman_inventario.txt` |
| Pruebas funcionales con captura | 4 operaciones, 8 imágenes | `docs expo/documento para que te guies claude/` |
| Requisitos no funcionales | 32 | `evidencia/rnf.txt`, importados de E1 |
| Defectos encontrados y corregidos | 4 | `CLAUDE.md` y las pruebas que los cubren |

Los cuatro defectos son los que le dan peso al informe, porque una lista de chequeo de
calidad quiere ver defectos detectados y corregidos, no un sistema que dice no haber
tenido ninguno. Son el membrete con el emisor equivocado, el descuento del 0,0 % restando
dinero real, la ciudad del comprador que llegaba vacía y los importes de ocho cifras que
se partían en la tabla.

Cuatro tipos de prueba quedan declarados como **planificados**, con esa palabra: el
rendimiento medido, la seguridad con herramienta, la regresión continua y la validación
real contra la autoridad tributaria.

**La matriz, hecha en C4.** El cruce vive en `MAPA`, dentro de
`generador/aa1_cap2_adopcion.py`, y las tablas se derivan de él contando, no escribiendo.
El archivo comprueba al importarse que no haya un requisito sin clasificar, uno clasificado
que no exista en el catálogo, una característica inventada ni una característica del
estándar sin ningún requisito, así que un descuadre rompe la generación en vez de salir
impreso.

El reparto quedó así, y es el hallazgo del capítulo: seguridad se lleva 9 de los 32
requisitos, más que ninguna otra característica. No es casualidad, es lo que significa ser
un proveedor que custodia las credenciales con las que otros emiten y responde por lo que
se hizo con ellas. En un sistema de gestión corriente ese peso estaría en usabilidad.

Tres categorías propias no coinciden con el estándar y el capítulo lo declara. Trazabilidad
no existe en la norma y sus dos requisitos son responsabilidad y no repudio, dentro de
seguridad. Escalabilidad tampoco existe y se reparte entre capacidad e interoperabilidad.
Y lo que el catálogo llamó compatibilidad de navegadores es en realidad adaptabilidad,
dentro de portabilidad, porque la compatibilidad de la norma se refiere a convivir e
intercambiar información con otros sistemas.

---

## 10 · Cosas que quedaron anotadas para el final

- **Las capturas funcionales son anteriores a un cambio del menú.** La imagen del
  formulario de emisión muestra todavía la entrada «Nueva factura (anterior)» en la barra
  lateral, que se retiró cuando quedó una sola vista de creación. La captura sigue siendo
  evidencia válida de que la operación se ejecutó. **Decidido el 8 de septiembre de 2026,
  se quedan como están** y no se vuelven a tomar.

---

## 11 · Bitácora

| Fecha | Tarea | Qué se decidió |
|---|---|---|
| 2026-09-08 | C0 | Se leyeron las dos guías y se levantó el inventario de evidencia real. 190 pruebas verificadas en verde. Aprobadas D1, D2 y D3, opción A en las tres. El informe adopta ISO/IEC 25010 en producto y CMMI nivel 2 en proceso, y la infografía se dibuja por código con matplotlib. |
| 2026-09-08 | C1 | Molde de formato listo y probado. Se decidió no copiar `apa.py` ni escribir un verificador propio, sino reutilizar los del documento de grado, para que los dos entregables y el documento de grado no se separen de formato. Los datos de portada se importan de `e4_preliminares.py` en vez de repetirse. Falta el apellido de la instructora. |
| 2026-09-08 | C2 | Evidencia recogida y congelada en `generador/evidencia.py`. Se corrigió el conteo por archivo del §4, que estaba hecho contando funciones y dejaba 32 pruebas por fuera, pues las parametrizadas valen por varias. Se decidió que la matriz ISO/IEC 25010 es trabajo de C4 y no de esta tarea. Confirmado el nombre de la instructora, Heidy Lizbeth Adarme, ya puesto en `comun.py`. |
| 2026-09-08 | C3 | Escritos la introducción y el marco de calidad, con las definiciones, la clasificación por producto y proceso, McCall, Boehm, CMMI y los cinco estándares, en 7 tablas. Las fuentes se pusieron en `fuentes.py` con dos formas de cita, porque escribir «según Scalone, 2006 la calidad» dentro de la frase es el error corriente al citar en APA. Se generalizó una comprobación de `verificar.py` del documento de grado, que buscaba la tabla de contenido en la tercera hoja porque ese documento abre con cubierta y portada, mientras que un entregable suelto la tiene en la segunda. Los cuatro entregables del documento de grado siguen pasando igual. |
| 2026-09-08 | C4 | Adoptados ISO/IEC 25010 y CMMI nivel 2, con el motivo del descarte de los otros cinco referentes. La matriz se deriva de una sola asignación y se comprueba sola. En CMMI se declararon 5 áreas cumplidas y 2 parciales, medición y análisis y gestión de acuerdos con proveedores, en vez de dar las siete por buenas, y se dejó escrito que un nivel de madurez se obtiene por evaluación formal, de modo que el informe no afirma estar certificado. Se ensanchó la columna de códigos de la tabla 8, donde «Requisitos» se partía en dos renglones. |
| 2026-09-08 | C5 | Plan de pruebas escrito con la estructura habitual de la documentación de pruebas. Se declaró explícitamente lo que queda fuera del alcance, la transmisión real ante la DIAN, la carga concurrente alta y el despliegue en producción, para que nadie lo busque en el capítulo de resultados. Dos decisiones del plan quedaron argumentadas, automatizar solo lo que no necesita base de datos y calcular a mano el resultado esperado de cada prueba. El riesgo de la concurrencia se declaró resuelto por diseño y no por prueba, porque una prueba de concurrencia detecta el problema a veces y el índice único lo impide siempre. |
| 2026-09-08 | C6 | Capítulo de evidencia. Los 15 casos se tomaron de la batería con sus valores tal como están escritos, no se redactaron para el informe, y por eso los importes no son cifras redondas. La tabla va en página apaisada porque con seis datos por caso en vertical las columnas quedaban en dos palabras por renglón. Se retiró el nivel 3 del índice, que hacía dos páginas y dejaba una hoja en blanco delante del primer capítulo por la marca de párrafo con que Word cierra el campo. |
| 2026-09-08 | C7 | Cerrado el contenido del informe. Las siete pruebas planificadas llevan métrica de aprobación y condición de inicio, porque una prueba planificada sin criterio no es un plan. El hallazgo del capítulo de resultados es el patrón de los cuatro defectos, pues ninguno está en la aritmética, que se escribió con pruebas, y los cuatro están en la generación del documento y en la consulta que lo alimenta, que no las tenían. De ahí salen las dos primeras acciones del plan de mejora. La conclusión final dice lo que las pruebas no demuestran, que es la ausencia de defectos, y lo que sí sostienen, que es que un error ya cometido no puede volver en silencio. |
| 2026-09-08 | C8 | Informe terminado. Las referencias se construyen desde las claves que cada capítulo declara, y el cierre comprueba que no quede una fuente citada sin referencia ni una referencia que nadie citó. El anexo B lista las 190 pruebas leyendo la salida de la corrida, no escritas a mano, así que el anexo no puede desfasarse del código. Se corrigieron dos cosas del armado, la hoja en blanco al final que dejaba volver a vertical después del anexo apaisado, y el título del libro de Beck, que el verificador leía como el patrón de texto generado y se agregó a su lista de excepciones junto con el de Myers. |
