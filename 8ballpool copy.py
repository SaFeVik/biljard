# Importere pg
import pygame as pg
import sys
import math
import random

'''
# forbedre
# + = skriv kommentar
# (brukes i testfasen) = tas bort før levering

1. Spør om der det står "forbedre"
2. Spør om self.surface_object
3. Spør om objekt for stick, bruke klasse?
4. Spør om det er bedre å gjøre regnestykker eller å ha tallene fra før av
'''

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

# Lister for ballene, veggene og hullene
balls = []
walls = []
holes = []

# Initiere pg
pg.init()

# Lager en overflate (surface) vi kan tegne på
surface = pg.display.set_mode(SIZE)

# Lager en klokke
clock = pg.time.Clock()

# Variabel som styrer om spillet skal kjøres
run = True


friction = 0.008    # Friksjon på banen

# Variabler som holder styr på tastetrykk (brukes i testfasen)
right, left, up, down = False, False, False, False

# Klasse for vektorobjekter
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # Addisjon av vektorer
    def add(self, v):
        return Vector(self.x+v.x, self.y+v.y)
    
    # Subtraksjon av vektorer
    def subtr(self, v):
        return Vector(self.x-v.x, self.y-v.y)
    
    # Lengde til vektorer
    def mag(self):
        return math.sqrt(self.x**2 + self.y**2)
    
    # Multiplikasjon av vektorer
    def mult(self, n):
        return Vector(self.x*n, self.y*n)
    
    # Normal til vektorer
    def normal(self):
        return Vector(-self.y, self.x).unit()
    
    # Enhetsvektor til vektorer
    def unit(self):
        if self.mag() == 0:
            return Vector(0, 0)
        else:
            return Vector(self.x/self.mag(), self.y/self.mag())
    
    # Skalarprodukt mellom to vektorer
    def dot(v1, v2):
        return v1.x*v2.x + v1.y*v2.y
    
    # Tegning av vektorer
    def draw_vec(self, surface_object, x, y, n, color):
        pg.draw.line(surface_object, color, [x, y], [x+self.x*n, y+self.y*n], 2)

# Klasse for ballobjekter
class Ball():
    def __init__(self, surface_object, x, y, r, m, farge):
        self.surface_object = surface_object    # overflaten (surface)
        self.r = r                              # radius
        self.m = m                              # masse
        
        # Omvendt masse
        if self.m == 0:
            self.inv_m = 0
        else:
            self.inv_m = 1/self.m
        self.elasticity = 0.7                   # elastisitet
        self.pos = Vector(x, y)                 # posisjonsvektor
        self.vel = Vector(0, 0)                 # fartsvektor
        self.acc = Vector(0, 0)                 # akselerasjonsvektor (brukes i testfasen)
        self.a = 0.05                           # akselerasjon (brukes i testfasen)
        self.farge = farge                      # ballfarge
        self.player = False                     # kan ballen styres? (Brukes i testfasen)
        
        # Legger til ballen i balls-listen
        balls.append(self)
            
    # Funksjon for å bevege ballen
    def draw(self):
        # Tegner ballen
        pg.draw.circle(self.surface_object, self.farge, (self.pos.x, self.pos.y), self.r)

    def display(self):
        # Tegner farts- og akselerasjonsvektor om lengden er under 0,01 (brukes i testfasen)
        if self.vel.mag() > 0.01:
            self.vel.draw_vec(self.surface_object, self.pos.x, self.pos.y, 1, (0, 200, 0))
        if self.acc.mag() > 0.01:
            self.acc.unit().draw_vec(self.surface_object, self.pos.x, self.pos.y, 1, (0, 0, 200))
            
        # Viser masse og elastisitet (brukes i testfasen)
        '''
        display_text(f"m: {self.m}", BLACK, self.farge, self.pos.x, self.pos.y-self.r*0.2, round(self.r*0.35))
        display_text(f"e: {self.elasticity}", BLACK, self.farge, self.pos.x, self.pos.y+self.r*0.2, round(self.r*0.35))
        '''
        
        
    # Endrer akselerasjons-, farts- og posisjonsvektoren
    def reposition(self):
        self.acc = self.acc.unit().mult(self.a)     # akselerasjon
        self.vel = self.vel.add(self.acc)           # fart
        self.vel = self.vel.mult(1-friction)        # friksjon
        self.pos = self.pos.add(self.vel)           # posisjon

