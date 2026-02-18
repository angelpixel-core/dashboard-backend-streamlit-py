---
stepsCompleted: [1, 2, 3, 4, 5, 6]
inputDocuments:
  - docs/seed/master-root.md
workflowType: 'research'
lastStep: 6
research_type: 'technical'
research_topic: 'Arquitectura profesional Streamlit con DDD + Hexagonal inspirada en Ruby'
research_goals: 'Definir stack y patrones para modularidad real, puertos/adaptadores, TDD, tooling explícito con uv/ruff/mypy/pytest/ptw, y separación dominio-aplicación-infra-presentación con UI reemplazable.'
user_name: 'Angel DevStack'
date: '2026-02-18'
web_research_enabled: true
source_verification: true
---

# Research Report: technical

**Date:** 2026-02-18
**Author:** Angel DevStack
**Research Type:** technical

---

## Research Overview

Investigación técnica orientada a diseñar un backend Streamlit mantenible,
modular y testeable, usando prácticas modernas del ecosistema Python en 2026,
con énfasis en DDD, arquitectura hexagonal, tipado estático y flujo TDD.

Metodología aplicada:

- Verificación con fuentes primarias (documentación oficial y estándares).
- Contraste multi-fuente para decisiones de stack.
- Priorización de decisiones explícitas (sin "magia" de tooling).

---

## Technical Research Scope Confirmation

**Research Topic:** Arquitectura profesional Streamlit con DDD + Hexagonal inspirada en Ruby
**Research Goals:** Definir stack y patrones para modularidad real, puertos/adaptadores, TDD, tooling explícito con uv/ruff/mypy/pytest/ptw, y separación dominio-aplicación-infra-presentación con UI reemplazable.

**Technical Research Scope:**

- Architecture Analysis - design patterns, frameworks, system architecture
- Implementation Approaches - development methodologies, coding patterns
- Technology Stack - languages, frameworks, tools, platforms
- Integration Patterns - APIs, protocols, interoperability
- Performance Considerations - scalability, optimization, patterns

**Research Methodology:**

- Current web data with rigorous source verification
- Multi-source validation for critical technical claims
- Confidence level framework for uncertain information
- Comprehensive technical coverage with architecture-specific insights

**Scope Confirmed:** 2026-02-18

## Technology Stack Analysis

### Programming Languages

Para este objetivo arquitectónico, Python sigue siendo el núcleo lógico por
madurez de tooling (typing, testing, lint/format, empaquetado moderno). La
documentación oficial vigente está en Python 3.14.x, y el typing estándar
incluye `Protocol`, pieza clave para diseñar puertos hexagonales sin acoplar
el dominio a infraestructura.

Para front interactivo, Streamlit mantiene el modelo Python-first, lo que
reduce fricción entre capa de presentación y capa de aplicación en equipos
backend.

_Popular Languages:_ Python es un lenguaje de uso ampliamente reportado en
encuestas de desarrolladores.
_Emerging Languages:_ En este contexto, el crecimiento más útil no es otro
lenguaje, sino fortalecer tipado y contratos en Python (Protocol + mypy).
_Language Evolution:_ Mayor peso de `pyproject.toml` y typing avanzado.
_Performance Characteristics:_ Python prioriza velocidad de desarrollo; para
cuellos de botella, se delega a componentes especializados o servicios.
_Source: https://docs.python.org/3/
_Source: https://docs.python.org/3/library/typing.html#typing.Protocol
_Source: https://survey.stackoverflow.co/2025/technology
### Development Frameworks and Libraries

Streamlit ofrece primitives claras para UI, estado de sesión, multipágina y
componentes personalizados (`st.components.v1.html`), lo que encaja con una
arquitectura donde presentación queda aislada del dominio.

Para apps de datos, `pandas` y `plotly` siguen siendo combinación estándar para
transformación + visualización. Para calidad de código, `ruff` unifica lint y
format, disminuyendo complejidad operacional.

_Major Frameworks:_ Streamlit para UI de dashboards Python-first.
_Micro-frameworks:_ Librerías orientadas a dominio (sin framework pesado en el core).
_Evolution Trends:_ Consolidación de tooling rápido (ruff/uv) en equipos Python.
_Ecosystem Maturity:_ Ecosistema maduro para testing, typing y data apps.
_Source: https://docs.streamlit.io/develop/api-reference
_Source: https://docs.streamlit.io/develop/concepts/multipage-apps
_Source: https://docs.streamlit.io/develop/api-reference/custom-components/st.components.v1.html
_Source: https://docs.astral.sh/ruff/configuration/
### Database and Storage Technologies

