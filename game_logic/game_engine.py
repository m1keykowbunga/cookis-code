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
from .menu import GameMenu # CRÍTICO: Integrar el nuevo sistema de menú


class GameEngine:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            
            # 1. Configuración de Entorno NO_DISPLAY
            # CRÍTICO: COMENTAR esta línea. La versión HEAD es correcta. 
            # Si NO se comenta, OpenCV no puede abrir la ventana de la cámara.
            # os.environ["SDL_VIDEODRIVER"] = "dummy" 
            
            # 2. Inicialización de Pygame y Configuración base
            pygame.init()
            self.screen = None  # No necesitamos la surface de Pygame, ya que OpenCV dibuja.
            self.clock = pygame.time.Clock()
            self.running = True
            self.initialized = True
            self.score = 0 # Inicializar la puntuación
            
            # ----------------------------------------------------------------
            # 5. CREACIÓN DE SPRITES Y GRUPOS
            # ----------------------------------------------------------------
            self.all_sprites = pygame.sprite.Group()
            self.enemies = pygame.sprite.Group()
            self.bullets = pygame.sprite.Group()
            
            # Control de Disparo
            self.last_shot = pygame.time.get_ticks()
            # CRÍTICO: Usar la constante del archivo settings.py (HEAD es correcto)
            self.shoot_delay = BULLET_PLAYER_COOLDOWN 
            
            # Crea la nave del jugador
            self.player = Player()
            self.all_sprites.add(self.player)
            
            # Creación inicial de enemigos (Usamos la lógica más robusta de HEAD)
            for _ in range(ENEMY_SPAWN_COUNT): # Usamos la constante ENEMY_SPAWN_COUNT de settings.py
                self._spawn_enemy()
            
            # 6. CREACIÓN DEL MANEJADOR DE CÁMARA
            self.camera_handler = CameraHandler(self)
            
            # 7. CREACIÓN DEL SISTEMA DE MENÚ (CRÍTICO: Añadido desde develop2)
            self.menu = GameMenu(self)
            
    def _spawn_enemy(self):
        """Método auxiliar para crear y añadir un enemigo con posición aleatoria."""
        enemy_x = random.randrange(0, SCREEN_WIDTH)
        enemy_y = random.randrange(50, SCREEN_HEIGHT // 4)
        enemy = Enemy(enemy_x, enemy_y)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    # --- MÉTODOS DEL BUCLE PRINCIPAL ---

    def _handle_input(self):
        """Gestiona eventos (cerrar ventana) y la lógica de Disparo Automático."""
        
        # Procesamiento de eventos de cierre de ventana
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Lógica de Disparo Automático (solo si estamos jugando, de develop2)
        if self.menu.is_playing():
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.player.shoot(self.all_sprites, self.bullets)


    def _update_game_state(self):
        """Actualiza el estado de todos los sprites y revisa las colisiones."""
        
        # Solo actualizar el juego si estamos jugando (de develop2)
        if not self.menu.is_playing():
            return
            
        self.all_sprites.update()

        # Colisión 1: Nave vs. Enemigos
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            print("¡COLISIÓN DETECTADA! Juego Terminado.")
            # CRÍTICO: Usamos el método game_over del menú (de develop2)
            self.menu.game_over() 
            # No es necesario poner self.running = False aquí, el menú lo gestiona.

        # Colisión 2: Disparos vs. Enemigos
        # Elimina la bala (True) y el enemigo (True)
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if hits:
            print("Enemigo destruido!")
            # Si destruimos un enemigo, sumamos puntos (nueva lógica)
            self.score += 10 
            
            # Reaparecer un enemigo usando el método auxiliar
            self._spawn_enemy()

    def _draw_elements(self):
        """
        Función de dibujo de Pygame (vacía, ya que el dibujo lo hace OpenCV).
        """
        pass
    
    def run(self):
        """
        Método principal: delega el control del bucle a la cámara (CRÍTICO, de develop2).
        """
        print("Iniciando motor de juego (Lógica Pygame OK). Abriendo cámara...")
        
        if not self.initialized:
            self.__init__()
        
        # El bucle principal del juego reside AHORA en CameraHandler.run()
        self.camera_handler.run()
        
        # Limpieza al finalizar (se ejecuta después de que camera_handler.run() termina)
        pygame.quit()
        sys.exit()
    
    def get_sprites_data(self):
        """Retorna la posición de todos los sprites activos para el overlay de la cámara."""
        data = []
        for sprite in self.all_sprites:
            
            # Usamos las clases para determinar el color de cada sprite
            if isinstance(sprite, Player):
                color = BLUE  # Nave del jugador
            elif isinstance(sprite, Enemy):
                color = RED    # Enemigo
            elif isinstance(sprite, Bullet): 
                color = YELLOW # Disparo
            else:
                color = BLACK 

            data.append({
                'rect': sprite.rect, 
                'color': color
            })
        return data