# main.py
import os
# --- Solución Final para el error libGL/Mesa ---
# Forzamos a Pygame/SDL a usar el driver DUMMY (el más compatible)
os.environ['SDL_VIDEODRIVER'] = 'dummy' 
# ----------------------------------------

from game_logic.game_engine import GameEngine

if __name__ == '__main__':
    game = GameEngine()
    game.run()