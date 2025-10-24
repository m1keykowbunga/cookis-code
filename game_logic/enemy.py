# game_logic/enemy.py

import pygame
import random
import time 

# Importar todas las constantes necesarias y la clase EnemyBullet
from .settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED, RED, 
    ENEMY_MAX_HEALTH, BULLET_DAMAGE_ENEMY, ENEMY_SHOOT_DELAY
)
from .bullet import EnemyBullet 


class Enemy(pygame.sprite.Sprite):
    
    # CRÍTICO: El constructor debe aceptar x, y para que GameEngine controle la posición inicial.
    def __init__(self, x, y):
        super().__init__()
        
        # 1. Componente de Visualización
        self.image = pygame.Surface([40, 40])
        self.image.fill(RED)                  
        
        # 2. Componente de Colisión y Posición
        self.rect = self.image.get_rect()
        
        # CRÍTICO: Usar las coordenadas pasadas para la posición
        self.rect.x = x
        self.rect.y = y                      
        
        # 3. Movimiento
        self.speed = ENEMY_SPEED
        
        # 4. LÓGICA DE SALUD (Añadida desde HEAD)
        self.max_health = ENEMY_MAX_HEALTH
        self.health = ENEMY_MAX_HEALTH
        
        # 5. LÓGICA DE DISPARO (Añadida desde HEAD)
        self.last_shot = pygame.time.get_ticks() 
        self.shoot_delay = ENEMY_SHOOT_DELAY # Usar constante si existe, sino 3500ms
        self.bullet_speed = ENEMY_SPEED + 1 # Una velocidad ligeramente superior a la del enemigo

    def update(self):
        """
        Mueve el enemigo hacia abajo y lo elimina si sale de la pantalla.
        """
        # Mueve el enemigo hacia abajo
        self.rect.y += self.speed
        
        # Si sale de la pantalla, se elimina. GameEngine se encarga de reemplazarlo.
        if self.rect.top > SCREEN_HEIGHT:
             self.kill() 

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
        Dispara una bala si el cooldown lo permite (Añadido desde HEAD).
        """
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Crea una bala específica del enemigo
            bullet = EnemyBullet(self.rect.centerx, self.rect.bottom) 
            
            # Añade la bala a ambos grupos
            all_sprites_group.add(bullet)
            enemy_bullets_group.add(bullet)

    # Nota: Es crucial que la clase EnemyBullet no reciba 'self.bullet_speed' en su __init__
    # a menos que su definición en 'bullet.py' se haya modificado para aceptarla.
    # Se asume que usa la velocidad por defecto.