DEBUG = False
PLAYER_SIZE = 64
SNAKE_INIT_SIZE = 3

# Resourcers
GRASS_SPRITE = "assets/grass.jpg"
SNAKE_HEAD_SPRITE = "assets/snake_head.png"
SNAKE_BODY_SPRITE = "assets/snake_skin.png"
SNAKE_TAIL_SPRITE = "assets/snake_tail.png"
EAT_EGG_SFX = "assets/power-up.mp3"
GAME_OVER_SFX = "assets/game-over.mp3"
EGG_SPRITE = "assets/egg.png"
MUSIC = "assets/8-bit-arcade.mp3"

# PATH CALCULATION FUNCTION
def get_path(file : str):
    import os, sys
    base_dir = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, file)