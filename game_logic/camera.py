# game_logic/camera.py
import cv2
import numpy as np
import time
import pygame # <--- NECESARIO para usar clock.tick()

from .settings import CAM_WIDTH, CAM_HEIGHT, RED_LOWER, RED_UPPER, SCREEN_WIDTH, SCREEN_HEIGHT

class CameraHandler:
    
    def __init__(self, game_engine):
        # Referencia al motor del juego para enviarle la posición
        self.game = game_engine 
        
        # 1. Inicializar la cámara
        self.cap = cv2.VideoCapture(0)
        
        # 2. Configurar la resolución de la cámara
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        
        # 3. Bandera para controlar el bucle de la cámara
        self.running = True

    def process_frame(self, frame):
        """
        Detecta el objeto de color rojo y devuelve su centro X.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, RED_LOWER, RED_UPPER)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            
            if cv2.contourArea(largest_contour) > 1000:
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    center_x = int(M["m10"] / M["m00"])
                    
                    # Dibuja el círculo en la imagen original
                    center_y = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (center_x, center_y), 10, (0, 255, 0), -1)
                    
                    return center_x
        return None

    def run(self):
        """
        Bucle principal de la cámara, captura, procesa, actualiza la lógica del juego y dibuja el overlay.
        """
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read() 
            if not ret:
                break
            
            frame = cv2.flip(frame, 1) 
            
            # 1. Procesamiento de Visión (solo si estamos jugando)
            new_x = None
            if self.game.menu.is_playing():
                new_x = self.process_frame(frame)
            
            # 2. Control Lógico (Envía posición a Pygame)
            if new_x is not None:
                screen_x = int(new_x * SCREEN_WIDTH / CAM_WIDTH)
                self.game.player.set_position_from_camera(screen_x)

            # -----------------------------------------------------
            # ¡CRÍTICO! LLAMADAS AL MOTOR DEL JUEGO PARA ACTUALIZAR LÓGICA
            # -----------------------------------------------------
            # 2a. Activa el disparo automático (en _handle_input).
            self.game._handle_input() 
            
            # 2b. Mueve enemigos y balas, y verifica colisiones.
            self.game._update_game_state() 
            # -----------------------------------------------------
            
            if not self.game.running:
                self.running = False 

            # -----------------------------------------------------------
            # 3. DIBUJAR EL OVERLAY DEL JUEGO O MENÚ
            # -----------------------------------------------------------
            if self.game.menu.current_state == "MENU":
                self.game.menu.draw_menu(frame)
            elif self.game.menu.current_state == "GAME_OVER":
                self.game.menu.draw_game_over(frame)
            elif self.game.menu.is_playing():
                # Dibujar sprites del juego solo si estamos jugando
                sprites_data = self.game.get_sprites_data()
                
                # Factores de escala (se mantienen correctos)
                SCALE_FACTOR_X = CAM_WIDTH / SCREEN_WIDTH
                SCALE_FACTOR_Y = CAM_HEIGHT / SCREEN_HEIGHT
                
                for data in sprites_data:
                    rect = data['rect']
                    color = data['color']
                    
                    # A. Conversión de coordenadas
                    cam_x1 = int(rect.left * SCALE_FACTOR_X)
                    cam_y1 = int(rect.top * SCALE_FACTOR_Y)
                    cam_x2 = int(rect.right * SCALE_FACTOR_X)
                    cam_y2 = int(rect.bottom * SCALE_FACTOR_Y)

                    # B. Conversión de color Pygame (RGB) a OpenCV (BGR)
                    color_bgr = (color[2], color[1], color[0]) 

                    # C. Dibujar el rectángulo sobre el frame de la cámara
                    cv2.rectangle(frame, (cam_x1, cam_y1), (cam_x2, cam_y2), color_bgr, 2)
                
            # -----------------------------------------------------------

            # 4. Muestra la ventana de OpenCV
            cv2.imshow('Space Invaders Origami - Camara', frame)
            
            # 5. Espera por eventos y control de tiempo
            key = cv2.waitKey(1)
            
            # Manejar entrada del menú
            if key != -1:
                result = self.game.menu.handle_input(key)
                if result == "QUIT":
                    self.running = False
            
            if key == ord('q') or cv2.getWindowProperty('Space Invaders Origami - Camara', cv2.WND_PROP_VISIBLE) < 1:
                self.running = False
            
            # Usa el reloj del motor para mantener la tasa de refresco (60 FPS)
            self.game.clock.tick(60) 

        # Limpieza
        self.cap.release()
        cv2.destroyAllWindows()