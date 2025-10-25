# game_logic/camera.py
import cv2
import numpy as np
# Eliminamos la importación de pygame aquí si no se usa directamente
# La dejamos por si acaso, pero la lógica de clock.tick se va
import pygame 

# Asegúrate de que estas constantes estén disponibles
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
        
        # Eliminamos self.running
        
        # Factores de escala
        self.SCALE_FACTOR_X = CAM_WIDTH / SCREEN_WIDTH
        self.SCALE_FACTOR_Y = CAM_HEIGHT / SCREEN_HEIGHT
        
        self.current_frame = None

    def process_frame(self, frame):
        """
        Detecta el objeto de color rojo y devuelve su centro X en coordenadas de CÁMARA.
        """
        # (El código de process_frame se mantiene igual ya que es SRP)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # ... (código de detección de color, contornos y centro X)
        mask1 = cv2.inRange(hsv, RED_LOWER_H1, RED_UPPER_H1)
        mask2 = cv2.inRange(hsv, RED_LOWER_H2, RED_UPPER_H2)
        mask = mask1 + mask2
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            
            if area > 100: 
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    center_x_cam = int(M["m10"] / M["m00"])
                    center_y_cam = int(M["m01"] / M["m00"])
                    
                    # Dibujar el centro detectado en el frame
                    cv2.circle(frame, (center_x_cam, center_y_cam), 10, (0, 255, 0), -1)
                    
                    # Devolver la posición en coordenadas de PANTALLA de Pygame
                    screen_x = int(center_x_cam * SCREEN_WIDTH / CAM_WIDTH)
                    return screen_x # CRÍTICO: Devolver la posición X convertida
                    
        return None

    # CRÍTICO: Renombrado de run() a get_position() y eliminación del bucle
    def get_position(self):
        """
        Captura un solo frame, lo procesa, dibuja el overlay y devuelve la posición X.
        Responsabilidad Única: Devolver el dato de entrada.
        """
        if not self.cap.isOpened():
             return None

        ret, frame = self.cap.read() 
        if not ret:
            return None
        
        # Espejo el frame para que el movimiento sea intuitivo
        frame = cv2.flip(frame, 1) 
        self.current_frame = frame.copy()

        # 1. Procesamiento de Visión: Obtener la posición X convertida a Pygame
        # No hay lógica de 'is_playing()' aquí; solo se obtienen datos.
        screen_x = self.process_frame(frame)
        
        # 2. DIBUJAR EL OVERLAY DEL JUEGO O MENÚ
        sprites_data = self.game_engine.get_sprites_data()
        self._draw_overlay_on_frame(self.current_frame, sprites_data)
        
        # 3. Manejo de Entrada (Solo para la ventana de OpenCV, no para el bucle del juego)
        key = cv2.waitKey(1)
        
        # Solo procesar la entrada si hay una tecla presionada
        if key != -1: 
            # Usamos el nuevo método handle_input_cv2
            menu_action = self.game_engine.menu.handle_input_cv2(key) 
            
            if menu_action == "QUIT":
                self.game_engine.running = False
                
            # Control de cierre forzado 'q' (ord('q') es 113)
            if key == ord('q'):
                self.game_engine.running = False 
        
        # 4. Devolver la posición detectada (o None)
        return screen_x

    def _draw_overlay_on_frame(self, frame, sprites_data):
        """
        Función auxiliar para dibujar el overlay.
        Se mantiene igual, solo cambia cómo se llama al menú.
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
                
                # Conversión y dibujo de rectángulos
                cam_x1 = int(rect.left * self.SCALE_FACTOR_X)
                cam_y1 = int(rect.top * self.SCALE_FACTOR_Y)
                cam_x2 = int(rect.right * self.SCALE_FACTOR_X)
                cam_y2 = int(rect.bottom * self.SCALE_FACTOR_Y)

                color_bgr = (color[2], color[1], color[0]) 

                cv2.rectangle(frame, (cam_x1, cam_y1), (cam_x2, cam_y2), color_bgr, 2)
            
        cv2.imshow('Space Invaders Origami - Camara', frame)


    def release_resources(self):
        """Llamado al final para liberar la cámara."""
        self.cap.release()
        cv2.destroyAllWindows()