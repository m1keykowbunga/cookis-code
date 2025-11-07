# game_logic/camera.py

import cv2
import numpy as np

# Importación de constantes
from .settings import (
    CAM_BASE_WIDTH, CAM_BASE_HEIGHT, CAM_OPTIONS, # <-- Nuevas constantes de configuración
    RED_LOWER_H1, RED_LOWER_H2, 
    RED_UPPER_H1, RED_UPPER_H2, 
    SCREEN_WIDTH, SCREEN_HEIGHT # SCREEN_WIDTH/HEIGHT son las globales iniciales
)

class CameraHandler:
    
    def __init__(self, game_engine):
        self.game_engine = game_engine 
        self.cap = None
        
        # 1. Variables de instancia para las dimensiones de la cámara
        self.CAM_WIDTH = CAM_BASE_WIDTH 
        self.CAM_HEIGHT = CAM_BASE_HEIGHT
        
        self.SCALE_FACTOR_X = None
        self.SCALE_FACTOR_Y = None
        
        self.current_frame = None

        # 2. Configuración inicial de la cámara, usando la resolución de pantalla inicial
        # Esto calcula CAM_WIDTH/HEIGHT y abre la captura.
        self.reconfigure_camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    
    # ----------------------------------------------------
    # MÉTODOS DE CONFIGURACIÓN DINÁMICA
    # ----------------------------------------------------

    def reconfigure_camera(self, new_screen_width, new_screen_height):
        """
        Calcula las nuevas dimensiones internas de la cámara según la resolución de pantalla,
        ajusta los factores de escala y reinicia la captura de video.
        """
        # 1. Obtener la nueva resolución de la cámara (CAM_WIDTH, CAM_HEIGHT)
        screen_size_tuple = (new_screen_width, new_screen_height)
        
        # Buscar el mapeo en CAM_OPTIONS. Si no se encuentra, usar los valores base.
        new_cam_size = CAM_OPTIONS.get(screen_size_tuple, (CAM_BASE_WIDTH, CAM_BASE_HEIGHT))
        
        self.CAM_WIDTH = new_cam_size[0]
        self.CAM_HEIGHT = new_cam_size[1]
        
        # 2. Reiniciar la captura de video con las nuevas dimensiones
        if self.cap and self.cap.isOpened():
            self.cap.release()
            
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.CAM_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.CAM_HEIGHT)
        
        # 3. Actualizar los factores de escala (Conversión de CAM -> SCREEN)
        self.SCALE_FACTOR_X = self.CAM_WIDTH / new_screen_width
        self.SCALE_FACTOR_Y = self.CAM_HEIGHT / new_screen_height

        print(f"Cámara reconfigurada a: {self.CAM_WIDTH}x{self.CAM_HEIGHT}")

    # ----------------------------------------------------
    # MÉTODOS DE PROCESAMIENTO
    # ----------------------------------------------------

    def process_frame(self, frame):
        """Detecta el objeto de color rojo y devuelve su centro X en coordenadas de PANTALLA de Pygame."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
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
                    
                    current_screen_width = self.game_engine.screen.get_width()
                    
                    screen_x = int(center_x_cam * SCREEN_WIDTH / self.CAM_WIDTH) 
                    return screen_x 
                    
        return None

    def get_position(self):
        """Captura un solo frame, lo procesa y devuelve la posición X. No maneja el dibujo ni la entrada."""
        if not self.cap or not self.cap.isOpened(): # Comprobación de seguridad
             return None

        ret, frame = self.cap.read() 
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1) 
        self.current_frame = frame.copy()

        screen_x = self.process_frame(frame)
        
        return screen_x

    def draw_window(self, sprites_data):
        """Aplica el overlay de sprites/menú al frame actual y lo muestra con CV2."""
        if self.current_frame is None:
            return 0

        # Ajuste de tamaño de la ventana de CV2 si es necesario (No es estrictamente necesario,
        # pero asegura que la ventana de CV2 muestre la resolución correcta)
        frame_to_display = self.current_frame.copy()
        
        # 1. Lógica para dibujar Sprites del Juego
        if self.game_engine.menu.is_playing() and not self.game_engine.is_paused:
            for data in sprites_data:
                rect = data['rect']
                color = data['color']
                
                # Conversión de coordenadas Pygame a coordenadas de Cámara (CV)
                
                cam_x1 = int(rect.left * self.SCALE_FACTOR_X)
                cam_y1 = int(rect.top * self.SCALE_FACTOR_Y)
                cam_x2 = int(rect.right * self.SCALE_FACTOR_X)
                cam_y2 = int(rect.bottom * self.SCALE_FACTOR_Y)

                color_bgr = (color[2], color[1], color[0]) 

                cv2.rectangle(frame_to_display, (cam_x1, cam_y1), (cam_x2, cam_y2), color_bgr, 2)
                
            self._draw_score(frame_to_display, self.CAM_WIDTH, self.CAM_HEIGHT)
            self._draw_health_bar(frame_to_display, self.CAM_WIDTH, self.CAM_HEIGHT)
        
        # 2. Dibujar Menús (GAME_OVER, MENU, OPTIONS)
        if not self.game_engine.menu.is_playing() or self.game_engine.is_paused:
            # El menú necesita saber el tamaño de la ventana de CV2 para dibujar su contenido.
            # Le pasamos el tamaño actual de la cámara como argumento.
            self.game_engine.menu.draw(frame_to_display, self.CAM_WIDTH, self.CAM_HEIGHT)
            
        cv2.imshow('Space Invaders Origami - Camara', frame_to_display)
        
        # 3. Manejo de entrada
        key = cv2.waitKey(1)
        
        if key == ord('q'):
             self.game_engine.running = False
        return key

    
    def release_resources(self):
        """Llamado al final para liberar la cámara."""
        if self.cap:
             self.cap.release()
        cv2.destroyAllWindows()
        
    #marcador de puntuación
    def _draw_score(self, frame, cam_width, cam_height):
        """Dibuja el marcador de puntuación en la esquina superior."""
        score_text = f"PUNTOS: {self.game_engine.score}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        
        # Coordenadas: Arriba a la derecha (Margen de 20px)
        text_size = cv2.getTextSize(score_text, font, 0.7, 2)[0]
        text_x = cam_width - text_size[0] - 20
        text_y = 30
        
        cv2.putText(frame, score_text, (text_x, text_y), font, 0.7, (255, 255, 255), 2) # Blanco
        
    def _draw_health_bar(self, frame, cam_width, cam_height):
        """Dibuja la barra de vida del jugador (nave azul) en la esquina inferior izquierda."""
        player = self.game_engine.player
        
        # Chequeo CRÍTICO: Asegurarse de que el objeto player exista y tenga salud.
        if player is None or not hasattr(player, 'health') or player.health <= 0:
            return
            
        health_ratio = player.health / player.max_health
        bar_width = cam_width // 4 
        bar_height = 15
        
        # Posición: Abajo a la izquierda (Margen de 20px)
        x = 20
        y = cam_height - bar_height - 20
        
        # Dibujar Fondo (Rojo) (BGR: 0, 0, 255)
        cv2.rectangle(frame, (x, y), (x + bar_width, y + bar_height), (0, 0, 255), -1) 
        
        # Dibujar Vida Actual (Verde) (BGR: 0, 255, 0)
        fill_width = int(bar_width * health_ratio)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + bar_height), (0, 255, 0), -1) 
        
        # Dibujar Borde (Blanco) (BGR: 255, 255, 255)
        cv2.rectangle(frame, (x, y), (x + bar_width, y + bar_height), (255, 255, 255), 2)
        
        