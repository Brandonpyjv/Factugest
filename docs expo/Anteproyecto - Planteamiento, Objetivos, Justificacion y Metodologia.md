# FactuGest — Planteamiento del Problema, Objetivos, Justificación, Metodología y Herramientas

**Proyecto:** FactuGest — Sistema de Facturación Electrónica para Colombia
**Equipo:** Brandon Arley Restrepo Gelvez · Johan Sebastián Acosta Sánchez · Wilmer Jesús Contreras Rangel
**Programa:** Tecnólogo en Análisis y Desarrollo de Software — SENA, Centro de la Industria, la Empresa y los Servicios

---

## 1. Planteamiento del problema

En Colombia, la facturación electrónica dejó de ser una opción para convertirse en una obligación legal. La Dirección de Impuestos y Aduanas Nacionales (DIAN) ha implementado de forma progresiva un sistema de facturación electrónica de validación previa que exige a los sujetos obligados generar documentos con estructura XML bajo el estándar UBL 2.1, firmarlos digitalmente, calcular el Código Único de Factura Electrónica (CUFE), transmitirlos a los servicios web de la entidad para su validación y conservarlos por los términos que fija la normativa tributaria. Quien no cumple queda expuesto al desconocimiento de costos y deducciones, al rechazo de sus documentos por parte de terceros y a sanciones de carácter tributario.

El problema no está en la norma, sino en la distancia entre lo que la norma exige y lo que una micro, pequeña o mediana empresa puede efectivamente ejecutar. Este segmento —que concentra la mayor parte del tejido empresarial y del empleo del país— opera con equipos reducidos, sin áreas de tecnología, con presupuestos ajustados y con niveles heterogéneos de alfabetización digital. Al enfrentarse al cumplimiento, encuentra tres barreras concretas:

**a) Barrera de complejidad técnica.** Emitir una factura electrónica válida no es "llenar un formulario": implica dominar conceptos de estructura XML, firma digital, códigos DIAN de impuestos, dígitos de verificación del NIT, resoluciones de numeración, rangos de consecutivos autorizados y reglas de prorrateo de IVA sobre descuentos. La plataforma gratuita de la DIAN y los portales oficiales resultan poco intuitivos para el usuario no técnico, y los errores en el diligenciamiento derivan en documentos rechazados que deben rehacerse.

**b) Barrera económica y de acceso.** Las soluciones comerciales disponibles en el mercado suelen estar diseñadas para empresas medianas y grandes, con esquemas de licenciamiento, costos de implementación y planes de soporte que no se ajustan a la capacidad de pago de un negocio pequeño. El resultado es que muchos establecimientos aplazan la adopción, la resuelven de forma manual y parcial, o quedan directamente en incumplimiento.

**c) Barrera de integración con lo que ya tienen.** Buena parte de estos negocios ya invirtió en un punto de venta (POS), un ERP liviano o un sistema propio con el que factura, controla inventario y cobra a diario. Las alternativas del mercado suelen exigir migrar toda la operación a una nueva plataforma —cambiar el software con el que el negocio ya opera—, lo que implica costos de aprendizaje, interrupción de la operación y pérdida del histórico. La necesidad real no es reemplazar ese software, sino **conectarlo** con la DIAN.

A estas barreras se suma la falta de información gerencial. Muchos de estos negocios facturan sin obtener a cambio ninguna lectura de su propia operación: no saben con precisión cuánto tienen por cobrar, qué facturas están vencidas, qué productos concentran sus ventas ni cómo se comporta su flujo de ingresos. La facturación se vive como una carga administrativa impuesta y no como una fuente de datos para tomar decisiones.

En consecuencia, se identifica la necesidad de una solución de software que reduzca simultáneamente las tres barreras: que sea **técnicamente correcta** frente a la DIAN, **accesible y usable** para un usuario no especializado, y **capaz de integrarse** con los sistemas que las empresas ya utilizan, entregando además información útil sobre la salud financiera del negocio. De no atenderse esta necesidad, un porcentaje significativo del tejido empresarial colombiano continuará operando en incumplimiento normativo o asumiendo sobrecostos administrativos evitables.

