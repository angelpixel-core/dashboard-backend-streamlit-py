---
id: brief
aliases: []
tags: []
---

# PRD / Brief — Sales Ops Dashboard (Streamlit) — “Producto Pro”
**Proyecto:** dashboard-backend-streamlit-py
**Owner:** Angel
**Estado:** Draft v1 (para implementar post-tutorial)
**Objetivo:** Convertir el sandbox actual de Streamlit en un dashboard “pro” y mantenible, con UX consistente, performance aceptable, tests, y una estructura lista para evolucionar a “producto interno” (Sales Ops).

---

## 0) Contexto y motivación

Hoy existe un dashboard en Streamlit que:
- muestra métricas (KPIs), un line chart de ventas y un pie chart de clientes por región
- tiene filtros por Mes y Región
- tiene una arquitectura de presentación separada (funciones `_render_*`) y un enfoque “clean/hexagonal” en proceso
- ya se corrigió una semántica clave: Mes debe permitir neutral (“Todos”)

El objetivo de esta etapa es **pasar de “demo/sandbox” a “dashboard operativo pro”**, sin caer en overengineering ni requerir componentes React custom.

---

## 1) Definición de “Pro”

Un dashboard “pro” significa:

1) **Consistencia funcional**
- Los filtros afectan: KPIs + charts + tabla (no solo la tabla).
- La semántica de filtros es clara y coherente (neutral/AND).

2) **Performance razonable**
- No recalcular todo ante cada interacción si no es necesario.
- Cachear dataset y agregaciones.

3) **UX clara**
- Estados vacíos entendibles
- Mensajes de error accionables
- “Contexto” visible (qué filtros están activos)

4) **Navegación**
- Múltiples vistas (tabs o multi-page) por “dominio” o “rol”.

5) **Mantenibilidad**
- Arquitectura con boundaries: dominio → aplicación → presentación
- Tests de lógica de filtros/agregaciones
- Makefile/targets para checks y fixes

6) **Listo para integrarse a un core (Rails) a futuro**
- El dashboard debe poder consumir datos desde un API (Rails) sin reescribir toda la UI.

---

## 2) Alcance (Scope)

### 2.1 En alcance (MVP pro)
- Filtros globales consistentes (Mes + Región)
- KPIs + charts + tabla conectados al dataset filtrado
- Multi-vista (tabs o multi-page) con al menos 3 secciones
- Caching (dataset + agregaciones)
- Export CSV de tabla filtrada
- Estados vacíos + errores robustos
- Theming base y layout consistente
- Tests unitarios para filtros y agregaciones
- Ajustes de deprecations de Streamlit (`width='stretch'`)

### 2.2 Fuera de alcance (por ahora)
- Auth/roles enterprise (se evalúa luego)
- Componentes React custom
- FastAPI como capa adicional
- Conectar a un warehouse real
- Alerting avanzado / scheduler
- AB testing / feature flags complejos

---

## 3) Usuarios y casos de uso

### Usuarios
- **Operador/Owner:** vos (uso interno) para analizar ventas y comportamiento.
- **Stakeholder:** “mirar números” en Overview (si se comparte).

### Casos de uso MVP
1) Ver el estado general (MTD/YTD) y tendencias.
2) Filtrar por Mes y Región, ver impacto inmediato en KPIs y charts.
3) Identificar top regiones / top SKUs (si la data lo permite).
4) Exportar la tabla filtrada para análisis externo.
5) Entender rápidamente por qué no hay datos (estado vacío).

---

## 4) Estructura de información (modelo de datos mínimo)

### Campos esperados (mínimos)
- `Mes` (string o periodo)
- `Región` (string)
- `Ventas` (numérico)
- `Clientes` (numérico)
- (opcional, recomendado) `sku`, `units`, `revenue`, `currency`

### Reglas de calidad mínimas
- El dashboard debe validar existencia de columnas requeridas.
- Si falta una columna, mostrar error explícito (no stacktrace).

---

## 5) Semántica de filtros (contrato UX)

### 5.1 Filtro Mes
- Opciones: `["Todos", ...meses ordenados...]`
- Regla:
  - `Mes="Todos"` => no filtra por mes
  - `Mes="Febrero"` => filtra por “Febrero”

### 5.2 Filtro Región
- `selected_regions=[]` => “Todas”
- `selected_regions=[...]` => filtra por esas regiones

### 5.3 Combinación
- Cuando ambos están activos: **AND**
  - Ej: Mes=Febrero y Región=[Centro, Sur] => Febrero ∩ (Centro ∪ Sur)

### 5.4 UI de filtros
- Mostrar siempre “Filtros activos -> Mes: X | Región: Y”
- Si Mes=Todos => mostrar “Todos”
- Si Región vacía => mostrar “Todas”

