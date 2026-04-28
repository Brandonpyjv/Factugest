# Factugest — Estado del Proyecto y Hoja de Ruta

> Última actualización: 2026-04-17

---

## ¿Qué es Factugest hoy?

Factugest es un sistema de facturación electrónica colombiana construido con **Python/FastAPI**, plantillas Jinja2 y base de datos MySQL. Actualmente funciona como un **panel de administración interno** desde el cual la empresa Factugest emite sus propias facturas electrónicas a sus clientes, cumpliendo con los estándares de la DIAN.

---

## ¿Qué tiene construido actualmente?

### Gestión de usuarios y roles
- Roles jerárquicos: **ADMIN → JEFE DE TIENDA → SUPERVISOR → CAJERO**
- Cada rol tiene permisos distintos sobre las vistas y acciones del sistema
- Soft-delete de usuarios (no se borran, se desactivan)

### Gestión de empresas / sucursales
- Registro completo de la empresa con datos DIAN:
  - NIT, DV, régimen tributario, actividad económica (CIIU)
  - Resolución DIAN: número, fechas de vigencia, rango de consecutivos autorizado
  - Prefijo de factura (ej. FV), consecutivo actual, consecutivo de NC y ND

### Gestión de clientes
- Registro con departamento y municipio de Colombia
- Tipo de documento, régimen tributario, datos de contacto
- Soft-delete (inactivación, no eliminación)

### Gestión de productos
- SKU, precio unitario, impuesto (IVA), unidad de medida, stock mínimo
- Descuentos por producto configurables

### Facturación electrónica completa
- **Factura de Venta (FV)** con:
  - Descuentos por línea de producto y descuento global a factura
  - Prorrateo correcto del IVA cuando hay descuento de factura
  - Generación de **CUFE** (Código Único de Factura Electrónica) con SHA-384
  - Numeración automática por consecutivo (ej. FV1, FV2…)
  - **PDF** completo al estilo DIAN con logo, membrete, resolución, QR, total en letras
  - **XML UBL 2.1** con estructura válida para la DIAN incluyendo descuentos (AllowanceCharge)
- **Nota Crédito (NC)**:
  - Anulación total de una factura
  - Devolución parcial por producto (selección de cantidades)
  - Actualiza el estado de la factura original a "Anulada" o "Parcialmente Anulada"
- **Nota Débito (ND)**:
  - Ajustes de precio, fletes, intereses u otros cargos adicionales
  - Descompone el IVA automáticamente según la tasa promedio de la factura original
- Todos los documentos quedan vinculados (FV ↔ NC/ND) con trazabilidad completa

### Estados de pago
- Paid, Pending, Partially Paid, Overdue, Cancelled, Disputed, Refunded
- **Anulada** y **Parcialmente Anulada** (nuevos, para NC)

### Dashboard
- Total de facturas, ingresos cobrados, facturas pendientes
- Total de clientes, productos activos, productos bajo stock
- Facturas recientes

---

## ¿Hacia dónde va Factugest?

### Decisión estratégica: Modelo A — API Middleware DIAN

Factugest **no será un software diferente para cada tipo de negocio**. En cambio, será el **intermediario técnico** que permite a cualquier negocio — con cualquier software que ya usen — emitir facturas electrónicas válidas ante la DIAN Colombia.

```
Sistema del cliente (POS, ERP, Excel, app propia)
        ↓  llamada HTTP
  API de Factugest
        ↓  genera CUFE + XML + PDF
      DIAN
        ↓  respuesta
  API de Factugest
        ↓  devuelve resultado
Sistema del cliente
```

El cliente **no cambia su software**. Solo se conecta a nuestra API.
El panel web actual se conserva como herramienta de administración y monitoreo interno.

---

## Hoja de ruta — Lo que viene

### Fase 1 — API pública REST *(próximo sprint)*
Exponer los servicios de facturación como endpoints consumibles por cualquier cliente:

| Endpoint | Descripción |
|---|---|
| `POST /api/v1/facturas` | Crear factura. Devuelve número, CUFE, PDF y XML |
| `POST /api/v1/notas-credito` | Crear NC referenciando una factura |
| `POST /api/v1/notas-debito` | Crear ND referenciando una factura |
| `GET /api/v1/facturas/{numero}` | Consultar estado de una factura |
| `GET /api/v1/facturas/{numero}/pdf` | Descargar PDF |
| `GET /api/v1/facturas/{numero}/xml` | Descargar XML |

**Autenticación:** API Key por cliente (header `X-API-Key`)
Cada cliente tendrá su propia empresa configurada con su resolución DIAN.

---

### Fase 2 — Modelo multicliente real
- Tabla de clientes API con nombre, API key, empresa asociada, plan y estado
- Cada cliente tiene sus propios consecutivos, resolución DIAN y datos de empresa
- Panel de administración para gestionar clientes: activar, desactivar, ver consumo

---

### Fase 3 — Habilitación DIAN real *(el paso más crítico)*
- Contratar proveedor tecnológico habilitado ante la DIAN o gestionar habilitación directa
- Implementar **firma digital XAdES-BES** en el XML (actualmente en pre-producción)
- Transmitir documentos al web service oficial de la DIAN
- Recibir y almacenar respuesta: aceptada, rechazada, con observaciones
- Manejar eventos del ciclo de vida: acuse de recibo, aceptación expresa, reclamo

---

### Fase 4 — Funcionalidades de valor agregado
- Envío automático del PDF de la factura por correo al cliente final
- Portal del cliente final para consultar sus propias facturas (sin login completo)
- **Webhooks**: notificar al sistema del cliente cuando la DIAN acepta o rechaza un documento
- Dashboard multicliente: monitoreo de transmisiones, errores y estadísticas por cliente API
- **SDKs** en Python, JavaScript y PHP para facilitar la integración
- Documentación pública de la API (aprovechando Swagger/OpenAPI integrado en FastAPI)

---

### Fase 5 — Monetización y self-service
- Planes por volumen de facturas mensuales: Free, Básico, Pro, Enterprise
- Panel self-service para que cada cliente configure su empresa y resolución DIAN sin intervención nuestra
- Facturación automática del servicio a los clientes API

---

## Stack tecnológico actual

| Componente | Tecnología |
|---|---|
| Backend | Python 3 / FastAPI |
| Base de datos | MySQL / MariaDB |
| Plantillas web | Jinja2 + Bootstrap 5 |
| Generación PDF | ReportLab + qrcode + num2words |
| XML | UBL 2.1 (estándar DIAN Colombia) |
| CUFE | SHA-384 (pre-producción) |
| Servidor | Uvicorn |

---

## Lo que falta para producción real con la DIAN

1. **Firma digital XAdES-BES** — el XML debe ir firmado digitalmente con certificado del emisor
2. **Clave técnica DIAN real** — actualmente se usa el NIT como placeholder en el CUFE
3. **Transmisión al web service DIAN** — endpoint oficial para envío de documentos
4. **Certificado digital** — cada empresa emisora necesita su certificado
5. **Habilitación formal** — proceso ante la DIAN para operar como proveedor tecnológico

---

*Factugest — Simplificando la facturación electrónica en Colombia*
