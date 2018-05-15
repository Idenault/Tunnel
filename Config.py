import pygame as pg

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (121, 89, 0)

# game settings
WIDTH = 1440
HEIGHT = 768
FPS = 30
TITLE = "TUNNEL!!!!!!!!"
BGCOLOR = DARKGREY


TILEPATH = ["NONE", "Assets/Imgs/leafy_ground01.png", "Assets/Imgs/ground06.png", "Assets/Imgs/rocky01.png", "Assets/Imgs/ground07.png", "Assets/Imgs/lava 2.png", "Assets/tree-ornament.png", "Assets/leafy_ground01.png"]
BGPATH = "Assets/2d-game-background-1.png"

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

PLAYER_ACC = 0.8
PLAYER_FRICTION = -0.12

FONT = pg.font.match_font("arial")

# res
STONE = 0
DIAMOND = 1
IRON = 2
SILVER = 3
GOLD = 4

# Items
FIREBALL = 0
JETPACK = 1




