# game_logic/menu.py

import cv2
import numpy as np
import random
# Importación de constantes
from .settings import CAM_WIDTH, CAM_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, BLUE, RED, YELLOW, ENEMY_SPAWN_COUNT

# Importación de clases de sprites (CRÍTICO: Necesario para reset_game_state)
from .player import Player
from .enemy import Enemy


class GameMenu:
    """
    Sistema de menú para el juego Space Invaders Origami.
    Maneja la interfaz de usuario y los estados del juego.
    """
    
    def __init__(self, game_engine):
        self.game = game_engine
        self.current_state = "MENU"  # MENU, PLAYING, GAME_OVER
        self.menu_options = ["JUGAR", "SALIR"]
        # CRÍTICO: Usar esta lista de opciones en draw_game_over
        self.game_over_options = ["REINICIAR", "MENU PRINCIPAL", "SALIR"] 
        self.selected_option = 0
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0
        self.thickness = 2
        
    def draw_menu(self, frame):
        """
        Dibuja el menú principal en el frame de la cámara.
        """
        # Fondo semi-transparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (CAM_WIDTH, CAM_HEIGHT), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título del juego
        title_text = "SPACE INVADERS ORIGAMI"
        title_size = cv2.getTextSize(title_text, self.font, 1.5, 3)[0]
        title_x = (CAM_WIDTH - title_size[0]) // 2
        title_y = 100
        cv2.putText(frame, title_text, (title_x, title_y), self.font, 1.5, WHITE, 3)
        
        # Instrucciones
        instructions = [
            "Mueve tu mano roja para controlar la nave",
            "Presiona 'ESPACIO' para seleccionar",
            "Presiona 'Q' para salir"
        ]
        
        for i, instruction in enumerate(instructions):
            text_size = cv2.getTextSize(instruction, self.font, 0.6, 2)[0]
            text_x = (CAM_WIDTH - text_size[0]) // 2
            text_y = 150 + i * 30
            cv2.putText(frame, instruction, (text_x, text_y), self.font, 0.6, WHITE, 2)
        
        # Opciones del menú
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            text_size = cv2.getTextSize(option, self.font, self.font_scale, self.thickness)[0]
            text_x = (CAM_WIDTH - text_size[0]) // 2
            text_y = 300 + i * 60
            
            # Dibujar fondo para la opción seleccionada
            if i == self.selected_option:
                padding = 10
                cv2.rectangle(frame, 
                            (text_x - padding, text_y - text_size[1] - padding),
                            (text_x + text_size[0] + padding, text_y + padding),
                            BLUE, 2)
            
            cv2.putText(frame, option, (text_x, text_y), self.font, self.font_scale, color, self.thickness)
        
        # Indicador de selección
        indicator_text = ">>>"
        cv2.putText(frame, indicator_text, (text_x - 100, 300 + self.selected_option * 60), 
                   self.font, self.font_scale, YELLOW, self.thickness)
    
    def draw_game_over(self, frame):
        """
        Dibuja la pantalla de Game Over.
        """
        # Fondo semi-transparente
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (CAM_WIDTH, CAM_HEIGHT), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Texto Game Over
        game_over_text = "GAME OVER"
        text_size = cv2.getTextSize(game_over_text, self.font, 2.0, 4)[0]
        text_x = (CAM_WIDTH - text_size[0]) // 2
        text_y = CAM_HEIGHT // 2 - 50
        cv2.putText(frame, game_over_text, (text_x, text_y), self.font, 2.0, RED, 4)
        
        # Muestra la puntuación final
        score_text = f"PUNTUACION: {self.game.score}" # Asumiendo que GameEngine tiene un atributo 'score'
        score_size = cv2.getTextSize(score_text, self.font, 1.0, 2)[0]
        score_x = (CAM_WIDTH - score_size[0]) // 2
        score_y = CAM_HEIGHT // 2
        cv2.putText(frame, score_text, (score_x, score_y), self.font, 1.0, WHITE, 2)

        # Opciones
        for i, option in enumerate(self.game_over_options): # Usar la lista de opciones
            color = YELLOW if i == self.selected_option else WHITE
            text_size = cv2.getTextSize(option, self.font, self.font_scale, self.thickness)[0]
            text_x = (CAM_WIDTH - text_size[0]) // 2
            text_y = CAM_HEIGHT // 2 + 50 + i * 50
            
            if i == self.selected_option:
                padding = 10
                cv2.rectangle(frame, 
                            (text_x - padding, text_y - text_size[1] - padding),
                            (text_x + text_size[0] + padding, text_y + padding),
                            BLUE, 2)
            
            cv2.putText(frame, option, (text_x, text_y), self.font, self.font_scale, color, self.thickness)
    
    def handle_input(self, key):
        """
        Maneja la entrada del teclado para navegar por el menú.
        """
        if self.current_state == "MENU":
            num_options = len(self.menu_options)
            
            if key == ord('w') or key == ord('W'):
                self.selected_option = (self.selected_option - 1) % num_options
            elif key == ord('s') or key == ord('S'):
                self.selected_option = (self.selected_option + 1) % num_options
            elif key == ord(' ') or key == 13:  # Espacio o Enter
                if self.selected_option == 0:  # JUGAR
                    self.start_game()
                elif self.selected_option == 1:  # SALIR
                    return "QUIT"
        
        elif self.current_state == "GAME_OVER":
            num_options = len(self.game_over_options)
            
            if key == ord('w') or key == ord('W'):
                # CRÍTICO: Usar num_options para el módulo (estaba hardcodeado a 3)
                self.selected_option = (self.selected_option - 1) % num_options 
            elif key == ord('s') or key == ord('S'):
                # CRÍTICO: Usar num_options para el módulo (estaba hardcodeado a 3)
                self.selected_option = (self.selected_option + 1) % num_options
            elif key == ord(' ') or key == 13:  # Espacio o Enter
                if self.selected_option == 0:  # REINICIAR
                    self.restart_game()
                elif self.selected_option == 1:  # MENU PRINCIPAL
                    self.return_to_menu()
                elif self.selected_option == 2:  # SALIR
                    return "QUIT"
        
        return None
    
    def start_game(self):
        """
        Inicia una nueva partida.
        """
        self.current_state = "PLAYING"
        self.game.running = True
        self.reset_game_state()
        print("¡Juego iniciado!")
    
    def restart_game(self):
        """
        Reinicia la partida actual.
        """
        self.current_state = "PLAYING"
        self.game.running = True
        self.reset_game_state()
        print("¡Partida reiniciada!")
    
    def return_to_menu(self):
        """
        Regresa al menú principal.
        """
        self.current_state = "MENU"
        self.selected_option = 0
        print("Regresando al menú principal...")
    
    def game_over(self):
        """
        Cambia al estado de Game Over.
        """
        self.current_state = "GAME_OVER"
        self.selected_option = 0
        print("¡Game Over!")
    
    def reset_game_state(self):
        """
        Reinicia el estado del juego a los valores iniciales.
        """
        # Limpiar todos los sprites existentes
        self.game.all_sprites.empty()
        self.game.enemies.empty()
        self.game.bullets.empty()
        
        # Resetear la puntuación
        self.game.score = 0
        
        # Recrear el jugador
        # CRÍTICO: Las importaciones deben estar al inicio del archivo, no aquí.
        self.game.player = Player()
        self.game.all_sprites.add(self.game.player)
        
        # Recrear los enemigos
        # Usamos el número de enemigos definido en settings (ENEMY_SPAWN_COUNT)
        for _ in range(ENEMY_SPAWN_COUNT):
            # Llamamos a la función auxiliar de GameEngine si existe, 
            # sino recreamos la lógica de spawn con las coordenadas que Enemy espera.
            if hasattr(self.game, '_spawn_enemy'):
                self.game._spawn_enemy()
            else:
                enemy_x = random.randrange(0, SCREEN_WIDTH)
                enemy_y = random.randrange(50, SCREEN_HEIGHT // 4)
                enemy = Enemy(enemy_x, enemy_y)
                self.game.all_sprites.add(enemy)
                self.game.enemies.add(enemy)
        
        # Resetear el control de disparo
        self.game.last_shot = 0
        
        print("Estado del juego reiniciado")
    
    # CRÍTICO: NUEVO MÉTODO PARA ENTRADA DE OPENCV
    def handle_input_cv2(self, cv2_key_code):
        """
        Recibe el código de tecla ASCII/CV2 y lo pasa al manejador principal.
        """
        # cv2.waitKey devuelve el valor ASCII de la tecla presionada.
        # Simplemente pasamos ese valor al handle_input original.
        return self.handle_input(cv2_key_code)
    
    def is_playing(self):
        """
        Retorna True si el juego está en estado PLAYING.
        """
        return self.current_state == "PLAYING"
    
    def should_quit(self):
        """
        Retorna True si el usuario quiere salir del juego.
        """
        # Este método no es necesario si handle_input devuelve "QUIT", 
        # pero se mantiene para compatibilidad.
        return self.current_state == "QUIT"