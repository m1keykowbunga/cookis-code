# game_logic/game_engine.py

import pygame
import sys
import os 
import random 

# Importaciones del Proyecto
# --------------------------------------------------------------------------
from .settings import * # Importamos las constantes (incluyendo FPS, BULLET_PLAYER_COOLDOWN, ENEMY_SPAWN_COUNT, etc.)
from .player import Player        
from .camera import CameraHandler 
from .enemy import Enemy          
from .bullet import Bullet        
# --------------------------------------------------------------------------

class GameEngine:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'initialized'):
            
            # 1. Configuración de Entorno NO_DISPLAY (COMENTADA para permitir la ventana de OpenCV)
            # os.environ["SDL_VIDEODRIVER"] = "dummy" 
            
            # 2. Inicialización de Pygame y Configuración base
            pygame.init()
            self.screen = None 
            self.clock = pygame.time.Clock()
            self.running = True
            self.initialized = True
            
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
            
            # Creación de enemigos
            for i in range(ENEMY_SPAWN_COUNT): 
                
                enemy_x = random.randrange(0, SCREEN_WIDTH) 
                enemy_y = random.randrange(50, SCREEN_HEIGHT // 4) 
                
                enemy = Enemy(enemy_x, enemy_y) 
                
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            
            # 6. CREACIÓN DEL MANEJADOR DE CÁMARA
            self.camera_handler = CameraHandler(self)
            
            
    # --- MÉTODOS DEL BUCLE PRINCIPAL ---

    def _handle_input(self):
        """Gestiona eventos (cerrar ventana) y la lógica de Disparo Automático."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Lógica de Disparo Automático
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            self.player.shoot(self.all_sprites, self.bullets)


    def _update_game_state(self):
        """Actualiza el estado de todos los sprites y revisa las colisiones."""
        self.all_sprites.update()

        # Colisión 1: Nave vs. Enemigos
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            print("¡COLISIÓN DETECTADA! Juego Terminado.")
            self.running = False

        # Colisión 2: Disparos vs. Enemigos
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if hits:
            print("Enemigo destruido!")
            
            enemy_x = random.randrange(0, SCREEN_WIDTH) 
            enemy_y = random.randrange(50, SCREEN_HEIGHT // 4) 
            
            enemy = Enemy(enemy_x, enemy_y)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def _draw_elements(self):
        """Función de dibujo de Pygame (vacía)."""
        pass
    
    # === MÉTODO RUN CON INVERSIÓN DE CONTROL (REF-01) ===
    def run(self):
        print("Iniciando motor de juego (Lógica Pygame OK). Tomando el control del bucle...")
        
        if not self.initialized:
            self.__init__()
        
        # El bucle principal del juego reside AHORA aquí (REF-01)
        while self.running:
            
            # 1. ENTRADA DEL JUGADOR (Teclado y Cámara)
            self._handle_input()
            
            # Pedir posición a la cámara
            detected_x = self.camera_handler.get_position() 
            self.player.set_position_from_camera(detected_x)
            
            # 2. ACTUALIZACIÓN DEL ESTADO DEL JUEGO
            self._update_game_state()
            
            # 3. DIBUJO (El motor pide a la cámara que dibuje el overlay)
            sprites_data = self.get_sprites_data()
            self.camera_handler.draw_overlay(sprites_data)
            
            # 4. CONTROL DE TIEMPO
            self.clock.tick(FPS) 
            
        # Limpieza al salir del bucle
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