# game_logic/game_engine.py
import pygame
import sys
import os # Necesario para manipular variables de entorno del sistema

# Importaciones del Proyecto
# --------------------------------------------------------------------------
from .settings import * # Importamos las constantes
from .player import Player        # Para crear la nave del jugador
from .camera import CameraHandler # Para manejar la cámara y el control por visión
from .enemy import Enemy          # Para crear enemigos
from .bullet import Bullet        # Importamos Bullet para crear y para la lógica de color
# --------------------------------------------------------------------------

class GameEngine:
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self,'initialized'):
            
            # 1. Configuración de Entorno NO_DISPLAY
            os.environ["SDL_VIDEODRIVER"] = "dummy"
            
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
            self.shoot_delay = 500                  
            
            # Crea la nave y enemigos
            self.player = Player()           
            self.all_sprites.add(self.player)        
            
            for i in range(5):
                enemy = Enemy()
                self.all_sprites.add(enemy)
                self.enemies.add(enemy)
            
            # 6. CREACIÓN DEL MANEJADOR DE CÁMARA
            self.camera_handler = CameraHandler(self)
            
            
    # --- MÉTODOS DEL BUCLE PRINCIPAL ---

    def _handle_input(self):
        """
        Gestiona eventos (cerrar ventana) y la lógica de Disparo Automático.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # Lógica de Disparo Automático (usa el cooldown de 500ms)
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            # La nave llama al método shoot, pasando los grupos
            self.player.shoot(self.all_sprites, self.bullets)


    def _update_game_state(self):
        """
        Actualiza el estado de todos los sprites y revisa las colisiones.
        """
        self.all_sprites.update()

        # Colisión 1: Nave vs. Enemigos
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            print("¡COLISIÓN DETECTADA! Juego Terminado.")
            self.running = False

        # Colisión 2: Disparos vs. Enemigos
        # Elimina la bala (True) y el enemigo (True)
        hits = pygame.sprite.groupcollide(self.bullets, self.enemies, True, True)
        
        if hits:
            print("Enemigo destruido!")
            enemy = Enemy()
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    def _draw_elements(self):
        """
        Función de dibujo de Pygame (vacía, ya que el dibujo lo hace OpenCV).
        """
        pass
    
    def run(self):
        # El método run estaba en el lugar correcto, no se toca.
        print("Iniciando motor de juego (Lógica Pygame OK). Abriendo cámara...")
        
        if not self.initialized:
            self.__init__()
        
        self.camera_handler.run()
        
        pygame.quit()
        sys.exit()
    
    def get_sprites_data(self):
        """
        Retorna la posición de todos los sprites activos para el overlay de la cámara.
        """
        data = []
        for sprite in self.all_sprites:
            
            # Usamos las clases para determinar el color de cada sprite
            if isinstance(sprite, Player):
                color = BLUE  # Nave del jugador
            elif isinstance(sprite, Enemy):
                color = RED   # Enemigo
            elif isinstance(sprite, Bullet): 
                color = YELLOW # Disparo
            else:
                color = BLACK 

            data.append({
                'rect': sprite.rect, 
                'color': color
            })
        return data