# game_logic/bullet.py

import pygame
# Importación correcta: Trae las constantes de color y velocidad
from .settings import YELLOW, BULLET_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT, RED

# =================================================================
# 1. Clase Bullet (DISPARO DEL JUGADOR)
# =================================================================
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.Surface([4, 15]) 
        self.image.fill(YELLOW)             # Color Amarillo
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        
        self.speed = BULLET_SPEED

    def update(self):
        """Mueve el disparo del jugador hacia arriba y lo elimina si sale de la pantalla."""
        self.rect.y -= self.speed
        
        if self.rect.bottom < 0:
            self.kill()


# =================================================================
# 2. Clase EnemyBullet (DISPARO DEL ENEMIGO) - ¡SOLUCIONA EL IMPORTERROR!
# =================================================================
class EnemyBullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        
        # 1. Componente de Visualización
        self.image = pygame.Surface([4, 10]) # Ligeramente más pequeña
        self.image.fill(RED)                # Color Rojo (importado de settings)
        
        # 2. Componente de Colisión y Posición
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y # Posición inicial: sale del 'bottom' del enemigo (pasado como 'y')
        
        # 3. Movimiento
        self.speed = BULLET_SPEED # Podrías usar BULLET_SPEED_ENEMY si la creaste en settings
    
    def update(self):
        """Mueve el disparo del enemigo hacia abajo y lo elimina si sale de la pantalla."""
        # Movimiento CLAVE:
        # El operador '+=' (suma) es correcto. Aumentar la coordenada 'y' mueve el objeto HACIA ABAJO.
        self.rect.y += self.speed
        
        # Lógica de limpieza:
        # Si el borde superior de la bala (rect.top) se sale del borde inferior de la pantalla (SCREEN_HEIGHT), se elimina.
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()