> **Pregunta problema:** ¿Cómo desarrollar una solución de software accesible, usable e integrable que permita a las micro, pequeñas y medianas empresas colombianas emitir facturación electrónica válida ante la DIAN, sin necesidad de reemplazar los sistemas de venta que ya utilizan, y obtener a partir de ello información útil para la gestión financiera de su negocio?

---

## 2. Objetivo general

Desarrollar FactuGest, un sistema de facturación electrónica para Colombia, construido con Python y FastAPI, que permita a micro, pequeñas y medianas empresas cumplir con la obligación legal de facturar electrónicamente ante la DIAN mediante una interfaz web accesible y sencilla de operar, y que exponga sus servicios como una API de integración capaz de conectarse con los sistemas de punto de venta que las empresas ya tienen implementados.

---

## 3. Objetivos específicos

**3.1.** **Implementar el módulo de emisión de documentos electrónicos**, que permita generar Facturas de Venta (FV), Notas Crédito (NC) y Notas Débito (ND) con el cálculo automático de bases gravables, descuentos por línea y globales, prorrateo de IVA e impuestos según el código DIAN de cada producto, generando para cada documento su consecutivo autorizado, su CUFE, su representación gráfica en PDF y su archivo XML bajo el estándar UBL 2.1 exigido por la DIAN.

**3.2.** **Desarrollar un módulo de reportes y tablero de control (dashboard)** que consolide la información generada por la operación de facturación —ingresos efectivamente cobrados, cartera pendiente y vencida, comportamiento de ventas, clientes, productos activos y niveles de inventario bajo mínimo— y la presente mediante indicadores y reportes exportables, de modo que el usuario pueda evaluar la salud financiera de su empresa y sustentar la toma de decisiones.

**3.3.** **Construir una API REST de integración (modelo *middleware* DIAN)** que exponga los servicios de facturación de FactuGest como endpoints consumibles por sistemas externos, de manera que un punto de venta, un ERP o una aplicación propia ya existente pueda enviar los datos de una venta, y FactuGest se encargue de generar el documento electrónico, gestionar la comunicación con la DIAN y devolver al sistema origen el resultado (número, CUFE, estado, PDF y XML), sin que la empresa deba reemplazar el software con el que opera.

---

## 4. Justificación

**Justificación legal y normativa.** La facturación electrónica es en Colombia un requisito de obligatorio cumplimiento para los sujetos definidos por la DIAN. Su incumplimiento no es una omisión menor: compromete la deducibilidad de costos y gastos, dificulta las relaciones comerciales con clientes que exigen soporte válido y expone al contribuyente a sanciones. Desarrollar una herramienta que facilite este cumplimiento atiende una necesidad jurídicamente exigible y con consecuencias económicas directas para el empresario.

**Justificación social y económica.** Las micro, pequeñas y medianas empresas constituyen la base del aparato productivo colombiano y son las que menos recursos tienen para asumir la carga técnica y financiera de la transformación digital tributaria. Una solución accesible, con interfaz sencilla y bajo costo de adopción, democratiza el acceso al cumplimiento: permite que un negocio pequeño opere en la formalidad en las mismas condiciones técnicas que una empresa grande. El impacto no se limita al empresario individual; una mayor formalización fortalece el recaudo, mejora la trazabilidad de las operaciones y aporta transparencia al sistema fiscal.

**Justificación técnica.** La decisión arquitectónica de operar como *middleware* —una API que se conecta a los sistemas ya existentes en lugar de reemplazarlos— responde directamente a una de las principales barreras identificadas en el diagnóstico: el costo de cambiar de software. Este enfoque preserva la inversión previa del empresario, elimina la curva de aprendizaje de un sistema nuevo y evita interrumpir la operación diaria del negocio. Adicionalmente, el uso de FastAPI aporta ventajas concretas para este caso de uso: alto rendimiento por transacción, validación automática de datos de entrada mediante tipado con Pydantic y generación automática de documentación OpenAPI/Swagger, lo que reduce significativamente el esfuerzo de integración para los desarrolladores de los sistemas cliente.