Para DDD + hexagonal, la recomendación es modelar repositorios como puertos y
decidir almacenamiento por adaptador. En práctica:

- SQLite para desarrollo/local y tests de integración rápidos.
- PostgreSQL para producción transaccional.
- Redis como cache/sesiones/eventos ligeros según necesidad.
- SQLAlchemy 2.x como capa técnica opcional en infraestructura.

_Relational Databases:_ PostgreSQL y SQLite cubren gran parte de casos CRUD/OLTP.
_NoSQL Databases:_ Redis entra como datastore de soporte de baja latencia.
_In-Memory Databases:_ Redis para cache y patrones pub/sub simples.
_Data Warehousing:_ No es prioridad inicial para este alcance, pero se puede
agregar vía adaptador analítico futuro.
_Source: https://www.postgresql.org/docs/current/
_Source: https://www.sqlite.org/index.html
_Source: https://redis.io/docs/latest/
_Source: https://docs.sqlalchemy.org/en/20/
### Development Tools and Platforms

El stack explícito recomendado para 2026 en este proyecto:

- `uv` para gestión de proyecto y dependencias (`pyproject.toml`).
- `ruff` como linter+formatter.
- `mypy` para contrato estático.
- `pytest` + `pytest-watch` para TDD y feedback rápido.

Esto minimiza tool sprawl y mejora reproducibilidad local/CI.

_IDE and Editors:_ VS Code/PyCharm siguen comunes, pero independientes del diseño.
_Version Control:_ Git + PR workflow estándar.
_Build Systems:_ `pyproject.toml` + uv como base moderna.
_Testing Frameworks:_ pytest como estándar de facto; watch mode con ptw.
_Source: https://docs.astral.sh/uv/concepts/projects/dependencies/
_Source: https://peps.python.org/pep-0621/
_Source: https://peps.python.org/pep-0735/
_Source: https://docs.pytest.org/en/stable/
_Source: https://pypi.org/project/pytest-watch/
_Source: https://mypy.readthedocs.io/en/stable/config_file.html#strict
### Cloud Infrastructure and Deployment

Para despliegue, Streamlit puede ejecutarse en su entorno administrado o en
infra propia containerizada. Patrón recomendado para hexagonal:

- App empaquetada en contenedor.
- Configuración por entorno (12-factor).
- Observabilidad y health checks desde infraestructura.

_Major Cloud Providers:_ AWS/Azure/GCP viables al contenerizar la app.
_Container Technologies:_ Docker como estándar base.
_Serverless Platforms:_ viable para componentes adyacentes; Streamlit suele ir
mejor como servicio continuo.
_CDN and Edge Computing:_ útil para assets/API gateway, menos crítico en MVP.
_Source: https://docs.streamlit.io/deploy
_Source: https://docs.docker.com/get-started/
_Source: https://kubernetes.io/docs/concepts/overview/
### Technology Adoption Trends

Patrones de adopción relevantes para este proyecto:

- Consolidación de configuración en `pyproject.toml`.
- Preferencia por herramientas unificadas y rápidas (`uv`, `ruff`).
- Mayor exigencia de typing estricto y test automation en equipos backend.
- En UI Python, Streamlit acelera entrega cuando el foco es valor de negocio,
no front-end SPA complejo.

_Migration Patterns:_ de stacks dispersos a pipeline compacto y explícito.
_Emerging Technologies:_ más foco en DX, velocidad de CI y contratos de tipos.
_Legacy Technology:_ setups múltiples (varios linters/formatters) tienden a
reducirse.
_Community Trends:_ Python y tooling de productividad mantienen fuerte tracción.
_Source: https://survey.stackoverflow.co/2025/technology
_Source: https://docs.astral.sh/uv/
_Source: https://docs.astral.sh/ruff/
_Source: https://docs.streamlit.io/develop/quick-reference/release-notes
---

<!-- Content will be appended sequentially through research workflow steps -->

## Integration Patterns Analysis

### API Design Patterns