---

## 6) Navegación: tabs o multi-page

### Recomendación MVP: Tabs (más simple que multi-page)
Crear tabs:
1) **Overview**
2) **Ventas**
3) **Clientes**
4) **Datos / Export** (opcional, pero recomendado)

> Alternativa: multi-page si querés que “se sienta producto enterprise”.
> Para MVP, tabs es más rápido y suficiente.

---

## 7) Páginas/Secciones — Contenido detallado

### 7.1 Overview (Executive Board)
**Objetivo:** visión rápida
- KPIs (arriba, en columnas):
  - Ventas totales (filtradas)
  - Clientes totales (filtrados)
  - Ticket promedio (si hay units o pedidos)
  - Variación vs periodo anterior (si hay histórico comparable; si no, “N/A”)
- Charts:
  - Evolución de ventas (line)
  - Distribución de clientes por región (pie o bar)
- Tabla resumida (top N):
  - top regiones por ventas
  - top SKUs (si existe sku)

### 7.2 Ventas
**Objetivo:** profundidad de revenue
- Line chart (ventas por mes/tiempo, según filtro)
- Breakdown:
  - ventas por región (bar)
  - ventas por SKU (bar / table)
- Tabla detallada filtrada (dataframe)

### 7.3 Clientes
**Objetivo:** entender distribución
- Clientes por región (bar + tabla)
- Si hay data: cohortes simples (opcional)
- Tabla filtrada

### 7.4 Datos / Export (opcional)
**Objetivo:** operación y confiabilidad
- “Última actualización” (si aplica)
- “Dataset shape”
- Export CSV del dataset filtrado
- Posibilidad de cargar CSV para pruebas (si querés)

---

## 8) Gráficos y librerías

- Plotly Express para charts (como ya usás).
- Template: `plotly_dark` (o configurable).
- Evitar errores por mismatch de columnas:
  - **Usar nombres exactos de columnas:** `"Región"` (con tilde), no `"Region"`.

**Acción requerida por bug detectado:**
- Corregir cualquier referencia a `names="Region"` → `names="Región"`.

---

## 9) Reglas de UI/UX (detalle)

### 9.1 Estados vacíos
Si el dataframe filtrado queda vacío:
- Mostrar `st.info("No hay datos para la combinación de filtros seleccionada.")`
- No renderizar charts que fallen por df vacío (evitar exceptions).

### 9.2 Errores de datos (missing columns / wrong schema)
- Detectar al inicio:
  - Si faltan columnas requeridas: `st.error("Faltan columnas requeridas: ...")` y abortar render.
- No permitir stack traces visibles al usuario.

### 9.3 Performance UX
- Ideal: filtros dentro de un `st.form` con botón “Aplicar”
  - Evita reruns en cada selección.
- Alternativa MVP: rerun inmediato, pero con caching.

### 9.4 Layout
- `st.set_page_config(layout="wide")`
- usar `st.columns` para KPIs y secciones
- evitar scroll excesivo: agrupar con `st.expander` cuando sea necesario

---

## 10) Caching y performance

### 10.1 Cache dataset
- `@st.cache_data` para load/compute del dataframe base

### 10.2 Cache agregaciones
- Cachear funciones de agregación por:
  - selected_month
  - selected_regions (convertir a tuple ordenada para key estable)

### 10.3 No recalcular si no cambió nada
- Guardar filtros en `st.session_state`
- Si usás `st.form`, solo recalcular cuando “Aplicar” se presiona.

---

## 11) Arquitectura del código (propuesta)

### 11.1 Objetivo
Mantener UI delgada y lógica testable.

### 11.2 Estructura sugerida (aprox)
```txt
src/dashboard/
----domain/
--------models.py
--------ports.py
--------schema.py
----application/
--------services.py
--------queries.py
----infrastructure/
--------readers/
------------in_memory.py
------------rails_api.py (future)
--------fixtures/
------------sales_seed.py (future)
----presentation/
--------streamlit/
------------app.py
------------components/
----------------kpis.py
----------------charts.py
----------------tables.py
------------pages/
----------------overview.py
----------------sales.py
----------------customers.py
```

### 11.3 Contratos
- `ReaderPort` (interfaz):
  - `get_sales_dataframe(...) -> pd.DataFrame` (o un DTO que luego se normaliza a df)
- `Application services`:
  - filtros / agregaciones / validaciones de schema

### 11.4 Principio clave
- Presentación (Streamlit) **no** conoce detalles de infraestructura.
- Infra define fuentes (in-memory hoy; API Rails mañana).

### 11.5 Patrón de inyección (Composition Root)

**Regla:** la capa `presentation/streamlit` **no debe** importar fixtures ni construir datos hardcodeados.
La UI solo compone dependencias (puertos) e invoca servicios.