# Klasse for veggobjekter
class Wall():
    def __init__(self, surface_object, x1, y1, x2, y2):
        self.start = Vector(x1, y1)             # startposisjon
        self.end = Vector(x2, y2)               # sluttposisjon
        self.surface_object = surface_object    # overflaten (surface)
        # Legger til veggen i walls-listen
        walls.append(self)
        
    # Tegner veggen
    def draw_wall(self):
        pg.draw.line(self.surface_object, BLACK, (self.start.x, self.start.y), (self.end.x, self.end.y), 1)
        
    # Enhetsvektor av veggen
    def wall_unit(self):
        return self.end.subtr(self.start).unit()

# Klasse for pinneobjekter
class Stick():
    def __init__(self, surface_object):
        self.surface_object = surface_object    # overflaten (surface)
    
    def draw_stick(self):
        # Museposisjonsvektor
        self.m_end = pg.mouse.get_pos()
        self.m_end = Vector(self.m_end[0], self.m_end[1])
        
        # Vektor fra mus til andre siden av ballen
        self.b_vec = self.m_end.subtr(ball1.pos)
        
        # Mengden forflytning
        self.movement = self.b_vec.mag()
        
        # Begrenser forflytningen og mulig kraft
        if self.movement > 150:
            self.movement = 150
        elif self.movement < 60:
            self.movement = 60
        '''
        forbedre
        '''
        # start- og sluttkoordinater for køen (biljardpinnen)
        start1 = (ball1.pos.x + self.b_vec.unit().mult(self.movement-30).x, ball1.pos.y + self.b_vec.unit().mult(self.movement-30).y)
        end1 = (ball1.pos.x + self.b_vec.unit().mult(self.movement+30).x, ball1.pos.y + self.b_vec.unit().mult(self.movement+30).y)

        start2 = (ball1.pos.x + self.b_vec.unit().mult(self.movement+30).x, ball1.pos.y + self.b_vec.unit().mult(self.movement+30).y)
        end2 = (ball1.pos.x + self.b_vec.unit().mult(self.movement+150).x, ball1.pos.y + self.b_vec.unit().mult(self.movement+150).y)
        
        # Tegner køen
        pg.draw.line(self.surface_object, BEIGE, start1, end1, 6)
        pg.draw.line(self.surface_object, BLACK, start2, end2, 6)
        
        pg.draw.line(self.surface_object, BLACK, start2, end2, 6)
        
        # Konverterer movementverdien til et tall [0, 255]
        power = (self.movement-60)*(255/90)

        # Viser kraft
        pg.draw.rect(self.surface_object, (power, 255-power, 0), ((WIDTH/2)-(255/2), f_a/2+20, power, 20))

class Hole():
    def __init__(self, surface, x, y, r):
        self.surface_object = surface
        self.pos = Vector(x, y)
        self.r = r
        holes.append(self)
        
    def draw_hole(self):
        pg.draw.circle(self.surface_object, BLACK, (self.pos.x, self.pos.y), self.r)

# Funksjon som avgjør skuddet
def stick_move():
    global clicked
    global stick
    for event in events:
        # Sjekker om musen er trykket
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                clicked = True
                stick = Stick(surface)
                
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                clicked = False

                ball1.vel = Vector(-stick.b_vec.unit().mult(stick.movement*power-60*power).x, -stick.b_vec.unit().mult(stick.movement*power-60*power).y)

    if clicked:
        stick.draw_stick()

