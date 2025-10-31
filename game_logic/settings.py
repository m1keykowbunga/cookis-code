# game_logic/settings.py

import pygame

# -----------------------------------------------------------------
# 1. CONFIGURACIÓN INICIAL DE DIMENSIONES (SCREEN & CAMERA)
# -----------------------------------------------------------------

# 1.1. Inicialización para obtener datos del monitor
pygame.init()
info = pygame.display.Info()

# 1.2. Dimensiones Iniciales (Usadas para Pygame en el primer arranque)
# Usamos el tamaño nativo del monitor como base inicial.
# Nota: Cambié el fallback de 1800x1600 a 1920x1080 (más estándar).
# Usamos el tamaño nativo del monitor si está disponible, si no, 1920x1080 como FALLBACK.
MONITOR_NATIVE_WIDTH = info.current_w if info.current_w != -1 else 1920
MONITOR_NATIVE_HEIGHT = info.current_h if info.current_h != -1 else 1080

# Establece el tamaño de pantalla inicial al nativo.
SCREEN_WIDTH = MONITOR_NATIVE_WIDTH
SCREEN_HEIGHT = MONITOR_NATIVE_HEIGHT

# 1.3. Dimensiones Base para la Cámara (Definimos un HD 16:9 y un SD 4:3)
# Usamos estas como las únicas dos resoluciones de trabajo de la cámara.
CAM_RES_HD = (1280, 720) # 16:9 - Para pantallas Grandes y Medianas
CAM_RES_SD = (640, 480)  # 4:3 - Para pantallas Pequeñas o 4:3

CAM_BASE_WIDTH, CAM_BASE_HEIGHT = CAM_RES_SD # Base por defecto (segura)


SCREEN_SIZE_OPTIONS = [
    # 1. GRANDE: Usa la resolución nativa detectada.
    ("GRANDE", (MONITOR_NATIVE_WIDTH, MONITOR_NATIVE_HEIGHT)),
    
    # 2. PEQUEÑA: Usa una resolución fija de 800x600 (tamaño PEQUEÑO).
    ("PEQUEÑA", (800, 600)), 
    
]
CAM_OPTIONS = {
    # 1. Mapeo de la Opción GRANDE (Natividad)
    (MONITOR_NATIVE_WIDTH, MONITOR_NATIVE_HEIGHT): 
        # Si la proporción nativa es > 1.6 (panorámica), usa HD; si no, SD. (Umbral corregido).
        CAM_RES_HD if MONITOR_NATIVE_WIDTH / MONITOR_NATIVE_HEIGHT > 1.0 else CAM_RES_SD,
    
    # 2. Mapeo de la Opción PEQUEÑA (Fija 800x600)
    (800, 600): 
        # Pantalla 4:3 (1.33), se mapea a la cámara SD (4:3) para proporción y rendimiento.
        CAM_RES_SD if MONITOR_NATIVE_WIDTH / MONITOR_NATIVE_HEIGHT > 1.0 else CAM_RES_HD
}
    

# -----------------------------------------------------------------
# 2. CONFIGURACIÓN DEL JUEGO (Pygame)
# -----------------------------------------------------------------
FPS = 100 

# COLORES (Pygame)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# 3. CONFIGURACIÓN DE ENTIDADES
# ... (Resto de las constantes sin cambios) ...
# JUGADOR (Player)
PLAYER_SPEED = 7        
PLAYER_MAX_HEALTH = 100 

# ENEMIGOS (Enemy)
ENEMY_SPEED = 2           
ENEMY_MAX_HEALTH = 30     
ENEMY_SPAWN_COUNT = 5     
ENEMY_SHOOT_DELAY = 3500  

# DISPAROS (Bullet)
BULLET_SPEED = 10       
BULLET_PLAYER_COOLDOWN = 500 
BULLET_DAMAGE_ENEMY = 30 

# DAÑOS DE COLISIÓN
PLAYER_ENEMY_COLLISION_DAMAGE = 25 
PLAYER_ENEMY_BULLET_DAMAGE = 10    


# 4. CONFIGURACIÓN DE VISIÓN POR COMPUTADORA (CV)
# RANGO ROJO (Doble Rango necesario para el color rojo)
# RANGO 1
RED_LOWER_H1 = (0, 100, 100)
RED_UPPER_H1 = (10, 255, 255)
# RANGO 2
RED_LOWER_H2 = (170, 100, 100) 
RED_UPPER_H2 = (180, 255, 255)

# CONFIGURACIÓN DE SUAVIZADO 
SMOOTHING_ALPHA = 0.1