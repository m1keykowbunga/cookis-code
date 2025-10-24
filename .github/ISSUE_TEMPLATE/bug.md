---
name: 🐞 2. Reporte de Bug / Caso de Prueba Fallido
about: Para reportar y documentar fallos en el software y su corrección.
title: "[BUG] M_MODULO: Breve descripción del comportamiento incorrecto"
labels: ['Type: Bug']
assignees: ['@username']

---

# 🐞 Reporte Detallado del Bug

## 👤 Información General del Fallo (Metadatos)

| Campo | Valor |
| :--- | :--- |
| **Severidad (S:)** | [Bloqueador | Crítico | Mayor | Menor | Trivial] |
| **Módulo Afectado (M_)** | [VISION | GAMEPLAY | UIX | DATA | SERVER] |
| **Versión/Commit** | [Versión o Commit Hash donde se encontró el error] |
| **Plataforma/SO** | [Ej: Windows 11, iOS 17, Chrome 120] |
| **Relacionado con RF/RN** | [ID del Requisito violado, Ej: **RF-01** o **RN-03**] |
| **Estimación (puntos/horas)** | [Dejar TBD inicialmente. Se completa en la fase de 'To Do'] |

---
> ## :feet: 💻**Trazabilidad del Cambio**
>* **Archivos Modificados:** `game_engine.py` (método `run`), `settings.py` (nueva `Enum`).
>* **Prueba Rápida:** Al presionar 'Enter' en el estado `MENU`, el estado debe cambiar a `PLAYING` y el *player* debe aparecer.
>* **Pull Request Fusionado:** `#47`
>* **Commit Hash de Fusión:** `h1i2j3k4l5m6n7o8`
>* **Acción Final:** Tarea **FEAT-12** cerrada y movida a **Done**.

---

## 🔬 Caso de Prueba 

### 📝 1. Pre-condiciones
[Condiciones que deben cumplirse antes de intentar la reproducción. Ej: Usuario logueado como Admin.]
* [Pre-condición 1]
* [Pre-condición 2]

### ⚙️ 2. Pasos para Reproducir
[Guía **clara y numerada** de las acciones exactas para replicar el error. Usa pasos simples y directos.]
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

### ❌ 3. Resultado Observado (Actual)
[Lo que el sistema HACE. Describe el comportamiento inesperado/erróneo.]
> **[Descripción clara del fallo: El sistema se bloquea, el valor es incorrecto, etc.]**

### ✅ 4. Resultado Esperado (Correcto)
[Lo que el sistema DEBERÍA hacer según los requisitos **RF-01**.]
> [Descripción de la acción correcta que debe realizar el sistema.]

---

## 🛠️ Logs y Evidencia

[Incluye logs, stack traces o capturas de pantalla relevantes. Usa el bloque de código para logs.]

```bash
# INSERTAR STACK TRACE O MENSAJES DE ERROR RELEVANTES AQUÍ
