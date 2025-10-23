# game_logic/settings.py

# =================================================================
# 1. DIMENSIONES DE LA VENTANA Y FPS (Pygame)
# =================================================================
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60 # Frames por segundo del motor de juego

# =================================================================
# 2. COLORES (Pygame)
# =================================================================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# =================================================================
# 3. CONFIGURACIÓN DEL JUGADOR (Player)
# =================================================================
PLAYER_SPEED = 5        # Píxeles que se mueve la nave por ciclo de juego
PLAYER_MAX_HEALTH = 100 # Salud máxima inicial del jugador

# Daños de colisión (Valores 'hardcodeados' que deben centralizarse)
PLAYER_ENEMY_COLLISION_DAMAGE = 25 # Daño que un enemigo quieto hace al jugador
PLAYER_ENEMY_BULLET_DAMAGE = 10    # Daño que un disparo enemigo hace al jugador

# =================================================================
# 4. CONFIGURACIÓN DE ENEMIGOS (Enemy)
# =================================================================
ENEMY_SPEED = 2           # Píxeles que se mueve el enemigo por ciclo de juego
ENEMY_MAX_HEALTH = 30     # **CORREGIDO** - Salud que tendrá el enemigo (Causó el ImportError)
ENEMY_SPAWN_COUNT = 5     # Cuántos enemigos se generan al inicio
ENEMY_SHOOT_DELAY = 1500  # [MS] Frecuencia de disparo del enemigo (si aplica)

# =================================================================
# 5. CONFIGURACIÓN DE DISPAROS (Bullet)
# =================================================================
BULLET_SPEED = 10       # Píxeles que se mueve el disparo por ciclo de juego
BULLET_PLAYER_COOLDOWN = 500 # [MS] Delay entre disparos del jugador (Tú lo tenías en GameEngine)
BULLET_DAMAGE_ENEMY = 30 # Daño que hace el disparo del jugador al enemigo

# =================================================================
# 6. CONFIGURACIÓN DE VISIÓN POR COMPUTADORA (CV)
# =================================================================

# Dimensiones de la cámara / video que esperamos
CAM_WIDTH = 640
CAM_HEIGHT = 480

# RANGO DE COLOR PARA DETECCIÓN (HSV)
# El problema del color rojo es que requiere DOS RANGOS (Bajo y Alto)

# --- RANGO ROJO ORIGINAL (Doble Rango) ---
# Bajo: (0-10) y Alto: (170-180)
RED_LOWER_H1 = (0, 100, 100)
RED_UPPER_H1 = (10, 255, 255)
RED_LOWER_H2 = (170, 100, 100) # El segundo rango de rojo
RED_UPPER_H2 = (180, 255, 255)

# --- RANGO VERDE (Recomendado para REF-02) ---
# Ya que el rojo es complejo, recomendamos usar VERDE para la Tarea REF-02
RED_LOWER = (0, 50, 50)  # Ejemplo de rango Verde
RED_UPPER = (10, 255, 255)

# --- CONFIGURACIÓN DE SUAVIZADO (REF-02) ---
SMOOTHING_ALPHA = 0.1 # Factor Alpha para el suavizado exponencial (0.0 = sin suavizado, 1.0 = sin suavizado)