**Dónde vive la composición:** `presentation/streamlit/app.py` actúa como *composition root* (armado de dependencias).

**Fuente de datos demo:** los mocks/seed deben vivir en `infrastructure/fixtures/` y exponerse como helpers (por ejemplo `build_seed_records()` / `seed_dataframe()`).

**Ejemplo (pseudo):**

- `infrastructure/fixtures/sales_seed.py`
  - `build_seed_records() -> list[InMemorySalesRecord]`

- `infrastructure/readers/in_memory.py`
  - `InMemorySalesAggregateReader(records=...)` implementa `ReaderPort`

- `presentation/streamlit/app.py`
  - importa **solo** el `ReaderPort` (vía implementación elegida) y compone:
    - `records = build_seed_records()`
    - `reader = InMemorySalesAggregateReader(records=records, ...)`
  - luego renderiza llamando a servicios/queries con `reader`

**Objetivo:** permitir reemplazar `InMemorySalesAggregateReader` por `RailsApiReader` sin tocar la UI, manteniendo una única “fuente de verdad” por entorno (demo vs real).

---

## 12) Integración futura (Rails como source of truth)

**No implementar ahora**, pero diseñar para:
- `Rails API` expone endpoints de reporting/export (pull)
- Streamlit consume endpoints (o dataset exportado)
- Rails recolecta eventos desde el frontend (Next) en el futuro

### Contrato futuro mínimo (idea)
- `GET /reports/sales?from=&to=&region=...`
- `GET /reports/customers?...`
- `GET /exports/sales.csv?...`

---

## 13) Tests (mínimos obligatorios)

### 13.1 Unit tests (lógica)
- `_apply_dashboard_filters`:
  1) Mes=Todos, Región=[] => full dataset
  2) Mes=Febrero, Región=[] => filtra por mes
  3) Mes=Todos, Región=[Centro] => filtra por región
  4) Mes=Febrero, Región=[Centro,Sur] => filtro AND
- Validación de schema:
  - si falta `Región` o `Mes` debe fallar con mensaje claro

### 13.2 Test de agregaciones (si existen)
- top regiones por ventas: suma correcta
- tabla ordenada correctamente

> Meta: al menos 5–8 tests unitarios.

---

## 14) Tooling / DevX

### 14.1 Makefile
- `make run`
- `make lint`, `make lint-fix`
- `make format`, `make format-check`
- `make typecheck`
- `make test` (unit)
- `make check` (lint + typecheck + test)
- `make check-fix` (aplica fix sin correr tests)

> Ya existe workflow de ruff fix con targets explícitos.

### 14.2 Deprecations Streamlit
Streamlit emitió warning:
- reemplazar `use_container_width` por `width`
  - `width='stretch'` para equivalente a True

**Regla:** usar `st.plotly_chart(fig, width="stretch")` (como ya estás migrando).

---

## 15) Definición de “Done” (aceptación)

Se considera completado el MVP pro cuando:

1) Filtros globales aplican a KPIs + charts + tabla
2) Mes tiene opción “Todos” y Región neutral “Todas”
3) Tabs (mínimo 3) con contenido útil y consistente
4) Cache aplicado (dataset + al menos una agregación)
5) Export CSV funcional del dataset filtrado
6) Estados vacíos y errores de schema controlados (sin stacktrace)
7) Warning de `use_container_width` eliminado
8) Bug de columna `Region` vs `Región` eliminado
9) Tests unitarios agregados y pasando en `make check`

---

## 16) Backlog pro (post-MVP)

- Auth básica (password/env var, o SSO si existiera)
- Alertas (caída > X% vs periodo anterior)
- Drill-down (click en región/sku -> detalle)
- Persistencia de “views” en URL (si aplica)
- Integración real con Rails API
- Observabilidad: logging estructurado + “debug panel”
- Snapshot de reportes (pdf/csv programado)

---

## 17) Notas de implementación inmediata (del estado actual)

### Bugs/Issues detectados en logs
- Plotly error: `names="Region"` pero la columna es `Región`.
  - Fix: unificar nombres de columnas, idealmente definir constantes.

### Recomendación práctica
- Crear un módulo `schema.py` con:
  - `COL_MONTH = "Mes"`
  - `COL_REGION = "Región"`
  - `COL_SALES = "Ventas"`
  - `COL_CUSTOMERS = "Clientes"`
- Usar esas constantes en todo el proyecto para evitar typos.

---

## 18) Plan de ejecución sugerido (post-tutorial)

1) Consolidar filtros + dataset único para todo
2) Implementar tabs + separar pages/components
3) Implementar caching
4) Implementar export
5) Hardening: estados vacíos + schema validation
6) Tests
7) Pulido visual (theme + layout)

---

