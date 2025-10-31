# game_logic/bullet.py

import pygame
# CRÍTICO: Importar todas las constantes necesarias: 
# - RED y YELLOW (Colores)
# - BULLET_SPEED (Velocidad de movimiento)
# - SCREEN_HEIGHT (Límite para eliminar balas que salen por abajo)
from .settings import YELLOW, BULLET_SPEED, SCREEN_HEIGHT, RED 

# =================================================================
# 1. Clase Bullet (DISPARO DEL JUGADOR)
# =================================================================
class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        # Llama al constructor de Pygame Sprite
        super().__init__()
        
        # 1. Componente de Visualización
        self.image = pygame.Surface([4, 15]) 
        self.image.fill(YELLOW)             # Color Amarillo
        
        # 2. Componente de Colisión y Posición
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y # Inicia desde abajo del jugador
        
        # 3. Movimiento
        self.speed = BULLET_SPEED

    def update(self):
        """Mueve el disparo del jugador hacia arriba y lo elimina si sale de la pantalla."""
        # Mover hacia arriba (resta en 'y')
        self.rect.y -= self.speed 
        
        # Eliminar si sale por el borde superior
        if self.rect.bottom < 0:
            self.kill()


# =================================================================
# 2. Clase EnemyBullet (DISPARO DEL ENEMIGO) - Añadida desde HEAD
# =================================================================
class EnemyBullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        super().__init__()
        
        # 1. Componente de Visualización
        self.image = pygame.Surface([4, 10]) # Ligeramente más pequeña que la del jugador
        self.image.fill(RED)                # Color Rojo
        
        # 2. Componente de Colisión y Posición
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y # Posición inicial: sale del 'bottom' del enemigo
        
        # 3. Movimiento
        self.speed = BULLET_SPEED # Usamos la misma velocidad por simplicidad
    
    def update(self):
        """Mueve el disparo del enemigo hacia abajo y lo elimina si sale de la pantalla."""
        # Mover hacia abajo (suma en 'y')
        self.rect.y += self.speed
        
        # Eliminar si sale por el borde inferior
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()