**Justificación desde la gestión empresarial.** El módulo de reportes convierte una obligación tributaria en un activo de información. Los datos que la empresa está legalmente obligada a registrar —ventas, clientes, impuestos, estados de pago— se transforman en indicadores de gestión sin trabajo adicional para el usuario. Esto agrega valor más allá del cumplimiento y responde a una necesidad real de control financiero en negocios que hoy no cuentan con herramientas de análisis.

**Justificación académica y formativa.** El proyecto integra y evidencia las competencias del programa Tecnólogo en Análisis y Desarrollo de Software: levantamiento y especificación de requisitos bajo el estándar IEEE 830, modelado de casos de uso, diseño y normalización de bases de datos relacionales, desarrollo backend y frontend, diseño e implementación de servicios REST, aplicación de mecanismos de seguridad (hasheo de contraseñas, gestión de sesiones, control de acceso por roles, autenticación por token), control de versiones y trabajo colaborativo bajo metodología ágil. Su desarrollo sobre un problema real, con normativa vigente y usuarios reales, otorga al ejercicio formativo un nivel de exigencia equivalente al de un entorno productivo.

---

## 5. Metodología

### 5.1. Tipo y enfoque de la investigación

El proyecto se enmarca en una **investigación aplicada**, orientada a resolver un problema concreto y verificable del entorno mediante la construcción de un producto de software. El **enfoque es mixto**: cualitativo en la caracterización de las dificultades, percepciones y barreras que enfrentan las empresas frente a la facturación electrónica, y cuantitativo en la medición de variables como el nivel de adopción, los tiempos de emisión, los tipos de clientes, productos y medios de pago más utilizados. El **alcance es descriptivo-propositivo**: describe la situación actual del proceso de facturación en las empresas objetivo y propone una solución tecnológica para atenderla.

### 5.2. Población, muestra e instrumento de recolección

- **Población:** micro, pequeñas y medianas empresas y profesionales independientes en Colombia que estén obligados a facturar electrónicamente.
- **Muestra:** no probabilística por conveniencia, integrada por empresas que ya emiten factura electrónica y por empresas que aún no han implementado el sistema, con el fin de contrastar experiencias, barreras y necesidades de ambos grupos.
- **Instrumento:** encuesta estructurada desplegada mediante formulario digital (Google Forms), cuyos objetivos fueron: (i) determinar el nivel de experiencia y las dificultades en la emisión de facturas electrónicas, (ii) identificar los tipos de clientes, productos y medios de pago más utilizados, y (iii) analizar el impacto del software de facturación en la eficiencia del proceso. Los resultados obtenidos alimentaron directamente la definición de requisitos y la priorización del backlog del producto.

### 5.3. Metodología de desarrollo de software

Se adopta **Scrum** como marco de trabajo ágil, por su capacidad de entregar valor de forma incremental y de absorber cambios de requisitos —una condición inevitable en un proyecto sujeto a normativa tributaria que se actualiza periódicamente. La planificación y el seguimiento se realizan en **Jira**, con el trabajo organizado en épicas, historias de usuario, tareas y subtareas, distribuidas en sprints.

**Elementos aplicados del marco:**

| Elemento | Aplicación en el proyecto |
|---|---|
| Roles | Product Owner (definición y priorización del backlog), Scrum Master (facilitación del proceso) y Equipo de Desarrollo (3 integrantes) |
| Artefactos | Product Backlog en Jira, Sprint Backlog por iteración, Incremento funcional al cierre de cada sprint |
| Ceremonias | Planificación de sprint, seguimiento periódico, revisión del incremento y retrospectiva |
| Definición de "hecho" | Funcionalidad implementada, probada manualmente y vía Postman/Swagger, documentada y versionada en el repositorio |

