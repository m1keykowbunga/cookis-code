# game_logic/game_engine.py

import pygame
import sys
import os
import random

# Importaciones del Proyecto
# --------------------------------------------------------------------------
from .settings import *
from .player import Player
from .camera import CameraHandler
from .enemy import Enemy
from .bullet import Bullet
from .menu import GameMenu 


class GameEngine:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            
            # 1. Configuración de Entorno
            pygame.init()
            self.screen = None 
            self.clock = pygame.time.Clock()
            self.running = True
            self.initialized = True
            self.score = 0
            
            # ----------------------------------------------------------------
            # 5. CREACIÓN DE SPRITES Y GRUPOS
            # ----------------------------------------------------------------
            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            
            # Control de Disparo
            self.last_shot = pygame.time.get_ticks()
            self.shoot_delay = BULLET_PLAYER_COOLDOWN 
            
            # Crea la nave del jugador
            self.player = Player()
            self.all_sprites.add(self.player)
            
            # 6. CREACIÓN DEL MANEJADOR DE CÁMARA
            self.camera_handler = CameraHandler(self)
            
            # 7. CREACIÓN DEL SISTEMA DE MENÚ
            self.menu = GameMenu(self)
            
    def _spawn_enemy(self):
        """Método auxiliar para crear y añadir un enemigo con posición aleatoria."""
        enemy_x = random.randrange(0, SCREEN_WIDTH)
        enemy_y = random.randrange(50, SCREEN_HEIGHT // 4)
        enemy = Enemy(enemy_x, enemy_y)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    # --- MÉTODOS DEL BUCLE PRINCIPAL ---

    # ESTE ES EL MÉTODO CORREGIDO: Sólo gestiona el disparo automático
    def _handle_input(self):
        """Gestiona la lógica de Disparo Automático (Disparo sólo si estamos jugando)."""
        
        # Lógica de Disparo Automático (permanece aquí)
        if self.menu.is_playing():
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.player.shoot(self.all_sprites, self.bullets)
                
    def _process_camera_data(self):
        """Llama a la cámara para obtener la posición y actualiza al jugador."""
        
        screen_x = self.camera_handler.get_position()
        
        if screen_x is not None:
            self.player.set_position_from_camera(screen_x)

    def _update_game_state(self):
        """Actualiza el estado de todos los sprites y revisa las colisiones."""
        
        if not self.menu.is_playing():
            return
            
        self.all_sprites.update()

        # Colisión 1: Nave vs. Enemigos
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.menu.game_over() 

        # Colisión 2: Disparos vs. Enemigos
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if hits:
            self.score += 10 
            self._spawn_enemy()

    def _draw_elements(self):
        """
        Función de dibujo de Pygame (vacía, ya que el dibujo lo hace OpenCV).
        """
        if self.screen is not None:
             pass
    
    def run(self):
        """
        Método principal: implementa el bucle de juego y controla el flujo.
        """
        print("Iniciando motor de juego (Lógica Pygame OK). Abriendo cámara...")
        
        if not self.initialized:
            self.__init__()
            
        while self.running:
            
            # 1. CRÍTICO: Manejo de tiempo (FPS)
            self.clock.tick(FPS) 
            
            # 2. Manejo de Eventos (DE PYGAME) - CRUCIAL PARA EL MENÚ
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                
            # 3. Lógica de la Cámara (Control Invertido)
            self._process_camera_data() 
            
            # 4. Lógica de Disparo y Colisiones (Si estamos jugando)
            self._handle_input()      # Disparo automático
            self._update_game_state()
            
            # 5. Salida
            if not self.running:
                break
                
        # Limpieza final
        self.camera_handler.release_resources()
        pygame.quit()
        sys.exit()
        
    def get_sprites_data(self):
        """Retorna la posición de todos los sprites activos para el overlay de la cámara."""
        data = []
        for sprite in self.all_sprites:
            
            if isinstance(sprite, Player):
                color = BLUE
            elif isinstance(sprite, Enemy):
                color = RED
            elif isinstance(sprite, Bullet): 
                color = YELLOW
            else:
                color = BLACK 

            data.append({
                'rect': sprite.rect, 
                'color': color
            })
        return data