# Styring av baller (brukes i testfasen)
def key_controll(b):
    global right, left, up, down
    for event in events:
    # Sjekker om tast blir trykket
        if event.type == pg.KEYDOWN:
            key = pg.key.name(event.key)
            if key == "right":
                right = True
            if key == "left":
                left = True
            if key == "up":
                up = True
            if key == "down":
                down = True
                
        # Sjekker om tast blir sluppet
        if event.type == pg.KEYUP:
            key = pg.key.name(event.key)
            if key == "right":
                right = False
            if key == "left":
                left = False
            if key == "up":
                up = False
            if key == "down":
                down = False
            
    # Oppdaterer farten fra konrollere
    if right:
        b.acc.x = b.a
    if left:
        b.acc.x = -b.a      
    if up:
        b.acc.y = -b.a
    if down:
        b.acc.y = b.a
        
    if right == False and left == False:
        b.acc.x = 0
    if up == False and down == False:
        b.acc.y = 0

# Finner punktet på en vegg som er nermest en ball
def closest_point_BW(b1Pos, w1):
    ball_to_wall_start = w1.start.subtr(b1Pos)
    if Vector.dot(w1.wall_unit(), ball_to_wall_start) > 0:
        return w1.start
    
    wall_end_to_ball = b1Pos.subtr(w1.end)
    if Vector.dot(w1.wall_unit(), wall_end_to_ball) > 0:
        return w1.end
    
    closest_dist = Vector.dot(w1.wall_unit(), ball_to_wall_start)
    closest_vect = w1.wall_unit().mult(closest_dist)
    return w1.start.subtr(closest_vect)

# Registerer kollisjon mellom to baller
def coll_det_bb(b1, b2):
    if b1.r + b2.r >= b2.pos.subtr(b1.pos).mag():
        return True
    else:
        return False
    
# Registerer ball i hull
def coll_det_bh(b1, h1):
    if h1.r >= h1.pos.subtr(b1.pos).mag():
        return True
    else:
        return False
    
# Registerer kollisjon mellom ball og vegg
def coll_det_bw(b1, w1):
    # Vektor fra ball til nærmeste punkt på veggen
    ball_to_closest = closest_point_BW(b1.pos, w1).subtr(b1.pos)
     
    # Punkt på enden av fartsvektoren
    vel_end = b1.pos.add(b1.vel)
    
    # Vektor fra enden av fartsvektor til nærmeste punkt på veggen
    vel_to_closest = closest_point_BW(vel_end, w1).subtr(vel_end)
    
    # Registrerer om enden av fartsvektoren er på forskjellig side av veggen enn ballen
    # Enden av fartsvektoren bestemmer ballens neste posisjon
    '''
    forbedre ?
    '''
    
    if b1.pos.x < f_a:
        b1.pos.x += b1.r
    if b1.pos.x > f_a+lengde:
        b1.pos.x -= b1.r
    if b1.pos.y < f_a:
        b1.pos.y += b1.r
    if b1.pos.y > f_a+bredde:
        b1.pos.y -= b1.r
        
    # Registrerer kollisjon
    if ball_to_closest.mag() <= b1.r:
        return True
    
# Beregner gjennomtrengningsoppløsning mellom to baller og reposisjonerer
def pen_res_bb(b1, b2):
    # Distansen mellom ball1 og ball2
    dist = b1.pos.subtr(b2.pos)
    
    # Hvor langt ballene overlapper hverandre
    pen_depth = b1.r + b2.r - dist.mag()
    
    # Hvor mye ballene blir dyttet tilbake (avhenger av massen)
    pen_res = dist.unit().mult(pen_depth / (b1.inv_m + b2.inv_m))
    
    # Blir dyttet tilbake avhengig av massen
    b1.pos = b1.pos.add(pen_res.mult(b1.inv_m))
    b2.pos = b2.pos.add(pen_res.mult(-b2.inv_m))
    
# Beregner gjennomtrengningsoppløsning mellom ball og vegg og reposisjonerer
def pen_res_bw(b1, w1):
    # Vektor fra nærmeste punkt på veggen, til ballen
    pen_vect = b1.pos.subtr(closest_point_BW(b1.pos, w1))
    
    # Ballen blir dyttet tilbake avhengig av hvor mye den overlapper
    b1.pos = b1.pos.add(pen_vect.unit().mult(b1.r - pen_vect.mag()))