La especificación de requisitos se documentó siguiendo el **estándar IEEE 830**, con la clasificación de requerimientos funcionales (RF01–RF17) y no funcionales (RNF01–RNF15) en las categorías de rendimiento, seguridad, usabilidad, escalabilidad, compatibilidad, mantenibilidad y conectividad. Cada requerimiento se tradujo posteriormente a **historias de usuario** con sus criterios de aceptación, y el comportamiento del sistema se modeló mediante **casos de uso** por actor (Administrador, Usuario/Cajero, Contador, Cliente), documentando descripción, precondiciones, secuencia normal, postcondiciones y excepciones.

### 5.4. Fases del desarrollo

**Fase 1 — Análisis y levantamiento de requisitos.**
Diagnóstico del problema, aplicación de la encuesta, análisis de la normativa DIAN aplicable (estructura UBL 2.1, CUFE, códigos de impuestos, resoluciones de numeración), especificación de requisitos bajo IEEE 830, elaboración del catálogo de casos de uso y definición de las clases de usuario y sus permisos.

**Fase 2 — Diseño.**
Diseño del modelo de datos relacional (facturas, detalle_factura, clientes, productos, empresas emisoras, impuestos, métodos y estados de pago, usuarios, logs) y definición de la **arquitectura en tres capas**:

```
Cliente (navegador web / sistema POS externo)
        ↓ HTTP
routes/       → controladores: reciben la petición y validan la entrada
        ↓
services/     → lógica de negocio: cálculos tributarios, CUFE, XML, PDF
        ↓
database.py   → capa de acceso a datos: ejecución de consultas SQL
        ↓
Base de datos relacional
```

Esta separación es la decisión de diseño central del proyecto: al concentrar toda la lógica de negocio en la capa `services/`, la misma implementación alimenta tanto la interfaz web como los endpoints JSON de la API de integración, sin duplicar código ni arriesgar inconsistencias entre canales.

**Fase 3 — Desarrollo iterativo e incremental.**
Construcción por sprints, entregando en cada uno un incremento funcional utilizable. El orden de implementación siguió la dependencia natural del dominio: primero los datos maestros (impuestos, empresas emisoras, métodos y estados de pago, productos, clientes), luego el módulo de facturación, después la generación de documentos electrónicos (PDF, XML, CUFE), las notas crédito y débito, el dashboard, y finalmente la exposición de la API REST de integración.

Durante esta fase el proyecto atravesó un proceso de **refactorización tecnológica documentada**: la implementación inicial se realizó sobre Flask, posteriormente se desarrolló una versión sobre Java con Spring Boot que incorporó mejoras en seguridad y en el modelo de datos, y finalmente esas mejoras se consolidaron sobre **FastAPI**, seleccionado por su rendimiento, su validación automática de datos y su generación nativa de documentación OpenAPI —capacidad determinante para el objetivo de exponer una API de integración. Cada migración quedó registrada en la documentación técnica del repositorio.

**Fase 4 — Pruebas y validación.**
Pruebas funcionales manuales sobre los flujos de la interfaz web; pruebas de los endpoints REST mediante **Postman** y la documentación interactiva **Swagger UI** autogenerada por FastAPI; verificación de la exactitud de los cálculos tributarios (bases gravables, descuentos por línea y globales, prorrateo de IVA, totales); validación de la estructura del XML frente al estándar UBL 2.1; y pruebas de control de acceso por rol y de los mecanismos de autenticación.

**Fase 5 — Documentación y despliegue.**
Elaboración de la documentación técnica del sistema (arquitectura, modelo de datos, referencia de endpoints, guía de instalación y ejecución, documento de seguridad) y de la documentación funcional de uso. La documentación de la API se publica de forma automática y siempre sincronizada con el código a través de Swagger/OpenAPI.

### 5.5. Control de versiones y trabajo colaborativo

