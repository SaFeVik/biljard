# Importere pg
import pygame as pg
import sys
from sprites import *

class Game():
    def __init__(self):
        # Initiere pg
        pg.init()

        # Lager en skjerm vi kan tegne på
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()
        print(type(7))
        # Variabel som styrer om spillet skal kjøres
        self.running = True

        self.fps = FPS

        self.player1Balls = 7
        self.player2Balls = 7
        self.playerTurn = 1

    def new(self):
        self.ball1 = Ball(self.screen, F_A+LENGTH_P/4, F_A+WIDTH_P/2, RADIUS, 1, RED)
        self.ball1.player = True

        self.stick = Stick(game_object.screen)

        for i in range(5):
            for j in range(i+1):
                ball = Ball(self.screen, F_A+LENGTH_P*(3/4) + i*DISTANCE, HEIGHT/2 + DIAMETER*j - i*RADIUS, RADIUS, 1, BALLVERDIER[i+j][0])

        # Vegger
        # Oppe venstre
        Wall(self.screen, F_A+P_S_D, F_A, F_A+LENGTH_P/2-P_S, F_A)
        # Oppe høyre
        Wall(self.screen, F_A+LENGTH_P/2+P_S, F_A, F_A+LENGTH_P-P_S_D, F_A)
        # Høyre
        Wall(self.screen, F_A+LENGTH_P, F_A+P_S_D, F_A+LENGTH_P, F_A+WIDTH_P-P_S_D)
        # Nede høyre
        Wall(self.screen, F_A+LENGTH_P-P_S_D, F_A+WIDTH_P, F_A+LENGTH_P/2+P_S, F_A+WIDTH_P)
        # Nede venstre
        Wall(self.screen, F_A+LENGTH_P/2-P_S, F_A+WIDTH_P, F_A+P_S_D, F_A+WIDTH_P)
        # Venstre
        Wall(self.screen, F_A, F_A+WIDTH_P-P_S_D, F_A, F_A+P_S_D)

        # Hull med sine vegger (fra øverst til venstre med klokka)
        # Hull 1
        Wall(self.screen, F_A+P_S_D, F_A, F_A-HOLE_RADIUS+P_S_D, F_A-HOLE_RADIUS)
        Wall(self.screen, F_A, F_A+P_S_D, F_A-HOLE_RADIUS, F_A-HOLE_RADIUS+P_S_D)
        Hole(self.screen, F_A - HOLE_RADIUS*(2**0.5)/10, F_A - HOLE_RADIUS*(2**0.5)/10, HOLE_RADIUS)

        # Hull 2
        Wall(self.screen, F_A+LENGTH_P/2-P_S, F_A, F_A+LENGTH_P/2-P_S/2, F_A-P_S)
        Wall(self.screen, F_A+LENGTH_P/2+P_S, F_A, F_A+LENGTH_P/2+P_S/2, F_A-P_S)
        Hole(self.screen, F_A+LENGTH_P/2, F_A-HOLE_RADIUS, HOLE_RADIUS)

        # Hull 3
        Wall(self.screen, F_A+LENGTH_P-P_S_D, F_A, F_A+LENGTH_P+HOLE_RADIUS-P_S_D, F_A-HOLE_RADIUS)
        Wall(self.screen, F_A+LENGTH_P, F_A+P_S_D, F_A+LENGTH_P+HOLE_RADIUS, F_A-HOLE_RADIUS+P_S_D)
        Hole(self.screen, F_A+LENGTH_P + HOLE_RADIUS*(2**0.5)/10, F_A - HOLE_RADIUS*(2**0.5)/10, HOLE_RADIUS)

        # Hull 4
        Wall(self.screen, F_A+LENGTH_P, F_A+WIDTH_P-P_S_D, F_A+LENGTH_P+HOLE_RADIUS, F_A+WIDTH_P+HOLE_RADIUS-P_S_D)
        Wall(self.screen, F_A+LENGTH_P-P_S_D, F_A+WIDTH_P, F_A+LENGTH_P+HOLE_RADIUS-P_S_D, F_A+WIDTH_P+HOLE_RADIUS)
        Hole(self.screen, F_A+LENGTH_P + HOLE_RADIUS*(2**0.5)/10, F_A+WIDTH_P + HOLE_RADIUS*(2**0.5)/10, HOLE_RADIUS)

        # Hull 5
        Wall(self.screen, F_A+LENGTH_P/2-P_S, F_A+WIDTH_P, F_A+LENGTH_P/2-P_S/2, F_A+WIDTH_P+P_S)
        Wall(self.screen, F_A+LENGTH_P/2+P_S, F_A+WIDTH_P, F_A+LENGTH_P/2+P_S/2, F_A+WIDTH_P+P_S)
        Hole(self.screen, F_A+LENGTH_P/2, F_A+WIDTH_P + HOLE_RADIUS, HOLE_RADIUS)

        # Hull 6
        Wall(self.screen, F_A+P_S_D, F_A+WIDTH_P, F_A-HOLE_RADIUS+P_S_D, F_A+WIDTH_P+HOLE_RADIUS)
        Wall(self.screen, F_A, F_A+WIDTH_P-P_S_D, F_A-HOLE_RADIUS, F_A+WIDTH_P+HOLE_RADIUS-P_S_D)
        Hole(self.screen, F_A - HOLE_RADIUS*(2**0.5)/10, F_A+WIDTH_P + HOLE_RADIUS*(2**0.5)/10, HOLE_RADIUS)

        self.run()

    def run(self):
        self.playing = True

        while self.playing:
            self.update()

    def update(self):
        # Sørger for at løkken kjører i korrekt hastighet
        self.clock.tick(self.fps)

        # Går gjennom hendelser (events)
        events = pg.event.get()
        
        for event in events:
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                print("quit")
                # Spillet avsluttes
                self.playing = False
                self.running = False 

                    
            # Enrer FPS om man trykker på g eller h (brukes i testfasen)
            keys = pg.key.get_pressed()
            if keys[pg.K_g]:
                self.fps = 1
            if keys[pg.K_h]:
                self.fps = 120

            # Avsgjør kraften til skuddet                    
            if event.type == pg.MOUSEBUTTONUP:
                self.ball1.vel = Vector(-self.stick.b_vec.unit().mult(self.stick.movement*POWER-60*POWER).x, -self.stick.b_vec.unit().mult(self.stick.movement*POWER-60*POWER).y)
               
        # Fyller skjermen med en farge
        self.screen.fill(DARKBLUE)

        # Avgjør om køen skal tegnes
        if pg.mouse.get_pressed()[0]:
            self.stick.draw_stick(self.ball1)
        
        # Viser faktisk fps
        actual_fps = self.clock.get_fps()
        display_text(f"fps: {round(actual_fps)}", RED, WHITE, WIDTH/2, F_A/4, 15)

        pg.draw.rect(self.screen, BLACK, ((WIDTH/2)-(255/2), F_A/2+20, 255, 20), 1)

        display_text("PLAYER 1 : STRIPER", BLACK, WHITE, WIDTH/4, F_A/2, 14)
        display_text("PLAYER 2 : UTEN STRIPER", BLACK, WHITE, WIDTH*(3/4), F_A/2, 14)

        if self.playerTurn == 1:
            display_text("TURN : PLAYER 1", BLACK, WHITE, WIDTH/2, F_A/2, 14)
        else:
            display_text("TURN : PLAYER 2", BLACK, WHITE, WIDTH/2, F_A/2, 14)
        
        # Tegner hull og registrerer ball i hull
        for index in range(len(Hole.liste)):
            Hole.liste[index].draw_hole()
            for b in Ball.liste:
                if coll_det_bh(b, Hole.liste[index]):

                    print(f"ball i hull")
                    b.pos = Vector(WIDTH/2, HEIGHT/2)

                    b.farge = BLACK
        
        # Registrerer kollisjon og beregner effekten av kollisjonen ved å iterere gjennom alle ballene
        for index in range(len(Ball.liste)):
            b = Ball.liste[index]
            b.draw()
            
            # Beveger spillerballen (brukes i testfasen)
            if b.player:
                key_controll(b)
                
            # Registrerer krasj for én ball med de som ikke har blitt testet og responderer
            for j in range(index + 1, len(Ball.liste)):
                if coll_det_bb(b, Ball.liste[j]):
                    pen_res_bb(b, Ball.liste[j])
                    coll_res_bb(b, Ball.liste[j])
                    
            # Registrerer kollisjon mellom baller og vegger og responderer
            for w in Wall.liste:
                if coll_det_bw(b, w):
                    pen_res_bw(b, w)
                    coll_res_bw(b, w)
                    
            # Viser farts- og akselerasjonsvektorer til ballene
            b.display()
            
            # Flytter på ballene
            b.reposition()

            
        # Tegner veggene
        for index in range(len(Wall.liste)):
            w = Wall.liste[index]
            w.draw_wall()

        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()



game_object = Game()

# Styring av baller (brukes i testfasen)
def key_controll(b):
    right, left, up, down = False, False, False, False
    key = pg.key.get_pressed()
    # Sjekker om tast blir trykket
    if key[pg.K_RIGHT]:
        right = True
    if key[pg.K_LEFT]:
        left = True
    if key[pg.K_UP]:
        up = True
    if key[pg.K_DOWN]:
        down = True
            
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
    
    if b1.pos.x < F_A:
        b1.pos.x += b1.r
    if b1.pos.x > F_A+LENGTH_P:
        b1.pos.x -= b1.r
    if b1.pos.y < F_A:
        b1.pos.y += b1.r
    if b1.pos.y > F_A+WIDTH_P:
        b1.pos.y -= b1.r
        
    # Registrerer kollisjon
    if ball_to_closest.mag() <= b1.r:
        return True
    
# Beregner gjennomtrengningsoppløsning mellom to baller og reposisjonerer
def pen_res_bb(b1, b2):
    # DISTANCEn mellom ball1 og ball2
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
    game_object.screen.blit(text, textRect)

# Spill-løkken
while game_object.running:
    # Starter et nytt spill
    game_object.new()
print("QUITTED")

# Avslutter pg
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()
