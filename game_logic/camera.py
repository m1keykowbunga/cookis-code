# game_logic/camera.py
import cv2
import numpy as np
import time
import pygame 

# Asegúrate de que estas constantes estén disponibles en settings.py
from .settings import CAM_WIDTH, CAM_HEIGHT, RED_LOWER_H1, RED_LOWER_H2,RED_UPPER_H1, RED_UPPER_H2, SCREEN_WIDTH, SCREEN_HEIGHT 

class CameraHandler:
    
    def __init__(self, game_engine):
        # ... (código __init__ sin cambios)
        self.game_engine = game_engine 
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
        self.running = True 
        self.SCALE_FACTOR_X = CAM_WIDTH / SCREEN_WIDTH
        self.SCALE_FACTOR_Y = CAM_HEIGHT / SCREEN_HEIGHT
        self.window_visible = True

    def process_frame(self, frame):
        """
        Detecta el objeto de color rojo y devuelve su centro X en coordenadas de Pygame.
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        mask1 = cv2.inRange(hsv, RED_LOWER_H1, RED_UPPER_H1)
        mask2 = cv2.inRange(hsv, RED_LOWER_H2, RED_UPPER_H2)
        mask = mask1 + mask2 # Fusionar ambas máscaras
        
        # Opcional: Descomenta esto para ver exactamente qué está detectando la máscara
        #cv2.imshow('Mask Debug', mask)
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            # ⚠️ AJUSTE CLAVE: Reducimos el umbral de 1000 a 100 para mejorar la sensibilidad.
            if area > 100: 
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    center_x_cam = int(M["m10"] / M["m00"])
                    center_y_cam = int(M["m01"] / M["m00"])
                    
                    # Dibujar el centro detectado
                    cv2.circle(frame, (center_x_cam, center_y_cam), 10, (0, 255, 0), -1)
                    
                    # CONVERSIÓN CRÍTICA: Convertir de coordenadas de cámara a Pygame
                    screen_x = int(center_x_cam * SCREEN_WIDTH / CAM_WIDTH)
                    
                    return screen_x
                    
        return None

    # === get_position() SIN CAMBIOS ===
    def get_position(self):
        """[NUEVO API] Captura y procesa un solo frame para devolver la posición X."""
        if not self.cap.isOpened() or not self.window_visible:
            return None
        
        ret, frame = self.cap.read() 
        if not ret:
            return None
            
        self.current_frame = cv2.flip(frame, 1)
        return self.process_frame(self.current_frame)
    
    # === draw_overlay() SIN CAMBIOS ===
    def draw_overlay(self, sprites_data):
        """[NUEVO API] Dibuja los rectángulos de Pygame sobre el último frame capturado."""
        if not hasattr(self, 'current_frame'):
            return 

        frame = self.current_frame.copy() 

        for data in sprites_data:
            rect = data['rect']
            color = data['color']
            
            cam_x1 = int(rect.left * self.SCALE_FACTOR_X)
            cam_y1 = int(rect.top * self.SCALE_FACTOR_Y)
            cam_x2 = int(rect.right * self.SCALE_FACTOR_X)
            cam_y2 = int(rect.bottom * self.SCALE_FACTOR_Y)

            color_bgr = (color[2], color[1], color[0]) 
            cv2.rectangle(frame, (cam_x1, cam_y1), (cam_x2, cam_y2), color_bgr, 2)
            
        cv2.imshow('Space Invaders Origami - Camara', frame)
        
        key = cv2.waitKey(1)
        if key == ord('q') or cv2.getWindowProperty('Space Invaders Origami - Camara', cv2.WND_PROP_VISIBLE) < 1:
            self.window_visible = False
            self.game_engine.running = False 

    # === release_resources() SIN CAMBIOS ===
    def release_resources(self):
        """Llamado por GameEngine al final para liberar la cámara."""
        self.cap.release()
        cv2.destroyAllWindows()