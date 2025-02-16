import pygame

# CONSTANT GAME VARIABLES
X_DIM = 600
Y_DIM = 500

FPS = 120
FINAL_DELAY = 3000

CREATETREE_TIMER_DELAY = 400
CREATEFLAG_TIMER_DELAY = 1000
CREATESNOWBALL_TIMER_DELAY = 2000

CREATETREE_EVENT = pygame.USEREVENT
CREATEFLAG_EVENT = pygame.USEREVENT + 1
CREATESNOWBALL_EVENT = pygame.USEREVENT + 1


BACKGROUND_COLOR = (255, 255, 255)  # white
SKIER_PNG_MAP = {
	-2: "skier_left2.png", 
	-1: "skier_left1.png", 
	0: "skier_down.png", 
	1: "skier_right1.png", 
	2: "skier_right2.png", 
	"crash": "skier_crash.png", 
	"tree": "skier_tree.png", 
	"flag": "skier_flag.png", 
}
DEFAULT_SKIER = SKIER_PNG_MAP[0]
BACKGROUND_IMAGE = "background.jpg"

INSTRUCTIONS_PATH = "res/instructions.txt"
MUSIC = "res/music.mp3"
