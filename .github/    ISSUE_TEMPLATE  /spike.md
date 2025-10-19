---
name: 🧪 3. Historia de Spike (Investigación)
about: Para resolver la incertidumbre técnica o evaluar la viabilidad de una solución compleja.
title: "SPIKE-[ID]: INVESTIGACIÓN: [Pregunta de Ingeniería Clave]"
labels: ['P: High', 'Type: CHORE']
assignees: ['@username']
---

# 💡 Spike de Investigación y Descubrimiento

## 👤 Detalles del Flujo de Trabajo (Kanban)
| Campo | Valor |
| :--- | :--- |
| **Prioridad (Policy of Pull)** | P: [Highest | **High** | Medium | Low] |
| **Tipo de Investigación** | Type: [**TECH** (Tecnología/Herramienta) | **DESIGN** (Arquitectura/UML) | **FUNC** (Requisito no claro)] |
| **Módulo Impactado** | M_[**VISION** | **GAMEPLAY** | **UIX** | **SERVER** | **DEVOPS**] |
| **Tiempo Asignado (Time Box)** | [**4 Horas** / 1 Día / 2 Días] |
| **Dependencia (Bloqueado por)** | [ID de otro Spike si aplica, Ej: SPIKE-01] |

---

## 🎯 Alcance de la Investigación

### 1. Problema a Resolver (Contexto)
[Describe brevemente la incertidumbre o la pregunta que este Spike debe responder. Ej: No sabemos si el motor 'X' es compatible con la nueva librería de visión.]

### 2. Hipótesis / Objetivo
[El resultado que se espera obtener. Debe ser una pregunta de SÍ/NO o una decisión binaria.]
> **Objetivo:** Determinar si la librería **[Nombre]** puede procesar $[X]$ transacciones por segundo con una latencia inferior a $10\text{ms}$.

---

## ⚙️ Plan de Acción
[Lista de pasos detallados para realizar la investigación. Esto ayuda a mantener el Spike enfocado y dentro del 'Time Box'.]

- [ ] Instalar la herramienta/librería en el entorno de prueba.
- [ ] Crear un PoC mínimo para probar el [Punto Crítico].
- [ ] Medir y documentar las métricas de rendimiento (latencia, consumo de memoria).
- [ ] Analizar la documentación para identificar [Limitaciones o Licencias].

---

## 💡 Resultados de la Investigación (Conclusión del Hallazgo)

**Esta es la sección crucial que debe completarse antes de cerrar el Spike.**

| Campo | Valor (A Completar después de la investigación) |
| :--- | :--- |
| **Resultado de la Hipótesis** | [**SÍ** / **NO** / Necesita más investigación] |
| **Recomendación Resumida** | [**Usar la herramienta 'X'** / **Descartar la herramienta y usar 'Y'** / **Dividir la tarea en Z sub-tareas**] |
| **Estimación de Tareas FUTURAS** | [Estimación final del trabajo de implementación: **20 Puntos** / **3 Días** / **TBD**] |
| **Impacto Arquitectónico** | [Breve descripción de los módulos que se verán afectados por esta decisión.] |
| **Documentos/PRs generados** | [Enlace a cualquier código de PoC, diagrama o documento generado.] |

---

## 🗒️ Notas y Evidencia

[Incluir capturas de pantalla, fragmentos de código del PoC, y cualquier dato o métrica obtenida durante la investigación.]
