# game_logic/camera.py
import cv2
import numpy as np
import pygame 

# Asegúrate de que estas constantes estén disponibles en settings.py
from .settings import (
    CAM_WIDTH, CAM_HEIGHT, 
    RED_LOWER_H1, RED_LOWER_H2, 
    RED_UPPER_H1, RED_UPPER_H2, 
    SCREEN_WIDTH, SCREEN_HEIGHT
)

class CameraHandler:
    
    def __init__(self, game_engine):
        """
        Inicializa la cámara y los factores de escala.
        """
        self.game_engine = game_engine 
        self.cap = cv2.VideoCapture(0)
        
        # Configurar la resolución de la cámara
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        
        self.running = True 
        
        # Factores para convertir coordenadas de Pygame a Cámara (y viceversa)
        self.SCALE_FACTOR_X = CAM_WIDTH / SCREEN_WIDTH
        self.SCALE_FACTOR_Y = CAM_HEIGHT / SCREEN_HEIGHT
        
        # Bandera para controlar la ventana de OpenCV
        self.window_visible = True
        self.current_frame = None # Almacena el último frame para el overlay

    def process_frame(self, frame):
        """
        Detecta el objeto de color rojo y devuelve su centro X en coordenadas de CÁMARA.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # CRÍTICO: Usar doble máscara para el color rojo (se envuelve en el rango HSV)
        mask1 = cv2.inRange(hsv, RED_LOWER_H1, RED_UPPER_H1)
        mask2 = cv2.inRange(hsv, RED_LOWER_H2, RED_UPPER_H2)
        mask = mask1 + mask2 # Fusionar ambas máscaras
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # Usar un umbral de área bajo (100) para mayor sensibilidad
            if area > 100: 
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    center_x_cam = int(M["m10"] / M["m00"])
                    center_y_cam = int(M["m01"] / M["m00"])
                    
                    # Dibujar el centro detectado en el frame
                    cv2.circle(frame, (center_x_cam, center_y_cam), 10, (0, 255, 0), -1)
                    
                    return center_x_cam
                    
        return None

    def run(self):
        """
        Bucle principal de la cámara (sustituye al bucle de Pygame)
        Captura, procesa, actualiza la lógica del juego y dibuja el overlay.
        """
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read() 
            if not ret:
                break
            
            # Espejo el frame para que el movimiento sea intuitivo
            frame = cv2.flip(frame, 1) 
            self.current_frame = frame.copy() # Almacena el frame para el overlay

            # 1. Procesamiento de Visión
            new_x_cam = None
            # Procesar solo si estamos jugando (lógica de menú de develop2)
            if self.game_engine.menu.is_playing(): 
                new_x_cam = self.process_frame(frame)
            
            # 2. Control Lógico (Envía posición a Pygame)
            if new_x_cam is not None:
                # CONVERSIÓN CRÍTICA: Convertir de coordenadas de cámara a Pygame
                screen_x = int(new_x_cam * SCREEN_WIDTH / CAM_WIDTH)
                self.game_engine.player.set_position_from_camera(screen_x)

            # -----------------------------------------------------
            # Actualizaciones del Motor de Juego (de develop2)
            # -----------------------------------------------------
            self.game_engine._handle_input() 
            self.game_engine._update_game_state() 
            
            if not self.game_engine.running:
                self.running = False 

            # -----------------------------------------------------------
            # 3. DIBUJAR EL OVERLAY DEL JUEGO O MENÚ
            # -----------------------------------------------------------
            sprites_data = self.game_engine.get_sprites_data()
            self._draw_overlay_on_frame(self.current_frame, sprites_data)
            # -----------------------------------------------------------

            # 4. Control de Ventana y Tiempo
            # Manejar entrada del menú (de develop2)
            key = cv2.waitKey(1)
            if key != -1:
                result = self.game_engine.menu.handle_input(key)
                if result == "QUIT":
                    self.running = False
            
            # Control de cierre de ventana y tecla 'q'
            if key == ord('q') or cv2.getWindowProperty('Space Invaders Origami - Camara', cv2.WND_PROP_VISIBLE) < 1:
                self.running = False
            
            # Usa el reloj del motor para mantener la tasa de refresco (60 FPS)
            self.game_engine.clock.tick(60) 

        # Limpieza final
        self.release_resources()
        
    def _draw_overlay_on_frame(self, frame, sprites_data):
        """
        Función auxiliar para dibujar el overlay (lógica combinada de draw_overlay y run)
        """
        
        # Lógica para dibujar Menús
        if self.game_engine.menu.current_state == "MENU":
            self.game_engine.menu.draw_menu(frame)
        elif self.game_engine.menu.current_state == "GAME_OVER":
            self.game_engine.menu.draw_game_over(frame)
        
        # Lógica para dibujar Sprites del Juego
        if self.game_engine.menu.is_playing():
            for data in sprites_data:
                rect = data['rect']
                color = data['color']
                
                # A. Conversión de coordenadas Pygame a Cámara
                cam_x1 = int(rect.left * self.SCALE_FACTOR_X)
                cam_y1 = int(rect.top * self.SCALE_FACTOR_Y)
                cam_x2 = int(rect.right * self.SCALE_FACTOR_X)
                cam_y2 = int(rect.bottom * self.SCALE_FACTOR_Y)

                # B. Conversión de color Pygame (RGB) a OpenCV (BGR)
                color_bgr = (color[2], color[1], color[0]) 

                # C. Dibujar el rectángulo sobre el frame de la cámara
                cv2.rectangle(frame, (cam_x1, cam_y1), (cam_x2, cam_y2), color_bgr, 2)
            
        cv2.imshow('Space Invaders Origami - Camara', frame)


    def release_resources(self):
        """Llamado al final para liberar la cámara."""
        self.cap.release()
        cv2.destroyAllWindows()

# NOTA: Los métodos get_position() y draw_overlay() de HEAD se fusionaron en el método run().
# Solo se mantiene release_resources() para la limpieza final.