El código fuente se gestiona con **Git** y se aloja en **GitHub**, en repositorios separados para el backend y el cliente móvil. El versionado de la API es obligatorio (`/api/v1/`): cualquier cambio que rompa el contrato existente debe publicarse en una nueva versión, garantizando que los sistemas ya integrados no se vean afectados. Las credenciales y datos sensibles se gestionan mediante variables de entorno en archivos `.env` excluidos del control de versiones.

---

## 6. Herramientas utilizadas

### 6.1. Lenguajes y frameworks

| Herramienta | Uso en el proyecto |
|---|---|
| **Python 3.10+** | Lenguaje principal del backend. Elegido por su legibilidad, su amplio ecosistema de librerías y su idoneidad para el procesamiento de datos y la generación de documentos. |
| **FastAPI** | Framework web del backend. Gestiona el enrutamiento HTTP, la validación automática de datos de entrada mediante tipado y la generación automática de la documentación OpenAPI/Swagger, base de la API de integración. |
| **Uvicorn** | Servidor ASGI que ejecuta la aplicación FastAPI. |
| **Jinja2** | Motor de plantillas para el renderizado del lado del servidor de la interfaz web. |
| **HTML5** | Estructura de las vistas e interfaces del sistema. |
| **CSS3 / Bootstrap 5** | Estilos y diseño responsivo, garantizando el acceso desde escritorio y dispositivos móviles. |
| **JavaScript** | Interactividad del lado del cliente: cálculo en tiempo real de bases gravables, descuentos, impuestos y totales durante la creación de la factura, y consumo asíncrono de endpoints. |

### 6.2. Base de datos

| Herramienta | Uso en el proyecto |
|---|---|
| **Motor relacional (MySQL/MariaDB en la implementación actual; PostgreSQL en la iteración sobre Spring Boot)** | Almacenamiento persistente de facturas, detalle de facturas, clientes, productos, empresas emisoras, impuestos, usuarios, métodos y estados de pago, y registro de logs. Se trabaja con SQL directo, sin ORM, para mantener control explícito sobre las consultas y el rendimiento. |

### 6.3. Librerías especializadas

| Herramienta | Uso en el proyecto |
|---|---|
| **ReportLab** | Generación de la representación gráfica en PDF de facturas, notas crédito y notas débito. |
| **qrcode** | Generación del código QR de verificación exigido en la representación gráfica DIAN. |
| **num2words** | Conversión del valor total de la factura a texto en español, requisito de la representación gráfica. |
| **bcrypt** | Hasheo de contraseñas de usuarios. |
| **python-dotenv** | Carga de variables de entorno para proteger credenciales fuera del código fuente. |
| **itsdangerous** | Firma criptográfica de las cookies de sesión. |

### 6.4. Entorno de desarrollo, pruebas y gestión

| Herramienta | Uso en el proyecto |
|---|---|
| **PyCharm** | IDE principal de desarrollo: edición, depuración, gestión del entorno virtual e integración con el control de versiones. |
| **Postman** | Pruebas manuales de los endpoints REST: verificación de peticiones, respuestas, códigos de estado y autenticación por token. |
| **Swagger UI / OpenAPI** | Documentación interactiva de la API generada automáticamente por FastAPI; sirve simultáneamente como herramienta de prueba y como documentación de integración para los sistemas cliente. |
| **Git** | Control de versiones del código fuente. |
| **GitHub** | Alojamiento remoto de los repositorios y trabajo colaborativo del equipo. |
| **Jira** | Planificación y seguimiento del proyecto bajo Scrum: épicas, historias de usuario, tareas, subtareas y sprints. |
| **Google Forms** | Diseño y aplicación de la encuesta de levantamiento de requisitos. |
| **Claude (Anthropic)** | Asistente de inteligencia artificial empleado como apoyo en el proceso de desarrollo: generación y revisión de código, refactorización, documentación técnica, análisis de la normativa aplicable y resolución de problemas de implementación. Todo el código generado fue revisado, probado y validado por el equipo antes de su integración. |

---

*FactuGest — Simplificando la facturación electrónica en Colombia*
