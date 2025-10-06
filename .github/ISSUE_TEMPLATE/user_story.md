---
name: 📚 Historia de Usuario (STORY) - Formal
about: Para definir un requisito funcional clave aplicando la estructura de IEEE 830 (Función, Desempeño, Criterios).
title: "[STORY] Como X, quiero Y, para Z"
labels: Requisito, Diseño, needs-triage
assignees: ''
---

## 📝 1. Definición del Requisito (USER STORY)

| Atributo | Valor Requerido |
| :--- | :--- |
| **Rol (COMO)** | [Ej: Jugador, Administrador del sistema, Usuario Nuevo] |
| **Meta (QUIERO)** | [La acción que se desea realizar, Ej: que la cámara detecte mi mano] |
| **Beneficio (PARA)** | [La razón o valor del negocio, Ej: poder mover mi nave sin teclado] |
| **Prioridad (MoSCoW)**| [Ej: **Must Have** (Esencial para el PoC)] |
| **Issue ID Relacionado** | [El Issue de Desarrollo (DEV-XX) o Diseño (DGN-XX) que implementará esta Story] |

## ⚙️ 2. Especificación Formal (IEEE 830)

### 2.1. Requisito Funcional (Función)
| Tipo | Identificador | Descripción de la Tarea |
| :---: | :---: | :--- |
| **FUN** | [Ej: FUN-001] | [Describe exactamente lo que el sistema debe hacer, Ej: El sistema debe calcular la posición X e Y del objeto detectado en el plano de la cámara.] |

### 2.2. Requisito de Desempeño (Performance)
| Tipo | Identificador | Criterio de Medición |
| :---: | :---: | :--- |
| **PERF** | [Ej: PERF-001] | La detección y movimiento de la nave debe tener una latencia menor a **150 ms** para asegurar una jugabilidad fluida. |

### 2.3. Criterios de Aceptación y Pruebas (DoD)
[Describe los pasos que el QA debe seguir para confirmar que la funcionalidad está completa.]

| # | Escenario / Condición de Prueba | Resultado Esperado |
| :---: | :--- | :--- |
| **1** | [Ej: El jugador mueve su mano hacia el límite derecho de la pantalla.] | [Ej: La nave alcanza la posición X máxima y se detiene, sin errores.] |
| **2** | [Ej: El jugador ejecuta el gesto de disparo.] | [Ej: Se instancia un proyectil en la posición central de la nave en un tiempo < 100ms.] |

## 🔗 3. Relación con Documentos Externos
[Si este requisito afecta la Arquitectura (DEV-02) o el Wireframe (DGN-02), dejar el enlace aquí.]