Para esta arquitectura (Streamlit + DDD + hexagonal), conviene separar APIs
externas de la UI: la UI llama servicios de aplicación, y los adaptadores
salientes consumen APIs HTTP/RPC. En HTTP, la base semántica vigente está en
RFC 9110. Para contratos HTTP, OpenAPI ya tiene versión publicada `3.2.0`
(19 Sep 2025), útil para estandarizar request/response, versionado y tooling.

GraphQL aporta endpoint único y contrato flexible; su guía oficial de serving
recomienda POST obligatorio y GET opcional para queries, y alinea con el draft
GraphQL-over-HTTP para interoperabilidad.

_RESTful APIs:_ ideales para integración estable entre bounded contexts.
_GraphQL APIs:_ útiles en lectura agregada cuando hay múltiples vistas.
_RPC and gRPC:_ fuerte opción para latencia y contratos tipados entre servicios.
_Webhook Patterns:_ para eventos de dominio hacia sistemas externos.
_Source: https://www.rfc-editor.org/rfc/rfc9110
_Source: https://spec.openapis.org/oas/latest.html
_Source: https://graphql.org/learn/serving-over-http/
_Source: https://graphql.github.io/graphql-over-http/draft/
### Communication Protocols

gRPC mantiene ventaja para comunicación interna de alto throughput con
streaming bidireccional sobre transporte HTTP/2, y metadata estructurada.
WebSocket sigue siendo opción estándar para flujos full-duplex en UI realtime
(RFC 6455), incluyendo bootstrapping sobre HTTP/2 vía RFC 8441.

Para integración asíncrona, AMQP 1.0 y MQTT 5.0 siguen vigentes como
estándares OASIS.

_HTTP/HTTPS Protocols:_ base interoperable para integraciones de negocio.
_WebSocket Protocols:_ canal bidireccional para updates en tiempo real.
_Message Queue Protocols:_ AMQP/MQTT para desacople y resiliencia.
_grpc and Protocol Buffers:_ integración tipada, performante y multi-lenguaje.
_Source: https://grpc.io/about/
_Source: https://grpc.io/docs/guides/metadata/
_Source: https://www.rfc-editor.org/info/rfc6455
_Source: https://www.rfc-editor.org/rfc/rfc8441
_Source: https://docs.oasis-open.org/amqp/core/v1.0/amqp-core-complete-v1.0.pdf
_Source: https://www.oasis-open.org/standard/mqtt-v5-0/
### Data Formats and Standards

JSON sigue siendo el formato dominante para APIs HTTP y GraphQL. Para payloads
compactos y contratos estrictos, Protobuf aporta eficiencia binaria. AsyncAPI
3.1.0 aporta descripción formal para APIs orientadas a eventos, complementando
OpenAPI en arquitecturas híbridas sync/async.

_JSON and XML:_ JSON domina en APIs modernas; XML persiste en legados.
_Protobuf and MessagePack:_ Protobuf destaca cuando el costo de serialización importa.
_CSV and Flat Files:_ útil para cargas batch y export/import operacional.
_Custom Data Formats:_ evitar salvo necesidad fuerte; priorizar estándares.
_Source: https://www.asyncapi.com/docs/reference/specification/latest
_Source: https://protobuf.dev/
_Source: https://spec.openapis.org/oas/latest.html
### System Interoperability Approaches

Para tu objetivo de UI reemplazable, la práctica clave es definir puertos de
aplicación (Protocol/interfaces) y mantener Streamlit como adaptador de entrada.
Interoperabilidad externa se resuelve con adaptadores dedicados (REST/gRPC/
mensajería), no desde el dominio.

_Point-to-Point Integration:_ rápido para MVP, pero escala peor en complejidad.
_API Gateway Patterns:_ útil cuando crecen consumidores y políticas transversales.
_Service Mesh:_ aporta mTLS, observabilidad y políticas de red en runtime.
_Enterprise Service Bus:_ puede servir en entornos legacy, pero suele aumentar acoplamiento.
_Source: https://istio.io/latest/about/service-mesh/
_Source: https://kubernetes.io/docs/reference/using-api/
### Microservices Integration Patterns

Si evoluciona a microservicios, Saga es patrón clave para consistencia eventual
entre bounded contexts. Choreography funciona bien con pocos participantes;
orchestration mejora control cuando hay más pasos y compensaciones.

