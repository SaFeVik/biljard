import math

# Størrelse på banen
pool_size = 4

# Størrelsen på ballene
radius = 5.715/2 * pool_size
diameter = radius*2

# Distansen mellom ballene i startposisjon
distanse = math.sqrt(diameter**2 - radius**2)

# Lengde og bredde på banen
lengde = 224 * pool_size
bredde = 112 * pool_size

# Fritt område (free area)
f_a = 150

# Kraft til pinnen
power = 0.25

hole_radius = 25    # Radius på hullene

friction = 0.008    # Friksjon på banen

# Lengde og bredde på vinduet
WIDTH = lengde + f_a*2
HEIGHT = bredde + f_a*2
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

ballverdier = [
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