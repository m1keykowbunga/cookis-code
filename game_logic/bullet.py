# game_logic/bullet.py

import pygame
# Importación correcta: Trae las constantes de color y velocidad
from .settings import YELLOW, BULLET_SPEED 

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        # Llama al constructor de Pygame Sprite, esencial para la funcionalidad de juego
        super().__init__()
        
        # 1. Componente de Visualización
        self.image = pygame.Surface([4, 15]) # Tamaño adecuado para una bala
        self.image.fill(YELLOW)             # Color blanco (como definimos en settings.py)
        
        # 2. Componente de Colisión y Posición
        self.rect = self.image.get_rect()
        
        # Posición inicial: Se centra en 'x' y sale desde el 'top' de la nave (pasado como 'y')
        self.rect.centerx = x
        self.rect.bottom = y
        
        # 3. Movimiento
        self.speed = BULLET_SPEED # Usa la constante importada
        # La creación de la bala es perfecta.

    def update(self):
        """
        Mueve el disparo hacia arriba y lo elimina si sale de la pantalla.
        """
        # Movimiento CLAVE:
        # El operador '-=' (resta) es correcto. Disminuir la coordenada 'y' en Pygame mueve el objeto HACIA ARRIBA.
        self.rect.y -= self.speed
        
        # Lógica de limpieza:
        # Si el borde inferior de la bala (rect.bottom) se sale del borde superior de la pantalla (0), se elimina.
        if self.rect.bottom < 0:
            self.kill() # Correcto: remueve la bala de todos los grupos Sprite