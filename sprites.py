import pygame as pg
import math
from settings import *

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
    arr = []    # ballliste
    nr = 0      # holder styr på ballnr som legges til i listen

    def __init__(self, surface_object, x, y, r, m):
        self.surface_object = surface_object    # overflaten (surface)
        self.r = r                              # radius
        self.m = m                              # masse (brukes i testfasen)

        self.values = BALLVERDIER[Ball.nr]      # gir riktige ballverdier til ballen
        Ball.nr += 1

        # Omvendt masse (brukes i testfasen)
        if self.m == 0:
            self.inv_m = 0
        else:
            self.inv_m = 1/self.m

        self.elasticity = 0.7                   # elastisitet
        self.pos = Vector(x, y)                 # posisjonsvektor
        self.vel = Vector(0, 0)                 # fartsvektor
        self.farge = self.values[0]             # ballfarge

        # Brukes ballen til å vise score?
        self.score_ball = False
        
        # Legger til ballen i balls-listen
        self.arr.append(self)
            
    # Funksjon for å bevege ballen
    def draw(self):
        # Tegner ballen
        pg.draw.circle(self.surface_object, self.farge, (self.pos.x, self.pos.y), self.r)
        
    # Endrer akselerasjons-, farts- og posisjonsvektoren
    def reposition(self):
        # Stopper ballen om farten er under 0.02
        if self.vel.mag() < 0.02:
            self.vel = Vector(0, 0)
        else:
            self.vel = self.vel.mult(1-FRICTION)    # friksjon
        self.pos = self.pos.add(self.vel)           # posisjon

# Klasse for veggobjekter
class Wall():
    arr = []
    def __init__(self, surface_object, x1, y1, x2, y2):
        self.start = Vector(x1, y1)             # startposisjon
        self.end = Vector(x2, y2)               # sluttposisjon
        self.surface_object = surface_object    # overflaten (surface)
        # Legger til veggen i walls-listen
        self.arr.append(self)
        
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
    
    def draw_stick(self, b):
        # Museposisjonsvektor
        self.m_end = pg.mouse.get_pos()
        self.m_end = Vector(self.m_end[0], self.m_end[1])
        
        # Vektor fra mus til andre siden av ballen
        self.b_vec = self.m_end.subtr(b.pos)
        
        # Mengden forflytning
        self.movement = self.b_vec.mag()
        
        # Begrenser forflytningen og mulig kraft
        if self.movement > CUE_MOVEMENT_MAX:
            self.movement = CUE_MOVEMENT_MAX
        elif self.movement < CUE_MOVEMENT_MIN:
            self.movement = CUE_MOVEMENT_MIN
        '''
        forbedre
        '''
        # start- og sluttkoordinater for køen (biljardpinnen)
        start1 = (b.pos.x + self.b_vec.unit().mult(self.movement-CUE_BALL_DIST).x, b.pos.y + self.b_vec.unit().mult(self.movement-CUE_BALL_DIST).y)

        end1 = (b.pos.x + self.b_vec.unit().mult(self.movement+CUE_LENGTH/5).x, b.pos.y + self.b_vec.unit().mult(self.movement+CUE_LENGTH/5).y)

        start2 = (b.pos.x + self.b_vec.unit().mult(self.movement+CUE_LENGTH/5).x, b.pos.y + self.b_vec.unit().mult(self.movement+CUE_LENGTH/5).y)
        end2 = (b.pos.x + self.b_vec.unit().mult(self.movement+CUE_LENGTH).x, b.pos.y + self.b_vec.unit().mult(self.movement+CUE_LENGTH).y)

        startLine = (b.pos.x - self.b_vec.unit().mult(20).x, b.pos.y - self.b_vec.unit().mult(20).y)
        endLine = (b.pos.x - self.b_vec.unit().mult(WIDTH).x, b.pos.y - self.b_vec.unit().mult(WIDTH).y)
        
        # Tegner køen
        pg.draw.line(self.surface_object, BEIGE, start1, end1, CUE_LENGTH//25)
        pg.draw.line(self.surface_object, BLACK, start2, end2, CUE_LENGTH//25)
        pg.draw.line(self.surface_object, GRAYBLACK, startLine, endLine)
        
        # Konverterer movementverdien til et tall [0, 255]
        self.power = 255*((self.movement-CUE_MOVEMENT_MIN)/(CUE_MOVEMENT_MAX-CUE_MOVEMENT_MIN))

        # Viser kraft
        pg.draw.rect(self.surface_object, (self.power, 255-self.power, 0), ((WIDTH/2)-(255/2), F_A/3, self.power, 20))

class Hole():
    arr = []
    def __init__(self, surface, x, y, r):
        self.surface_object = surface
        self.pos = Vector(x, y)
        self.r = r
        self.arr.append(self)
        
    def draw_hole(self):
        pg.draw.circle(self.surface_object, BLACK, (self.pos.x, self.pos.y), self.r)

