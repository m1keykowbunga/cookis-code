# game_logic/player.py

import pygame
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED, BLUE 
from .bullet import Bullet 

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = pygame.Surface([50, 50]) 
        self.image.fill(BLUE) 
        self.rect = self.image.get_rect() 
        self.rect.centerx = SCREEN_WIDTH // 2 
        self.rect.bottom = SCREEN_HEIGHT - 10 
        self.speed = PLAYER_SPEED 

    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def handle_movement_input(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed 
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed 

    def set_position_from_camera(self, x_position):
        """
        Actualiza la posición X del jugador basada en la entrada de la cámara.
        Se usa en GameEngine.run().
        """
        if x_position is not None:
            # Asegura que la posición esté dentro de los límites de la pantalla
            new_x = max(0, min(x_position, SCREEN_WIDTH))
            self.rect.centerx = new_x
        
    def shoot(self, all_sprites, bullets):
        """
        Crea una instancia de Bullet en la posición actual de la nave.
        """
        new_bullet = Bullet(self.rect.centerx, self.rect.top) 
        
        all_sprites.add(new_bullet)
        bullets.add(new_bullet)