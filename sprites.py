import math
import pygame as pg
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
    liste = []

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
        self.liste.append(self)
            
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
    liste = []
    def __init__(self, surface_object, x1, y1, x2, y2):
        self.start = Vector(x1, y1)             # startposisjon
        self.end = Vector(x2, y2)               # sluttposisjon
        self.surface_object = surface_object    # overflaten (surface)
        # Legger til veggen i walls-listen
        self.liste.append(self)
        
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
        if self.movement > 150:
            self.movement = 150
        elif self.movement < 60:
            self.movement = 60
        '''
        forbedre
        '''
        # start- og sluttkoordinater for køen (biljardpinnen)
        start1 = (b.pos.x + self.b_vec.unit().mult(self.movement-30).x, b.pos.y + self.b_vec.unit().mult(self.movement-30).y)
        end1 = (b.pos.x + self.b_vec.unit().mult(self.movement+30).x, b.pos.y + self.b_vec.unit().mult(self.movement+30).y)

        start2 = (b.pos.x + self.b_vec.unit().mult(self.movement+30).x, b.pos.y + self.b_vec.unit().mult(self.movement+30).y)
        end2 = (b.pos.x + self.b_vec.unit().mult(self.movement+150).x, b.pos.y + self.b_vec.unit().mult(self.movement+150).y)
        
        # Tegner køen
        pg.draw.line(self.surface_object, BEIGE, start1, end1, 6)
        pg.draw.line(self.surface_object, BLACK, start2, end2, 6)
        
        pg.draw.line(self.surface_object, BLACK, start2, end2, 6)
        
        # Konverterer movementverdien til et tall [0, 255]
        power = (self.movement-60)*(255/90)

        # Viser kraft
        pg.draw.rect(self.surface_object, (power, 255-power, 0), ((WIDTH/2)-(255/2), f_a/2+20, power, 20))

class Hole():
    liste = []
    def __init__(self, surface, x, y, r):
        self.surface_object = surface
        self.pos = Vector(x, y)
        self.r = r
        self.liste.append(self)
        
    def draw_hole(self):
        pg.draw.circle(self.surface_object, BLACK, (self.pos.x, self.pos.y), self.r)