'''
# +
Kommenter ballkollisjon og ball- og veggkollisjon
'''
# Kollisjonsrespons mellom to baller
def coll_res_bb(b1, b2):
    normal = b1.pos.subtr(b2.pos).unit()
    rel_vel = b1.vel.subtr(b2.vel)
    sep_vel = Vector.dot(rel_vel, normal)
    new_sep_vel = -sep_vel * min(b1.elasticity, b2.elasticity)
    
    vsep_diff = new_sep_vel - sep_vel
    impulse = vsep_diff / (b1.inv_m + b2.inv_m)
    impulse_vec = normal.mult(impulse)
    
    b1.vel = b1.vel.add(impulse_vec.mult(b1.inv_m))
    b2.vel = b2.vel.add(impulse_vec.mult(-b2.inv_m))

# Kollisjonsrespons mellom vegg og ball
def coll_res_bw(b1, w1):
    normal = b1.pos.subtr(closest_point_BW(b1.pos, w1)).unit()
    sep_vel = Vector.dot(b1.vel, normal)
    new_sep_vel = -sep_vel * b1.elasticity
    vsep_diff = sep_vel - new_sep_vel
    b1.vel = b1.vel.add(normal.mult(-vsep_diff))

# Viser tekst på skjermen
def display_text(txt, txt_color, rect_color, x, y, s):
    font = pg.font.Font('freesansbold.ttf', s)
    text = font.render(txt, True, txt_color, rect_color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    surface.blit(text, textRect)

# Variabel som sier om man trykker
clicked = False

# Pinnen og kraften til den
stick = 0
power = 0.25

# Lager baller og vegger
ball1 = Ball(surface, f_a+lengde/4, f_a+bredde/2, radius, 1, RED)

# Biljardmellomrom (pool_space)
p_s = diameter*1.1
# Biljardmellomrom diagonal
p_s_d = (p_s**2+p_s**2)**0.5


wall1_1 = Wall(surface, f_a+p_s_d, f_a, f_a+lengde/2-p_s, f_a)
wall1_2 = Wall(surface, f_a+lengde/2+p_s, f_a, f_a+lengde-p_s_d, f_a)

wall2 = Wall(surface, f_a+lengde, f_a+p_s_d, f_a+lengde, f_a+bredde-p_s_d)

wall3_1 = Wall(surface, f_a+lengde-p_s_d, f_a+bredde, f_a+lengde/2+p_s, f_a+bredde)
wall3_2 = Wall(surface, f_a+lengde/2-p_s, f_a+bredde, f_a+p_s_d, f_a+bredde)

wall4 = Wall(surface, f_a, f_a+bredde-p_s_d, f_a, f_a+p_s_d)

hole_radius = 25
hole_wall1_1 = Wall(surface, f_a+p_s_d, f_a, f_a-hole_radius+p_s_d, f_a-hole_radius)
hole_wall1_2 = Wall(surface, f_a, f_a+p_s_d, f_a-hole_radius, f_a-hole_radius+p_s_d)

hole_wall2_1 = Wall(surface, f_a+lengde/2-p_s, f_a, f_a+lengde/2-p_s/2, f_a-p_s)
hole_wall2_2 = Wall(surface, f_a+lengde/2+p_s, f_a, f_a+lengde/2+p_s/2, f_a-p_s)

hole_wall3_1 = Wall(surface, f_a+lengde-p_s_d, f_a, f_a+lengde+hole_radius-p_s_d, f_a-hole_radius)
hole_wall3_2 = Wall(surface, f_a+lengde, f_a+p_s_d, f_a+lengde+hole_radius, f_a-hole_radius+p_s_d)

hole_wall4_1 = Wall(surface, f_a+lengde, f_a+bredde-p_s_d, f_a+lengde+hole_radius, f_a+bredde+hole_radius-p_s_d)
hole_wall4_2 = Wall(surface, f_a+lengde-p_s_d, f_a+bredde, f_a+lengde+hole_radius-p_s_d, f_a+bredde+hole_radius)

hole_wall5_1 = Wall(surface, f_a+lengde/2-p_s, f_a+bredde, f_a+lengde/2-p_s/2, f_a+bredde+p_s)
hole_wall5_2 = Wall(surface, f_a+lengde/2+p_s, f_a+bredde, f_a+lengde/2+p_s/2, f_a+bredde+p_s)

hole_wall6_2 = Wall(surface, f_a+p_s_d, f_a+bredde, f_a-hole_radius+p_s_d, f_a+bredde+hole_radius)
hole_wall6_1 = Wall(surface, f_a, f_a+bredde-p_s_d, f_a-hole_radius, f_a+bredde+hole_radius-p_s_d)


'''
forbedre
'''
hole1 = Hole(surface, f_a - hole_radius*(2**0.5)/10, f_a - hole_radius*(2**0.5)/10, hole_radius)

hole2 = Hole(surface, f_a+lengde/2, f_a-hole_radius, hole_radius)

hole3 = Hole(surface, f_a+lengde + hole_radius*(2**0.5)/10, f_a - hole_radius*(2**0.5)/10, hole_radius)


hole4 = Hole(surface, f_a+lengde + hole_radius*(2**0.5)/10, f_a+bredde + hole_radius*(2**0.5)/10, hole_radius)

hole5 = Hole(surface, f_a+lengde/2, f_a+bredde + hole_radius, hole_radius)

hole6 = Hole(surface, f_a - hole_radius*(2**0.5)/10, f_a+bredde + hole_radius*(2**0.5)/10, hole_radius)

for i in range(5):
    for j in range(i+1):
        ball = Ball(surface, f_a+lengde*(3/4) + i*distanse, HEIGHT/2 + diameter*j - i*radius, radius, 1, ballverdier[i+j][0])

# Ball1 kan styres (brukes i testfasen)
ball1.player = True

# Spill-løkken
while run:
    # Sørger for at løkken kjører i korrekt hastighet
    clock.tick(FPS)

    # Går gjennom hendelser (events)
    events = pg.event.get()
    for event in events:
        # Sjekker om vi ønsker å lukke vinduet
        if event.type == pg.QUIT:
            # Spillet avsluttes
            run = False 
                
        # Enrer FPS om man trykker på g eller h (brukes i testfasen)
        keys = pg.key.get_pressed()
        if keys[pg.K_g]:
            FPS = 1
        if keys[pg.K_h]:
            FPS = 120
        
        
    # Fyller skjermen med en farge
    surface.fill(WHITE)
    
    # Viser faktisk fps
    actual_fps = clock.get_fps()
    display_text(f"fps: {round(actual_fps)}", RED, WHITE, WIDTH/2, f_a/2, 15)
    
    # Beveger køen
    stick_move()
    pg.draw.rect(surface, BLACK, ((WIDTH/2)-(255/2), f_a/2+20, 255, 20), 1)
    
    # Tegner hull og registrerer ball i hull
    for index in range(len(holes)):
        holes[index].draw_hole()
        for b in balls:
            if coll_det_bh(b, holes[index]):
                print(f"ball i hull")
                b.pos = Vector(WIDTH/2, HEIGHT/2)
                b.farge = BLACK
    
    # Registrerer kollisjon og beregner effekten av kollisjonen ved å iterere gjennom alle ballene
    for index in range(len(balls)):
        b = balls[index]
        b.draw()
        
        # Beveger spillerballen (brukes i testfasen)
        if b.player:
            key_controll(b)
            
        # Registrerer krasj for én ball med de som ikke har blitt testet og responderer
        for j in range(index + 1, len(balls)):
            if coll_det_bb(b, balls[j]):
                pen_res_bb(b, balls[j])
                coll_res_bb(b, balls[j])
                
        # Registrerer kollisjon mellom baller og vegger og responderer
        for w in walls:
            if coll_det_bw(b, w):
                pen_res_bw(b, w)
                coll_res_bw(b, w)
                
        # Viser farts- og akselerasjonsvektorer til ballene
        b.display()
        
        # Flytter på ballene
        b.reposition()

        
    # Tegner veggene
    for index in range(len(walls)):
        w = walls[index]
        w.draw_wall()

    # "Flipper" displayet for å vise hva vi har tegnet
    pg.display.flip()

# Avslutter pg
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()

