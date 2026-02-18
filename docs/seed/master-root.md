---
id: master-root
aliases: []
tags: []
---

Querés:
	•	DDD
	•	Arquitectura hexagonal (ports & adapters)
	•	Modularidad tipo Ruby
	•	TDD real
	•	Linter + formatter
	•	Watch mode para tests
	•	Estructura extraíble / copiable
	•	Setup entendible, no magia

⸻

🧠 Equivalencias Ruby → Python

Ruby module ≈ Python package + module + mixins con clases base

En Python:
	•	Namespace = carpeta con __init__.py
	•	Módulo = archivo .py
	•	Mixin = clase que se hereda múltiple
	•	Callbacks tipo Rails = decorators / hooks / signals
	•	DSL tipo Capybara = API fluida orientada a objetos
	•	Watch tests = pytest-watch
	•	Capybara equivalente = pytest + playwright
	•	Linter moderno = ruff
	•	Formatter = ruff format (reemplaza black)
	•	Type safety = mypy o pyright

Streamlit permite:
	•	st.components.v1.html() para inyectar HTML/CSS/JS
	•	Custom components
	•	Event handling vía state

⸻

PROMPT

Quiero que estructures este proyecto de Streamlit con
un enfoque profesional inspirado en Ruby + DDD + Hexagonal Architecture.

1️⃣ Primero: NO ejecutes nada.

Primero generá un plan detallado que incluya:
	•	Estructura de carpetas
	•	Separación por dominio
	•	Capa de aplicación
	•	Capa de infraestructura
	•	Capa de presentación (Streamlit)
	•	Ubicación de tests
	•	Herramientas de linting y formatting
	•	Herramientas de testing
	•	Modo watch para tests
	•	Estrategia de inyección de dependencias
	•	Cómo implementar mixins estilo Ruby
	•	Cómo diseñar puertos y adaptadores
	•	Cómo manejar eventos y state en Streamlit
	•	Cómo permitir extensión futura con HTML custom

Explicá cada decisión.
No generes código todavía.

⸻

2️⃣ Objetivos arquitectónicos
	•	Modularidad real (extraíble como package interno)
	•	Namespaces claros por dominio
	•	Aplicar SOLID
	•	Arquitectura hexagonal
	•	Separar dominio puro de infraestructura
	•	Permitir testear dominio sin Streamlit
	•	Permitir cambiar Streamlit por otra UI

⸻

3️⃣ Estilo de código
	•	Máximo 80 caracteres por línea (no más de 100)
	•	Docstrings en triple comillas estilo Google
	•	Tipado estático obligatorio
	•	Uso de dataclasses cuando tenga sentido
	•	Uso de Protocol para definir puertos
	•	Mixins vía multiple inheritance
	•	Evitar funciones globales

⸻

4️⃣ Tooling requerido

Configurar:
	•	ruff (linter + formatter)
	•	mypy (type checking)
	•	pytest
	•	pytest-watch
	•	cobertura de tests
	•	Makefile con comandos:
	•	make lint
	•	make format
	•	make test
	•	make test-watch
	•	make run

Todo configurado desde pyproject.toml.

⸻

5️⃣ Testing
	•	TDD-ready
	•	tests/unit
	•	tests/integration
	•	fixtures organizadas
	•	testear dominio sin Streamlit
	•	testear presentación con mocks

Opcional: proponer integración con Playwright Python.

⸻

6️⃣ Flujo de desarrollo esperado

Explicar cómo sería:
	•	Crear nuevo módulo de dominio
	•	Agregar nuevo adaptador
	•	Agregar nueva página Streamlit
	•	Escribir test primero
	•	Ejecutar tests en watch mode

⸻

7️⃣ Estructura esperada (orientativa)

Algo similar a:
```txt
src/
  dashboard/
    domain/
    application/
    infrastructure/
    presentation/
tests/
```

Pero proponé la mejor variante según buenas prácticas 2026.

⸻

8️⃣ Después del plan

Una vez aprobado el plan:
	•	Generar estructura de carpetas
	•	Generar archivos base
	•	Configurar tooling
	•	Generar Makefile
	•	Agregar primer ejemplo de dominio simple
	•	Agregar primer test
	•	Confirmar que todo corre

⸻

9️⃣ No usar setuptools.

Usar uv + pyproject.toml moderno.

⸻

🔟 Importante

Explicar cada herramienta que agregues y por qué.
No usar magia implícita.
Todo debe ser explícito y entendible.

⸻

🚀 Extra: si querés más Ruby vibes

Después podemos pedirle que:
	•	Cree un mini DSL tipo:
DashboardPage.title("Ventas").chart(data)
	•	Agregue sistema de hooks tipo before_render
	•	Cree una capa tipo “Components” reutilizable

⸻

