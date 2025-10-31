import pygame
# Importamos todas las constantes necesarias
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, BLUE 
from .bullet import Bullet 

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface([50, 50]) 
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect() 
        
        self.rect.bottom = int(SCREEN_HEIGHT * 1.0)  
        self.speed = PLAYER_SPEED 

    def update(self):
        """Actualiza la posición X del jugador basada en la entrada CV."""
        # LÍMITES HORIZONTALES (Redundantes si se usa set_position_from_camera, pero seguros)
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # LÍMITES VERTICALES (Asegura que la nave esté en el borde inferior)
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

    

    def set_position_from_camera(self, x_position):
        """
        Actualiza la posición X del jugador basada en la entrada de la cámara,
        asegurando que permanezca dentro de los límites de la pantalla Pygame.
        """
        if x_position is not None:
            # Asegura que la posición (el centro del sprite) esté dentro de [0, SCREEN_WIDTH]
            new_center_x = max(self.rect.width // 2, min(x_position, SCREEN_WIDTH - self.rect.width // 2))
            
            self.rect.centerx = new_center_x
        
    def shoot(self, all_sprites, bullets):
        """
        Crea una instancia de Bullet en la posición actual de la nave.
        """
        new_bullet = Bullet(self.rect.centerx, self.rect.top) 
        
        all_sprites.add(new_bullet)
        bullets.add(new_bullet)