import math

# Størrelse på banen
POOL_SIZE = 4

# Størrelsen på ballene
RADIUS = 5.715/2 * POOL_SIZE
DIAMETER = RADIUS*2

# Distansen mellom ballene i startposisjon
DISTANCE = math.sqrt(DIAMETER**2 - RADIUS**2)

# LENGDE og BREDDE på banen
LENGTH_P = 224 * POOL_SIZE
WIDTH_P = 112 * POOL_SIZE

# Fritt område (free area)
F_A = 150

# Biljardmellomrom (pool_space)
P_S = DIAMETER*1.1
# Biljardmellomrom diagonal
P_S_D = (P_S**2+P_S**2)**0.5

# Kraft til pinnen
POWER = 0.25

HOLE_RADIUS = 25

FRICTION = 0.008    # Friksjon på banen

# LENGDE og BREDDE på vinduet
WIDTH = LENGTH_P + F_A*2
HEIGHT = WIDTH_P + F_A*2
SIZE = (WIDTH, HEIGHT)

# Frames Per Second (bilder per sekund)
FPS = 120

# Farger (RGB)
WHITE = (255, 255, 255)     # Køball
BEIGE = (230, 200, 170)     # Kø
BLACK = (0, 0, 0)           # 8 Ball
YELLOW = (255, 255, 0)      # 1 and 9 Ball
BLUE = (0, 0, 255)          # 2 and 10 Ball
RED = (255, 0, 0)           # 3 and 11 Ball
PURPLE = (128, 0, 128)      # 4 and 12 Ball
ORANGE = (255, 165, 0)      # 5 and 13 Ball
GREEN = (0, 128, 0)         # 6 and 14 Ball
BROWN = (165, 42, 42)       # 7 and 15 Ball
GRAYBLACK = (50, 50, 50)    # Kø støttelinje
DARKBLUE = (52, 152, 219)    # Brettfarge

BALLVERDIER = [
    [YELLOW, 1, 0],
    [BLUE, 2, 0],
    [RED, 3, 0],
    [PURPLE, 4, 0],
    [ORANGE, 5, 0],
    [GREEN, 6, 0],
    [BROWN, 7, 0],
    [BLACK, 8],
    [YELLOW, 9, 1],
    [BLUE, 10, 1],
    [RED, 11, 1],
    [PURPLE, 12, 1],
    [ORANGE, 13, 1],
    [GREEN, 14, 1],
    [BROWN, 15, 1]
]

