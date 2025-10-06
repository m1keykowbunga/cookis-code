# game_logic/enemy.py

import pygame
import random
# Asegúrate de que SCREEN_HEIGHT esté importada aquí
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, RED 

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        # Es necesario llamar al constructor de la clase padre (Sprite)
        super().__init__()
        
        # 1. Componente de Visualización 
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)                  
        
        # 2. Componente de Colisión y Posición (self.rect)
        self.rect = self.image.get_rect() 
        
        # 3. Posición Inicial (aleatoria en la parte superior)
        # Ajustamos el margen para que sean visibles inmediatamente en el overlay
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width) 
        self.rect.y = random.randrange(-120, -40)                      
        
        # 4. Movimiento
        self.speed = ENEMY_SPEED

    def update(self):
        """
        Lógica que se ejecuta en cada fotograma para mover el enemigo y reiniciarlo.
        """
        # Mueve el enemigo hacia abajo
        self.rect.y += self.speed
        
        # CRÍTICO: Usamos la constante SCREEN_HEIGHT para evitar el AttributeError
        # Si el borde superior del enemigo pasa el borde inferior de la pantalla:
        if self.rect.top > SCREEN_HEIGHT:
             # Reinicia el enemigo en una nueva posición X aleatoria
             self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
             # Reinicia el enemigo en la zona invisible superior
             self.rect.y = random.randrange(-120, -40)