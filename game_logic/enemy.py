# game_logic/enemy.py

import pygame
import random
import time # Necesario para el cooldown de disparo

# Importar todas las constantes V2.0 necesarias
from .settings import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, RED, ENEMY_MAX_HEALTH, BULLET_DAMAGE_ENEMY 
# Importar la clase de bala específica del enemigo
from .bullet import EnemyBullet 

class Enemy(pygame.sprite.Sprite):
    
    # CORRECCIÓN CRÍTICA: Aceptar x, y para la posición
    def __init__(self, x, y):
        super().__init__()
        
        # 1. Componente de Visualización (Cambiado de 40x40 a 30x30 para mayor distinción)
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)                  
        
        # 2. Componente de Colisión y Posición (self.rect)
        self.rect = self.image.get_rect()
        
        # CRÍTICO: Usar las coordenadas pasadas para la posición
        self.rect.x = x
        self.rect.y = y                      
        
        # 3. Movimiento
        self.speed = ENEMY_SPEED
        
        # 4. LÓGICA DE SALUD (DEV-04, DEV-05)
        self.max_health = ENEMY_MAX_HEALTH
        self.health = ENEMY_MAX_HEALTH
        
        # 5. LÓGICA DE DISPARO (DEV-03)
        self.last_shot = pygame.time.get_ticks() 
        self.shoot_delay = 3500 # Dispara cada 1.5 segundos
        self.bullet_speed = 5
        
    def update(self):
        """
        Lógica que se ejecuta en cada fotograma para mover el enemigo y reiniciarlo.
        """
        # Mueve el enemigo hacia abajo
        self.rect.y += self.speed
        
        # Si sale de la pantalla, reinicia la posición
        if self.rect.top > SCREEN_HEIGHT:
             # Lo reiniciamos completamente para simular que un nuevo enemigo entró
             self.kill() 
             # Nota: GameEngine es responsable de crear un reemplazo.

    # --- NUEVOS MÉTODOS V2.0 ---
    
    def take_damage(self, damage):
        """
        Reduce la salud del enemigo. Retorna True si el enemigo murió, False si sobrevive.
        """
        self.health -= damage
        if self.health <= 0:
            self.kill() # Elimina el sprite de todos los grupos
            return True
        return False
        
    def fire(self, all_sprites_group, enemy_bullets_group):
        """
        Dispara una bala si el cooldown lo permite (DEV-03).
        """
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Crea una bala específica del enemigo
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom, self.bullet_speed)
            
            # Añade la bala a ambos grupos
            all_sprites_group.add(bullet)
            enemy_bullets_group.add(bullet)