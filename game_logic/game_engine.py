# game_logic/game_engine.py

import pygame
import sys
import os
import random

# Importaciones del Proyecto
from .settings import *
from .player import Player
from .camera import CameraHandler
from .enemy import Enemy
from .bullet import Bullet
from .menu import GameMenu


class GameEngine:
    # Implementación del patrón Singleton
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            # 1. Configuración de Entorno
            pygame.init()
            # Inicializamos la pantalla. Aunque no se dibuje, es necesario para que Pygame capture eventos.
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SHOWN)
            self.clock = pygame.time.Clock()
            self.running = True
            self.initialized = True
            self.score = 0

            # 5. CREACIÓN DE SPRITES Y GRUPOS
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
            
            #estado pausa del juego
            self.is_paused = False

    def _spawn_enemy(self):
        """Método auxiliar para crear y añadir un enemigo con posición aleatoria."""
        enemy_x = random.randrange(0, SCREEN_WIDTH)
        enemy_y = random.randrange(40, SCREEN_HEIGHT // 4)
        enemy = Enemy(enemy_x, enemy_y)
        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def set_screen_size(self, new_width, new_height):
        """Ajusta la resolución de pantalla y reinicializa los componentes dependientes."""
        global SCREEN_WIDTH, SCREEN_HEIGHT
        screen_mode = pygame.SHOWN

        # 1. Lógica para Pantalla Completa (Full-screen)
        if new_width is None or new_height is None:
            info = pygame.display.Info()
            new_width = info.current_w
            new_height = info.current_h
            screen_mode = pygame.FULLSCREEN

        # 2. Actualizar las constantes GLOBALES
        SCREEN_WIDTH = new_width
        SCREEN_HEIGHT = new_height

        # 3. Reconfigurar el sistema de video de Pygame.
        self.screen = pygame.display.set_mode((new_width, new_height), screen_mode)

        # 4. DELEGACIÓN: Pide a la cámara que se ajuste
        self.camera_handler.reconfigure_camera(new_width, new_height)

        # 5. Reinicialización de estado: Vuelve al menú y ajusta el jugador
        self.menu.reset_game_state()
        self.menu.return_to_menu()
        
        self.player.rect.centerx = SCREEN_WIDTH // 2 
        # Asegúrate de que el bottom esté exactamente en el límite.
        self.player.rect.bottom = SCREEN_HEIGHT
     
        print(f"Pantalla cambiada a: {new_width}x{new_height}")

    # --- MÉTODOS DEL BUCLE PRINCIPAL ---

    def _handle_input(self):
        """Gestiona la lógica de Disparo Automático."""
        if self.menu.is_playing() and not self.is_paused:
            now = pygame.time.get_ticks()
            if now - self.last_shot > self.shoot_delay:
                self.last_shot = now
                self.player.shoot(self.all_sprites, self.bullets)
        
                    
    def _process_camera_data(self, player_x):
        """Llama a la cámara para obtener la posición y actualiza al jugador."""
        if self.menu.is_playing() and self.player: 
            if player_x is not None:
                self.player.set_position_from_camera(player_x)

    def _update_game_state(self):
        """Actualiza el estado de todos los sprites y revisa las colisiones (SCORE & HEALTH integrados)."""
        if not self.menu.is_playing():
            return
        
        if self.is_paused:
            self.player.rect.bottom = SCREEN_HEIGHT
            return
        
        # Actualiza todos los sprites
        self.all_sprites.update()
        
        # Asegura la posición del jugador al fondo (ajuste visual)
        self.player.rect.bottom = SCREEN_HEIGHT
        
        
        # -----------------------------------------------------------------
        # 🛡️ 1. Colisiones de Enemigos con el Jugador (LÓGICA DE VIDA)
        # -----------------------------------------------------------------
        # True: El enemigo que choca se destruye
        player_hits = pygame.sprite.spritecollide(self.player, self.enemies, True) 
        if player_hits:
            if self.player.take_damage(): # reduce la vida y chequea si es <= 0
                self.menu.game_over()
            
        # -----------------------------------------------------------------
        # 💰 2. Colisiones de Balas con Enemigos (LÓGICA DE PUNTUACIÓN)
        # -----------------------------------------------------------------
        # True: Las balas y los enemigos golpeados se destruyen
        enemy_hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if enemy_hits:
            enemies_destroyed = sum(len(enemies) for enemies in enemy_hits.values())
            self.score += (enemies_destroyed * 10) 
            
            # Reponer los enemigos
            for _ in range(enemies_destroyed):
                self._spawn_enemy()
                
    def run(self):
        """Método principal: implementa el bucle de juego y controla el flujo."""
        print("Iniciando motor de juego (Lógica Pygame OK). Abriendo cámara...")

        if not self.initialized:
            self.__init__()

        while self.running:
            # 1. Captura de eventos Pygame (QUIT) y manejo de tiempo
            # Mantenemos pump() aquí para asegurar que Pygame esté activo.
            pygame.event.pump()
            self.clock.tick(FPS)
            

            # Procesar eventos Pygame normales (solo necesitamos QUIT)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
                    
                #tecla Pausa
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        if self.menu.is_playing():
                            self.is_paused = not self.is_paused

                # Intentamos pasar los eventos a Pygame Menu por si acaso funciona en el sistema del usuario
                # (Aunque la entrada de CV2 es la que usamos para la navegación forzada)
               # menu_action = self.menu.handle_input(event)
               # if menu_action == "QUIT":
                #    self.running = False

            # 2. Lógica del Juego (Solo si estamos jugando)
            player_x = self.camera_handler.get_position()
            self._process_camera_data(player_x) 
            
            # Movemos la nave solo si estamos jugando.
            if self.menu.is_playing() and self.player: 
                 self.player.set_position_from_camera(player_x)
                 
            self._handle_input()
            self._update_game_state()

            # 3. DIBUJO Y OBTENCIÓN DE LA TECLA CV2 (CRÍTICO)
            sprites_data = self.get_sprites_data()
            
    
            # Una sola llamada: dibuja la ventana y obtiene la tecla pulsada.
            key_cv2 = self.camera_handler.draw_window(sprites_data)

            # 4. Procesamiento de la Tecla CV2 (Navegación Forzada)
            # Usamos el valor de la tecla CV2 para simular la entrada del menú.
            if not self.menu.is_playing() or self.is_paused:
                # Mapeo de ASCII (CV2) a Eventos de Pygame para el menú
                # 119='w' (Arriba), 115='s' (Abajo), 13=ENTER (Seleccionar), 27=ESCAPE (Volver)
                if key_cv2 == ord('w'):
                    self.menu.handle_input_cv2_shim(pygame.K_w)
                elif key_cv2 == ord('s'):
                    self.menu.handle_input_cv2_shim(pygame.K_s)
                elif key_cv2 == 13:
                    self.menu.handle_input_cv2_shim(pygame.K_RETURN)
                elif key_cv2 == 27:
                    if not self.is_paused:
                        self.menu.handle_input_cv2_shim(pygame.K_ESCAPE)
                    
            if self.menu.is_playing() and key_cv2 == ord('p'):
                 self.is_paused = not self.is_paused
                 print(f"DEBUG: Pausa activada por CV2: {self.is_paused}")

        # Limpieza final (FUERA DEL BUCLE)
        self.camera_handler.release_resources()
        pygame.quit()
        sys.exit()

    def get_sprites_data(self):
        """Retorna la posición de todos los sprites activos para el overlay de la cámara."""
        data = []
        for sprite in self.all_sprites:
            
            if self.is_paused and not isinstance(sprite, Player):
                continue
            # ... (Lógica de color y recolección de datos sin cambios)
            if isinstance(sprite, Player):
                color = (0, 0, 255)  # BLUE
            elif isinstance(sprite, Enemy):
                color = (255, 0, 0)  # RED
            elif isinstance(sprite, Bullet):
                color = (255, 255, 0)  # YELLOW
            else:
                color = (0, 0, 0)  # BLACK

            data.append({
                'rect': sprite.rect,
                'color': color
            })
        return data