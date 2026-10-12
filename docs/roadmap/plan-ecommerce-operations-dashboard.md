# Roadmap: E-Commerce Operations & Intelligence Dashboard

Este documento define la hoja de ruta para evolucionar la PoC de Streamlit hacia un dashboard analítico y operativo de nivel productivo para un **E-Commerce de extremo a extremo**.

---

## 🧭 Visión y Pipeline de Negocio

El sistema modela las 4 etapas críticas del ciclo de vida de un E-Commerce:
1. **Checkout & Ventas**: GMV, AOV, conversión y ciclo de vida de pedidos.
2. **Pagos & Transacciones**: Cobros aprobados/rechazados, causales de rechazo, desempeño de pasarelas de pago.
3. **Logística & Envíos**: Despachos, lead times de entrega, cumplimiento de SLAs por courier.
4. **Inventario & Stock**: Monitoreo de rotación de catálogo, SKUs críticos y alertas de quiebre de stock.

---

## 📋 Fases del Roadmap

### Fase 1: Modelado de Dominio & Pipeline de Datos Sintético (`feat/01-ecommerce-domain-pipeline`)
- [x] Definir Value Objects de Dominio (`Money`, `OrderStatus`, `PaymentStatus`, `PaymentMethod`, `ShipmentStatus`).
- [x] Definir Entidades del Dominio (`Order`, `OrderItem`, `PaymentTransaction`, `Shipment`, `InventoryItem`).
- [x] Definir Puerto de Lectura de Datos (`EcommerceDataReaderPort`).
- [x] Implementar Generador de Datos Sintéticos Realistas con distribución temporal y correlaciones estadísticas (`SyntheticEcommerceDataGenerator`).
- [x] Implementar Adaptador en Memoria (`InMemoryEcommerceDataReader`).
- [x] Tests unitarios del dominio y generador (`make test`).

### Fase 2: Casos de Uso Analíticos y Motor de Métricas (`feat/02-ecommerce-analytics-use-cases`)
- [ ] Definir DTOs analíticos (`EcommerceOverviewDTO`, `PaymentAnalyticsDTO`, `LogisticsAnalyticsDTO`, `InventoryHealthDTO`).
- [ ] Implementar Caso de Uso: `GetEcommerceOverviewUseCase` (GMV, AOV, evolución temporal, categorías top).
- [ ] Implementar Caso de Uso: `GetPaymentAnalyticsUseCase` (Tasa de aprobación, desglose de fallas, volumen por método).
- [ ] Implementar Caso de Uso: `GetLogisticsAnalyticsUseCase` (Cumplimiento de SLA On-Time %, lead times por courier y región).
- [ ] Implementar Caso de Uso: `GetInventoryHealthUseCase` (SKUs en riesgo, alertas de stockout, rotación de catálogo).
- [ ] Tests unitarios e integración para todos los casos de uso (`make check`).

### Fase 3: Dashboard Multi-Página Ejecutivo en Streamlit (`feat/03-ecommerce-streamlit-views`)
- [ ] Diseñar layout multi-página profesional con sidebar de navegación y filtros globales (fecha, categoría, courier).
- [ ] Implementar Vista: **📈 Executive Overview** (KPI cards con deltas, gráfico evolutivo GMV, funnel interactivo).
- [ ] Implementar Vista: **💳 Payment & Risk Intelligence** (Gráfico donut de aprobación/rechazo, barras de causales de fallo, matriz de pasarelas).
- [ ] Implementar Vista: **🚚 Logistics & Delivery Tracking** (Cumplimiento de SLA por operador, tiempos medios, estado en tránsito).
- [ ] Implementar Vista: **📦 Inventory Health & Alerts** (Tabla de alertas de stock crítico, semáforo de reposición, turnover).
- [ ] Extraer componentes atómicos reutilizables (`kpi_metric_card.py`, `status_tag.py`, `dark_theme_config.py`).
- [ ] Pruebas de integración visual y verificación manual interactiva (`make check`).

### Fase 4: Modo Stream / Tiempo Real & Simulación de Eventos (`feat/04-realtime-simulation-stream`)
- [ ] Implementar emisor de transacciones en streaming simulado (`EcommerceEventStreamGenerator`).
- [ ] Agregar vista o selector de monitoreo en vivo con autorefresh en Streamlit.
- [ ] Validar rendimiento y estabilidad de estado en Streamlit.