_API Gateway Pattern:_ encapsula auth/rate-limit/routing.
_Service Discovery:_ esencial cuando aumentan servicios y despliegues.
_Circuit Breaker Pattern:_ protege experiencia ante degradaciones de downstream.
_Saga Pattern:_ transacciones distribuidas con compensación.
_Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga.html
_Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html
_Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-orchestration.html
### Event-Driven Integration

Para desacople real entre módulos, conviene publicar eventos de dominio y
traducirlos en adaptadores a brokers/protocolos externos. CloudEvents v1.0.2
ayuda a estandarizar metadatos entre plataformas y evita contratos ad hoc.

_Publish-Subscribe Patterns:_ desacople temporal y organizacional.
_Event Sourcing:_ opcional, útil si necesitas auditoría y replay detallado.
_Message Broker Patterns:_ AMQP/MQTT según requerimientos de routing y footprint.
_CQRS Patterns:_ útil cuando lectura/escritura divergen fuertemente.
_Source: https://github.com/cloudevents/spec
_Source: https://www.asyncapi.com/docs/reference/specification/latest
_Source: https://www.oasis-open.org/standard/mqtt-v5-0/
### Integration Security Patterns

En APIs HTTP, OAuth 2.0 sigue siendo referencia normativa para autorización, y
mTLS en OAuth (RFC 8705) fortalece autenticación de clientes y token binding.
En plano de red interno, service mesh con mTLS añade defensa en profundidad.

_OAuth 2.0 and JWT:_ base común para autorización API.
_API Key Management:_ válido para integraciones simples, con rotación y scopes.
_Mutual TLS:_ recomendado para integraciones críticas B2B o service-to-service.
_Data Encryption:_ TLS en tránsito y cifrado en reposo como baseline.
_Source: https://www.rfc-editor.org/rfc/rfc6749
_Source: https://www.rfc-editor.org/rfc/rfc8705
_Source: https://istio.io/latest/about/service-mesh/

## Architectural Patterns and Design

### System Architecture Patterns

El patrón más sólido para tu objetivo es hexagonal (ports & adapters): núcleo
aplicativo independiente de UI y base de datos, con adaptadores reemplazables.
Esto alinea exactamente con la recomendación original de poder testear en
aislamiento y desacoplar runtime devices.

En evolución de legado, Strangler Fig (actualizado por Fowler en 2024) aporta
ruta incremental de bajo riesgo: convivir legado+nuevo, extraer capacidades por
seams y mover comportamiento de forma progresiva.

_Source: https://alistair.cockburn.us/hexagonal-architecture
_Source: https://martinfowler.com/bliki/StranglerFigApplication.html
### Design Principles and Best Practices

DDD estratégico refuerza separación por bounded contexts para evitar un modelo
único monolítico y mantener lenguaje ubicuo por subdominio. Para diseño
microservicios/servicios modulares, Microsoft Learn mantiene el enfoque de
bounded context + patrones tácticos dentro de cada contexto.

Para tu caso, la frontera correcta es: dominio puro (sin Streamlit),
aplicación orquestadora de casos de uso, infraestructura con adaptadores y
presentación Streamlit como driver adapter.

_Source: https://martinfowler.com/bliki/BoundedContext.html
_Source: https://learn.microsoft.com/en-us/azure/architecture/microservices/model/domain-analysis
_Source: https://learn.microsoft.com/en-us/azure/architecture/microservices/model/tactical-ddd
### Scalability and Performance Patterns

La ejecución de Streamlit (rerun) exige decisiones explícitas de performance:
cachear computación y recursos, y usar session state para estado por sesión.
El modelo oficial indica reruns frecuentes ante interacción/cambio de código,
por lo que el diseño debe minimizar recomputación costosa.

_Source: https://docs.streamlit.io/develop/concepts/architecture/caching
_Source: https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
_Source: https://docs.streamlit.io/develop/api-reference/execution-flow
### Integration and Communication Patterns

Con crecimiento de complejidad, OpenAPI para contratos HTTP y AsyncAPI para
canales asíncronos reducen ambigüedad entre equipos. Para migraciones graduales,
una estrategia refactor/rearchitect debe ser explícita por workload y driver
de negocio.

