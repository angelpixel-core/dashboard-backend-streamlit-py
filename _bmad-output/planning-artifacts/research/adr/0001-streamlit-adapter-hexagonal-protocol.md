# ADR-0001: Streamlit como adaptador, arquitectura hexagonal y puertos con Protocol

- Fecha: 2026-02-18
- Estado: Accepted
- Contexto: `dashboard-backend-streamlit-py`

## Contexto

El repositorio busca modularidad real, TDD, separación estricta de capas y
capacidad futura de reemplazar la UI sin reescribir dominio.

## Decisiones

### 1. Streamlit es adaptador y no core

- La lógica de negocio vive en `domain` y `application`.
- Streamlit vive en `presentation/streamlit` como driver adapter.
- Beneficio: la UI puede cambiar sin romper casos de uso ni dominio.

### 2. Se adopta arquitectura hexagonal

- Los casos de uso dependen de puertos, no de frameworks.
- Infraestructura y UI son detalles intercambiables.
- Beneficio: testabilidad alta, acoplamiento bajo, evolución incremental.

### 3. Los puertos se definen con `Protocol`

- `Protocol` permite contratos estructurales tipados en Python.
- Adaptadores cumplen interfaz sin herencia obligatoria.
- Beneficio: flexibilidad de implementación con verificación estática (`mypy`).

## Riesgos de lock-in

1. Lock-in de UI si Streamlit invade `domain` o `application`.
2. Lock-in de persistencia si SQL/ORM se filtra a entidades.
3. Lock-in operativo si build/deploy dependen de vendor específico.

## Mitigaciones

1. Regla de imports por capa + tests de arquitectura.
2. Repositorios como puertos, SQL solo en `infrastructure`.
3. Configuración declarativa y entorno reproducible con `uv`.

## Estrategia de reemplazo de UI

1. Mantener casos de uso como API interna estable.
2. Encapsular `session_state` en un módulo de adapter (`state.py`).
3. Evitar tipos/objetos Streamlit fuera de `presentation`.
4. Introducir nuevo adapter (FastAPI/CLI/React backend) contra mismos puertos.
5. Correr suite de tests existente para validar paridad funcional.

## Consecuencias

- Positivas: mantenibilidad, testabilidad y capacidad de evolución.
- Negativas: más estructura inicial y disciplina de boundaries.
- Trade-off aceptado por objetivo de escalabilidad técnica del proyecto.
