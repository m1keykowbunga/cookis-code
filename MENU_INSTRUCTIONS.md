# Sistema de Menú - Space Invaders Origami

## Descripción
Se ha implementado un sistema de menú completo para el juego Space Invaders Origami que permite:
- Iniciar una nueva partida
- Reiniciar la partida actual
- Navegar entre opciones
- Salir del juego

## Características del Menú

### Estados del Juego
1. **MENU**: Pantalla principal con opciones de juego
2. **PLAYING**: Estado de juego activo
3. **GAME_OVER**: Pantalla de fin de partida

### Controles
- **W/S**: Navegar hacia arriba/abajo en las opciones del menú
- **ESPACIO/ENTER**: Seleccionar la opción actual
- **Q**: Salir del juego en cualquier momento

### Opciones del Menú Principal
- **JUGAR**: Inicia una nueva partida
- **SALIR**: Cierra el juego

### Opciones de Game Over
- **REINICIAR**: Reinicia la partida actual con el mismo estado inicial
- **MENU PRINCIPAL**: Regresa al menú principal
- **SALIR**: Cierra el juego

## Funcionalidades Implementadas

### 1. Sistema de Estados
- Control de flujo entre diferentes pantallas
- Lógica condicional para actualización del juego
- Manejo de transiciones entre estados

### 2. Interfaz Visual
- Menú principal con título y opciones
- Pantalla de Game Over con opciones de reinicio
- Indicadores visuales para la opción seleccionada
- Fondo semi-transparente para mejor legibilidad

### 3. Reinicio de Partida
- Limpieza completa de sprites existentes
- Recreación de jugador y enemigos
- Reset de variables de control de disparo
- Restauración del estado inicial del juego

### 4. Integración con el Motor de Juego
- Modificación del `GameEngine` para soportar estados
- Actualización del `CameraHandler` para mostrar menús
- Control de entrada unificado
- Lógica de juego condicional

## Archivos Modificados

1. **`game_logic/menu.py`** (NUEVO): Sistema completo de menú
2. **`game_logic/game_engine.py`**: Integración del menú
3. **`game_logic/camera.py`**: Renderizado de menús y control de entrada

## Cómo Usar

1. Ejecuta el juego normalmente con `python main.py`
2. El juego iniciará en el menú principal
3. Usa W/S para navegar y ESPACIO para seleccionar
4. Cuando termines una partida, aparecerá la pantalla de Game Over
5. Puedes reiniciar la partida o volver al menú principal

## Detalles Técnicos

- El menú se renderiza usando OpenCV sobre el feed de la cámara
- La lógica del juego solo se ejecuta cuando el estado es "PLAYING"
- El reinicio de partida preserva la configuración inicial del juego
- Los controles son consistentes en todos los estados del menú