_Source: https://spec.openapis.org/oas/latest.html
_Source: https://www.asyncapi.com/docs/reference/specification/latest
_Source: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/select-cloud-migration-strategy
### Security Architecture Patterns

ASVS 5.0.0 (30 mayo 2025) entrega baseline actual para controles de aplicación.
Para integraciones y despliegues, combinar OAuth2/mTLS, gestión de secretos por
entorno y verificación de supply chain incrementa resiliencia.

_Source: https://owasp.org/www-project-application-security-verification-standard/
_Source: https://www.rfc-editor.org/rfc/rfc6749
_Source: https://www.rfc-editor.org/rfc/rfc8705
_Source: https://slsa.dev/
### Data Architecture Patterns

Mantener persistencia como puerto permite alternar SQLite (local/tests),
PostgreSQL (producción) y cache/colas ligeras sin contaminar dominio.
La decisión de modelo de datos queda en infraestructura, con contratos estables
hacia aplicación/dominio.

_Source: https://www.postgresql.org/docs/current/
_Source: https://www.sqlite.org/index.html
_Source: https://redis.io/docs/latest/
### Deployment and Operations Architecture

En operación cloud-native, probes de Kubernetes (liveness/readiness/startup)
son controles fundamentales para disponibilidad y recuperación. Para entrega,
GitOps v1.0.0 aporta principios operativos claros (declarativo, versionado
inmutable, pull automático, reconciliación continua).

_Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
_Source: https://opengitops.dev/

## Implementation Approaches and Technology Adoption

### Technology Adoption Strategies

Para este proyecto, la estrategia recomendada es incremental (Strangler) por
módulos y contextos, evitando migraciones big-bang. Esta ruta minimiza riesgo,
permite validación temprana y conserva continuidad operativa.

_Source: https://martinfowler.com/bliki/StranglerFigApplication.html
_Source: https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/select-cloud-migration-strategy
### Development Workflows and Tooling

Workflow técnico recomendado:

- `uv` para entornos/deps reproducibles vía `pyproject.toml`
- `ruff` para lint+format unificado
- `mypy --strict` para contratos de tipos
- `pytest` para suites unit/integration
- CI en GitHub Actions para validación automática por PR

_Source: https://docs.astral.sh/uv/
_Source: https://docs.astral.sh/ruff/
_Source: https://mypy.readthedocs.io/en/stable/config_file.html#strict
_Source: https://docs.pytest.org/en/stable/
_Source: https://docs.github.com/actions/automating-builds-and-tests/building-and-testing-python
### Testing and Quality Assurance

TDD-ready implica pirámide clara:

- unit tests sobre dominio puro (sin Streamlit)
- integration tests sobre adaptadores
- tests de presentación con mocks/fakes de puertos

Para endurecimiento, incorporar controles de seguridad de workflows CI/CD.

_Source: https://docs.pytest.org/en/stable/
_Source: https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions
### Deployment and Operations Practices

Operación confiable requiere:

- probes de salud (liveness/readiness/startup)
- autoscaling según carga
- observabilidad con trazas/métricas/logs
- prácticas SRE con SLO/error budgets

_Source: https://kubernetes.io/docs/concepts/configuration/liveness-readiness-startup-probes/
_Source: https://kubernetes.io/docs/concepts/workloads/autoscaling/horizontal-pod-autoscale/
_Source: https://opentelemetry.io/docs/concepts/signals/
_Source: https://sre.google/workbook/error-budget-policy/
### Team Organization and Skills

Asignar ownership por módulo y capa (domain/application/infrastructure/
presentation) acelera decisiones y evita zonas grises. `CODEOWNERS` formaliza
responsabilidad y revisión experta.

_Source: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners
### Cost Optimization and Resource Management

Diseño consciente de costos desde inicio: right-sizing, autoscaling y control
de recursos/caché por entorno. Baseline recomendado: pilar de optimización de
costos de Well-Architected.

_Source: https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html
### Risk Assessment and Mitigation

Riesgos principales detectados:

- Acoplamiento accidental del dominio con Streamlit
- Deuda de testing en adaptadores
- Superficie de ataque en CI/CD y supply chain
- Observabilidad insuficiente para producción

Mitigaciones:

- Puertos explícitos con `Protocol`
- Gates de calidad (lint/type/test) en CI
- Hardening de GitHub Actions
- Baseline de seguridad ASVS + prácticas SLSA

