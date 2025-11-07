# game_logic/menu.py

import cv2
import numpy as np
import random
import pygame
# Importación de constantes
# 💥 ELIMINAMOS CAM_WIDTH, CAM_HEIGHT de la importación
from .settings import (SCREEN_WIDTH, SCREEN_HEIGHT, 
                       SCREEN_SIZE_OPTIONS, WHITE, BLACK, BLUE, RED, YELLOW, ENEMY_SPAWN_COUNT)

# Importación de clases de sprites (CRÍTICO: Necesario para reset_game_state)
from .player import Player
from .enemy import Enemy


class GameMenu:
    """
    Sistema de menú para el juego Space Invaders Origami.
    Maneja la interfaz de usuario y los estados del juego (MENU, OPTIONS, PLAYING, GAME_OVER).
    """
    
    def __init__(self, game_engine):
        self.game = game_engine
        self.current_state = "MENU"  
        
        self.menu_options = ["JUGAR", "OPCIONES", "SALIR"]
        
        self.game_over_options = ["REINICIAR", "MENU PRINCIPAL", "SALIR"] 
        
        self.pause_options = ["CONTINUAR...", "MENU PRINCIPAL"]
        
        # CRÍTICO: Las opciones de pantalla se toman directamente de settings.py
        self.screen_menu_options = SCREEN_SIZE_OPTIONS
        
        self.selected_option = 0
        self.pause_selected_option = 0      
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1.0
        self.thickness = 2
        
    # 💥 Método draw actualizado para recibir las dimensiones de la cámara
    def draw(self, frame, cam_width, cam_height):
        """
        Método central de dibujo llamado por GameEngine (Alta Cohesión).
        Recibe las dimensiones reales de la ventana CV2 para el centrado.
        """
        # Maneja la pantalla de pausa
        if self.is_playing() and self.game.is_paused:
            self.draw_pause(frame, cam_width, cam_height)
            return
        
        if self.current_state == "MENU":
            self.draw_menu(frame, cam_width, cam_height)
        elif self.current_state == "OPTIONS":
            self.draw_options_menu(frame, cam_width, cam_height)
        elif self.current_state == "GAME_OVER":
            self.draw_game_over(frame, cam_width, cam_height)
            
    # 💥 Método draw_menu actualizado para usar cam_width y cam_height
    def draw_menu(self, frame, cam_width, cam_height):
        """
        Dibuja el menú principal en el frame de la cámara.
        """
        # Fondo semi-transparente
        overlay = frame.copy()
        # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
        cv2.rectangle(overlay, (0, 0), (cam_width, cam_height), (0, 0, 0), -1) 
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Título del juego
        title_text = "SPACE INVADERS ORIGAMI"
        title_size = cv2.getTextSize(title_text, self.font, 1.5, 3)[0]
        # 💥 Reemplazar CAM_WIDTH por el argumento
        title_x = (cam_width - title_size[0]) // 2 
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
            # 💥 Reemplazar CAM_WIDTH por el argumento
            text_x = (cam_width - text_size[0]) // 2
            text_y = 150 + i * 30
            cv2.putText(frame, instruction, (text_x, text_y), self.font, 0.6, WHITE, 2)
            
        
        # Opciones del menú
        for i, option in enumerate(self.menu_options):
            color = YELLOW if i == self.selected_option else WHITE
            text_size = cv2.getTextSize(option, self.font, self.font_scale, self.thickness)[0]
            # 💥 Reemplazar CAM_WIDTH por el argumento
            text_x = (cam_width - text_size[0]) // 2
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
                   
    
    # 💥 Método draw_options_menu actualizado para usar cam_width y cam_height
    def draw_options_menu(self, frame, cam_width, cam_height):
        """
        Dibuja el submenú de opciones de tamaño de pantalla.
        """
        overlay = frame.copy()
        # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
        cv2.rectangle(overlay, (0, 0), (cam_width, cam_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        title_text = "SELECCIONAR TAMAÑO DE PANTALLA"
        title_size = cv2.getTextSize(title_text, self.font, 1.0, 2)[0]
        # 💥 Reemplazar CAM_WIDTH por el argumento
        title_x = (cam_width - title_size[0]) // 2
        cv2.putText(frame, title_text, (title_x, 50), self.font, 1.0, YELLOW, 2)
        
        # Opciones de tamaño
        for i, (name, size) in enumerate(self.screen_menu_options):
            color = BLUE if i == self.selected_option else WHITE
            display_text = f"{name}"
            
            text_size = cv2.getTextSize(display_text, self.font, 0.8, self.thickness)[0]
            # 💥 Reemplazar CAM_WIDTH por el argumento
            text_x = (cam_width - text_size[0]) // 2
            text_y = 150 + i * 50
            
            if i == self.selected_option:
                padding = 10
                cv2.rectangle(frame, 
                            (text_x - padding, text_y - text_size[1] - padding),
                            (text_x + text_size[0] + padding, text_y + padding),
                            RED, 2)
            
            cv2.putText(frame, display_text, (text_x, text_y), self.font, 0.8, color, self.thickness)
        
        # Opción de Volver
        # 💥 Reemplazar CAM_HEIGHT por el argumento
        back_text = "VOLVER (ESC)"
        cv2.putText(frame, back_text, (50, cam_height - 50), self.font, 0.5, WHITE, 1)
    
    # 💥 Método draw_game_over actualizado para usar cam_width y cam_height
    def draw_game_over(self, frame, cam_width, cam_height):
        """
        Dibuja la pantalla de Game Over.
        """
        # Fondo semi-transparente
        overlay = frame.copy()
        # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
        cv2.rectangle(overlay, (0, 0), (cam_width, cam_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Texto Game Over
        game_over_text = "GAME OVER"
        text_size = cv2.getTextSize(game_over_text, self.font, 2.0, 4)[0]
        # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
        text_x = (cam_width - text_size[0]) // 2
        text_y = cam_height // 2 - 50
        cv2.putText(frame, game_over_text, (text_x, text_y), self.font, 2.0, RED, 4)
        
        # Muestra la puntuación final
        score_text = f"PUNTUACION: {self.game.score}"
        score_size = cv2.getTextSize(score_text, self.font, 1.0, 2)[0]
        # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
        score_x = (cam_width - score_size[0]) // 2
        score_y = cam_height // 2
        cv2.putText(frame, score_text, (score_x, score_y), self.font, 1.0, WHITE, 2)

        # Opciones
        for i, option in enumerate(self.game_over_options):
            color = YELLOW if i == self.selected_option else WHITE
            text_size = cv2.getTextSize(option, self.font, self.font_scale, self.thickness)[0]
            # 💥 Reemplazar CAM_WIDTH, CAM_HEIGHT por los argumentos
            text_x = (cam_width - text_size[0]) // 2
            text_y = cam_height // 2 + 50 + i * 50
            
            if i == self.selected_option:
                padding = 10
                cv2.rectangle(frame, 
                            (text_x - padding, text_y - text_size[1] - padding),
                            (text_x + text_size[0] + padding, text_y + padding),
                            BLUE, 2)
            
            cv2.putText(frame, option, (text_x, text_y), self.font, self.font_scale, color, self.thickness)
    

    def draw_pause(self, frame, cam_width, cam_height):
        """
        Dibuja la pantalla de Pausa, incluyendo las opciones para continuar o volver al menú.
        """
        # Fondo semi-transparente (similar a Game Over)
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, 0), (cam_width, cam_height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.8, frame, 0.2, 0, frame)
        
        # Texto PAUSA
        pause_text = "PAUSA"
        text_size = cv2.getTextSize(pause_text, self.font, 2.0, 4)[0]
        text_x = (cam_width - text_size[0]) // 2
        text_y = cam_height // 2 - 100 # Movemos el título más arriba
        cv2.putText(frame, pause_text, (text_x, text_y), self.font, 2.0, YELLOW, 4)
        
        # Opciones de Pausa
        for i, option in enumerate(self.pause_options):
            color = BLUE if i == self.pause_selected_option else WHITE
            text_size = cv2.getTextSize(option, self.font, self.font_scale, self.thickness)[0]
            text_x = (cam_width - text_size[0]) // 2
            text_y = cam_height // 2 + i * 50 # Dibujamos las opciones
            
            # Resaltar la opción seleccionada
            if i == self.pause_selected_option:
                padding = 10
                cv2.rectangle(frame, 
                            (text_x - padding, text_y - text_size[1] - padding),
                            (text_x + text_size[0] + padding, text_y + padding),
                            YELLOW, 2)
            
            cv2.putText(frame, option, (text_x, text_y), self.font, self.font_scale, color, self.thickness)

        # Indicador de selección (opcional, pero ayuda)
        indicator_text = ">>"
        cv2.putText(frame, indicator_text, (text_x - 70, cam_height // 2 + self.pause_selected_option * 50), 
                   self.font, self.font_scale, YELLOW, self.thickness)

    def handle_input(self, event):
        """
        Maneja la entrada del teclado para navegar por el menú.
        (Recibe eventos de Pygame)
        """
        if event.type == pygame.KEYDOWN:
            
            # Dejamos el debug aquí, aunque ahora el shim es el que lo activará
            print(f"DEBUG: Tecla detectada: {pygame.key.name(event.key)}")
            
        if event.type != pygame.KEYDOWN:
            return None
        
        key = event.key
        

        
        # Lógica de navegación (W/S) y selección (Espacio/Enter)
        if self.current_state == "MENU":
            num_options = len(self.menu_options)
            
            if key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % num_options
            elif key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % num_options
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.selected_option == 0:  # JUGAR
                    self.start_game()
                elif self.selected_option == 1:  # OPCIONES
                    self.current_state = "OPTIONS"
                    self.selected_option = 0
                elif self.selected_option == 2:  # SALIR
                    return "QUIT"
        
        # BLOQUE: Manejo de entrada del menú de opciones
        elif self.current_state == "OPTIONS":
            num_options = len(self.screen_menu_options)
            
            if key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % num_options
            elif key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % num_options
            elif key == pygame.K_ESCAPE: # Tecla ESCAPE para volver
                self.return_to_menu()
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                # 1. Obtener la opción seleccionada
                _, size_tuple = self.screen_menu_options[self.selected_option]
                
                # 2. Llamar usando self.game (la instancia de GameEngine)
                self.game.set_screen_size(size_tuple[0], size_tuple[1])
                
                # 3. Volver al menú principal
                self.return_to_menu()
                
        elif self.current_state == "GAME_OVER":
            num_options = len(self.game_over_options)
            
            if key == pygame.K_w:
                self.selected_option = (self.selected_option - 1) % num_options
            elif key == pygame.K_s:
                self.selected_option = (self.selected_option + 1) % num_options
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.selected_option == 0:  # REINICIAR
                    self.restart_game()
                elif self.selected_option == 1:  # MENU PRINCIPAL
                    self.return_to_menu()
                elif self.selected_option == 2:  # SALIR
                    return "QUIT"
        # ... (Después de la lógica de GAME_OVER) ...

        # BLOQUE: Manejo de entrada cuando está en Pausa (Sub-estado de PLAYING)
        if self.is_playing() and self.game.is_paused:
            num_options = len(self.pause_options)
            
            if key == pygame.K_w:
                self.pause_selected_option = (self.pause_selected_option - 1) % num_options
            elif key == pygame.K_s:
                self.pause_selected_option = (self.pause_selected_option + 1) % num_options
            elif key == pygame.K_SPACE or key == pygame.K_RETURN:
                if self.pause_selected_option == 0: # CONTINUAR
                    # 1. Quitar la pausa
                    self.game.is_paused = False
                    # 2. Resetear el puntero
                    self.pause_selected_option = 0
                elif self.pause_selected_option == 1: # VOLVER AL MENU PRINCIPAL
                    # 1. Quitar la pausa
                    self.game.is_paused = False
                    # 2. Reiniciar el estado del juego (para limpiar enemigos y puntuación)
                    self.reset_game_state() 
                    # 3. Regresar al menú principal
                    self.return_to_menu() 
                  
                
        
        return None
    
    # ----------------------------------------------------
    # CRÍTICO: Método para manejar la entrada de OpenCV
    def handle_input_cv2_shim(self, pygame_key_code):
        """
        Método auxiliar para simular un evento de Pygame a partir de una tecla CV2.
        Esto soluciona el problema de foco de entrada.
        """
        # Crear un objeto de evento simulado con el código de tecla Pygame correcto
        simulated_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame_key_code})
        
        # Llamar al manejador de entrada real con el evento simulado
        menu_action = self.handle_input(simulated_event)
        
        # Si el menú retorna 'QUIT', se lo pasamos al GameEngine
        if menu_action == "QUIT":
            self.game.running = False
            
    # ----------------------------------------------------
    
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
        self.game.player = Player()
        self.game.all_sprites.add(self.game.player)
        
        # Recrear los enemigos
        for _ in range(ENEMY_SPAWN_COUNT):
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
    
    def is_playing(self):
        """
        Retorna True si el juego está en estado PLAYING.
        """
        return self.current_state == "PLAYING"
    
    def should_quit(self):
        """
        Retorna True si el usuario quiere salir del juego.
        """
        return self.current_state == "QUIT"