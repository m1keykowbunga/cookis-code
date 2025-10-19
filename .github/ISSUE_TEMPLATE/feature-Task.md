---
name: 🚀 1. Feature / Task (Implementación)
about: Para implementar nuevas funcionalidades, refactorización de código o tareas de infraestructura.
title: "[**RF 1**ID tarea**]: [TIPO](MODULO): Título Conciso"
labels: ['P: Medium', 'Type: Feat']
assignees: ['@username']
---
# 📋 Task (issus)

# 👤 Detalles Generales
| Campo | Valor |
| :--- | :--- |
| **Prioridad (Policy of Pull)** | P: [Highest | High | Medium | Low] |
| **Tipo** | Type: [FEAT | REFACTOR | CHORE] |
| **Módulo Principal** | M_[VISION | GAMEPLAY | UIX | CONFIG] |
| **Esfuerzo Estimado** | [Puntos de Historia o Horas] |
| **Dependencia (Bloqueado por)** | [ID de otro Issue si aplica, Ej: SPIKE-03] |

---


# ⚙️ Especificación Formal 

## 📝 Requisitos Funcional (RF) 

| **Número del Requisito** | **RF-01** |
| :--- | :--- |
| **Nombre del Requisito** | Visualización del catálogo de productos |
| **Tipo** | Requisito |
| **Fuente del Requisito** | Reuniones con las partes interesadas en el proyecto |
| **Prioridad del Requisito** | Alta/Esencial |
| **Descripción** | El sistema debe mostrar a los clientes un catálogo completo de los productos disponibles. |

---



## 📚 Historia de Usuario  

| Atributo | Valor Requerido |
| :--- | :--- |
| **Rol (COMO)** | [Ej: Jugador, Administrador del sistema, Usuario Nuevo] |
| **Meta (QUIERO)** | [La acción que se desea realizar, Ej: que la cámara detecte mi mano] |
| **Beneficio (PARA)** | [La razón o valor del negocio, Ej: poder mover mi nave sin teclado] |
| **Prioridad (MoSCoW)**| [Ej: **Must Have** (Esencial para el PoC)] |
| **Issue ID Relacionado** | [El Issue de Desarrollo (DEV-XX) o Diseño (DGN-XX) que implementará esta Story] |

---

## 📝 Objetivo Técnico
**Crear y subir un Diagrama UML simple (o de Componentes) que muestre las relaciones entre las clases principales del núcleo del juego (Player, Enemy, Bullet, GameEngine) para estandarizar la arquitectura.**

## ⚙️ Tareas Técnicas
[Checklist detallado de implementación para el desarrollador.]
- [ ] Crear la rama de trabajo `feature/ID-nombre-corto`.
- [ ] Implementar la lógica en `[Archivo.py]`.
- [ ] Documentar el código con *docstrings*.

## ✅ Criterios de Aceptación (DoD - IEEE 830 Verificabilidad)
[La tarea es 'Done' solo si se cumplen todos los criterios. Deben ser verificables.]
1.  **Funcional:** [Ej: El movimiento de la nave es preciso y sin lag.]
2.  **Rendimiento:** [Métricas obligatorias - Ej: Latencia máxima de 50ms; FPS > 60.]
3.  **Trazabilidad:** El PR debe referenciar este ID y el Log de Trazabilidad debe estar completo.

---

### 📐 Referencia de Arquitectura (UML - Nuevo)
Obligatorio: Mencione o enlace el diagrama relevante.

   >Diagramas y capturas de pantalla de los compunestes o template completo
---

## 💾 Documentación de Trazabilidad del Cambio (POST-FUSIÓN)

**Esta sección se completa ÚNICAMENTE después de que la tarea haya sido fusionada y verificada.** Sirve como un registro final, estandarizado y trazable.

| Campo | Valor (A Completar por el Responsable de Cierre) |
| :--- | :--- |
| **Rama de Desarrollo (Origen)** | [Ej: `feature/ID-nombre-corto`] |
| **Pull Request (PR) Fusionado** | [Número del PR que cerró este Issue, Ej: **#47**] |
| **Commit Hash de Fusión** | [El hash final del merge. Ej: `h1i2j3k4l5m6n7o8`] |
| **Archivos Modificados o Creados** | [Ej: `product_view.js`, `api/catalog.py`, `tests/test_catalog.py`] |
| **Prueba Rápida de Verificación (QA)** | [La prueba de validación final en el entorno de Staging/Prod.] |
| **Responsable de Cierre (DEV)** | [👤 @username] |
| **Fecha de Cierre** | [📅 YYYY-MM-DD] |

---

## 🔄 Historial y Evidencia de Trazabilidad 


👤 **Responsable:** DEV – mk  
📅 **Fecha de Ejecución:** 2025-10-09  


### 📘 Historial y Evidencia de Trazabilidad

| Fecha | Acción / Cambio de Estado | Evidencia / Comentarios |
|:------|:--------------------------|:-------------------------|
| 2025-10-09 02:30 PM | Ready → Done  | esta plantilla esta integrado para ser usada en la seccion de comentarios; es copiar y pegar. sirve como un control y estandarizacion estos, ademas como elemento para contextualizar a los demas integrantes|