_Source: https://owasp.org/www-project-application-security-verification-standard/
_Source: https://slsa.dev/
_Source: https://docs.github.com/en/actions/how-tos/security-for-github-actions/security-guides/security-hardening-for-github-actions
## Technical Research Recommendations

### Implementation Roadmap

1. Establecer estructura hexagonal y contratos de puertos
2. Configurar tooling (`uv`, `ruff`, `mypy`, `pytest`, `pytest-watch`)
3. Implementar primer módulo de dominio con TDD
4. Conectar adaptador Streamlit como driver de casos de uso
5. Incorporar observabilidad y pipeline CI/CD endurecido

### Technology Stack Recommendations

- Python + Streamlit para capa de presentación/data app
- Dominio puro con `dataclasses` + `Protocol`
- Persistencia desacoplada (SQLite local, PostgreSQL prod, Redis opcional)
- Tooling unificado en `pyproject.toml`

### Skill Development Requirements

- DDD táctico/estratégico
- diseño de puertos/adaptadores
- testing por capas
- observabilidad y seguridad operativa

### Success Metrics and KPIs

- % cobertura de dominio y adaptadores
- tiempo medio de feedback en CI
- defectos de integración por release
- cumplimiento de gates (lint/type/test)
- estabilidad operacional (SLO/error budget)


## Execution Blueprint Artifacts

Este research se traduce en los siguientes entregables ejecutables:

- Implementation Blueprint:
  `_bmad-output/planning-artifacts/research/implementation-blueprint-dashboard-streamlit-2026-02-18.md`
- Architecture Decision Record (ADR-0001):
  `_bmad-output/planning-artifacts/research/adr/0001-streamlit-adapter-hexagonal-protocol.md`

Estos artefactos incluyen:

- estructura final de carpetas
- `pyproject.toml` definitivo
- tooling mínimo viable
- checklist de implementación por commit
- Definition of Done
- decisiones formales de arquitectura y estrategia de reemplazo de UI


# Comprehensive Technical Synthesis

## Executive Summary

La investigación confirma que la opción más robusta para este repositorio es:
**DDD + Hexagonal** con **Streamlit como adaptador de presentación**. Esta
estrategia maximiza testabilidad, reduce lock-in y habilita reemplazo futuro de
UI sin reescribir dominio ni casos de uso.

El cierre práctico del research queda materializado en dos entregables
operativos:

- Implementation Blueprint ejecutable por fases
- ADR-0001 con decisiones, riesgos y mitigaciones

## Table of Contents

1. Technical Research Introduction and Methodology
2. Technical Landscape and Architecture Analysis
3. Implementation Approaches and Best Practices
4. Technology Stack Evolution and Trends
5. Integration and Interoperability Patterns
6. Performance and Scalability Analysis
7. Security and Compliance Considerations
8. Strategic Technical Recommendations
9. Implementation Roadmap and Risk Assessment
10. Future Technical Outlook and Innovation Opportunities
11. Technical Research Methodology and Source Documentation
12. Technical Appendices and Reference Materials

## Strategic Technical Recommendations

1. Mantener `domain` y `application` libres de dependencias de Streamlit.
2. Definir puertos con `Protocol` y adaptadores explícitos por infraestructura.
3. Consolidar tooling en `pyproject.toml` con `uv`, `ruff`, `mypy`, `pytest`.
4. Exigir gates de calidad por PR: lint, type-check y tests.
5. Ejecutar implementación por commits atómicos según blueprint.

## Implementation Roadmap and Risk Assessment

Roadmap y secuencia de commits ya definidos en:

- `_bmad-output/planning-artifacts/research/implementation-blueprint-dashboard-streamlit-2026-02-18.md`

Decisiones de arquitectura y riesgos de lock-in formalizados en:

- `_bmad-output/planning-artifacts/research/adr/0001-streamlit-adapter-hexagonal-protocol.md`

## Technical Research Conclusion

Research completado con traducción a plan ejecutable para este repositorio.
La fase siguiente recomendada es iniciar Fase 1 (estructura) + Fase 2
(pyproject/tooling) en una rama de bootstrap con commits granulares.

**Technical Research Completion Date:** 2026-02-18
**Workflow Status:** Completed

