# Importere pg
import pygame as pg
import sys
import random
from sprites import *

# Initierer mixer
pg.mixer.init()

# Laster inn lyder
song = pg.mixer.Sound('printer_sang.mp3')
cue_sound = pg.mixer.Sound('cueSound.mp3')
pling_sound = pg.mixer.Sound('pling.mp3')
plop_sound = pg.mixer.Sound('plop.mp3')

# Spillobjekt
class Game():
    def __init__(self):
        # Initiere pg
        pg.init()

        # Lager en skjerm vi kan tegne på
        self.screen = pg.display.set_mode(SIZE)

        # Lager en klokke
        self.clock = pg.time.Clock()

        # Variabel som styrer om spillet skal kjøres
        self.running = True

    # Lager et nytt spill
    def new(self):
        Ball.nr = 0
        Ball.arr = []
        Wall.arr = []
        Hole.arr = []

        # Endrer seg når ballene stopper og starter å bevege seg
        self.motion = False

        # Antall baller hver spiller har igjen
        self.player1Balls = 7
        self.player2Balls = 7
        self.player1Balls_temp = self.player1Balls
        self.player2Balls_temp = self.player2Balls

        # Spiller 1 har "1", Spiller 2 har "-1"
        self.playerTurn = 1

        # Sjekker om svart ball har havnet i hullet
        self.black_ball_in_hole = False

        # Sjekker om hvit ball har havnet i hullet
        self.player_ball_in_holee = False

        # Legger ballene i tilfeldig rekkefølge unntatt hvit og svart
        black_ball = BALLVERDIER.pop(5)
        white_ball = BALLVERDIER.pop(0)
        random.shuffle(BALLVERDIER)
        BALLVERDIER.insert(0, white_ball)
        BALLVERDIER.insert(5, black_ball)

        # Lager spillerball
        self.ball1 = Ball(self.screen, F_A+LENGTH_P/4, F_A+WIDTH_P/2, RADIUS, 1)

        # Lager køen
        self.stick = Stick(game_object.screen)

        # Lager resten av ballene
        for i in range(5):
            for j in range(i+1):
                Ball(self.screen, F_A+LENGTH_P*(3/4) + i*DISTANCE*1.1, HEIGHT/2 + DIAMETER*j*1.1 - i*RADIUS, RADIUS, 1)

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

        # Starter spillet
        self.run()

    def run(self):
        # variabel som sjekker om spillet er i gang
        self.playing = True

        # Oppdaterer brettet
        while self.playing:
            self.update()

        # Viser endscreen hvis programmet kjører
        if self.running == True:
            self.endscreen()

    def events(self):
        # Går gjennom hendelser (events)
        events = pg.event.get()
        for event in events:
            # Sjekker om vi ønsker å lukke vinduet
            if event.type == pg.QUIT:
                # Spillet avsluttes
                self.playing = False
                self.running = False 
                self.end_screen_render = False

            # Avsgjør kraften til skuddet 
            if self.playing:
                if event.type == pg.MOUSEBUTTONUP:
                    # Passer på at den hvite ballen står stille
                    if self.momentum == 0:
                        cue_sound.play()
                        self.ball1.vel = Vector(-self.stick.b_vec.unit().mult((self.stick.movement-CUE_MOVEMENT_MIN)*POWER).x, -self.stick.b_vec.unit().mult((self.stick.movement-CUE_MOVEMENT_MIN)*POWER).y)


    def update(self):
        # Sørger for at løkken kjører i korrekt hastighet
        self.clock.tick(FPS)

        # Starter sangen på nytt om den er ferdig
        if not pg.mixer.get_busy() or pg.mixer.get_busy() == song:
            song.play()
            pass

        # Sjekker events
        self.events()
               
        # Fyller skjermen med en farge
        self.screen.fill(BACKGROUND)

        # Brettfarge
        pg.draw.rect(self.screen, BOARDCOLOR, (F_A, F_A, WIDTH-2*F_A, HEIGHT-2*F_A), 0)
        
        # Avgjør om køen skal tegnes
        if pg.mouse.get_pressed()[0]:
            # Passer på at den hvite ballen står stille
            if self.momentum == 0:
                self.stick.draw_stick(self.ball1)
        
        # Finner faktisk fps
        actual_fps = self.clock.get_fps()

        # Viser fps
        display_text(f"fps: {round(actual_fps)}", ORANGE, WIDTH/2, F_A/4, 15)

        # Ramme for køkraft
        pg.draw.rect(self.screen, BLACK, ((WIDTH/2)-(255/2), F_A/3, 255, 20), 1)

        # Viser hvem sin tur det er 
        if self.playerTurn == 1:
            display_text("PLAYER 1 : STRIPER", ORANGE, WIDTH/4, F_A/4, 14)
            display_text("PLAYER 2 : UTEN STRIPER", WHITE, WIDTH*(3/4), F_A/4, 14)
        else:
            display_text("PLAYER 1 : STRIPER", WHITE, WIDTH/4, F_A/4, 14)
            display_text("PLAYER 2 : UTEN STRIPER", ORANGE, WIDTH*(3/4), F_A/4, 14)
        
        # Tegner hull og registrerer ball i hull
        for index in range(len(Hole.arr)):
            Hole.arr[index].draw()
            for b in Ball.arr:
                if coll_det_bh(b, Hole.arr[index]):
                    plop_sound.play()
                    # Registrerer om det er spillerballen som har gått i hullet
                    b.vel = Vector(0, 0)
                    if b.values[1] == "":
                        self.player_ball_in_hole = True
                        b.pos = Vector(WIDTH/2, HEIGHT/2)

                    # Registrerer om det er den svarte ballen som har gått i hullet
                    elif b.values[1] == 8:
                        b.score_ball = True
                        if self.playerTurn == 1:
                            b.pos = Vector(WIDTH/3 - self.player1Balls * DIAMETER, F_A/2)
                        else:
                            b.pos = Vector(WIDTH*(3/4) - self.player2Balls * DIAMETER, F_A/2)

                        self.black_ball_in_hole = True

                    # Registrerer alle andre baller
                    else:
                        b.score_ball = True
                        # Registrerer poeng
                        if b.values[2] == 1:
                            b.pos = Vector(WIDTH/3 - self.player1Balls * DIAMETER, F_A/2)
                            self.player1Balls -= 1
                        elif b.values[2] == 0:
                            b.pos = Vector(WIDTH*(8.1/10) - self.player2Balls * DIAMETER, F_A/2)
                            self.player2Balls -= 1
        
        # Total fart til ballene
        self.momentum = 0

        # Registrerer kollisjon og beregner effekten av kollisjonen ved å iterere gjennom alle ballene
        for index in range(len(Ball.arr)):
            b = Ball.arr[index]
            # Legger til total fart til ballene
            self.momentum += b.vel.mag()
            b.draw()

            # Tegner balldetaljer
            if b.values[2] == 1:
                pg.draw.line(self.screen, WHITE, (b.pos.x-1, b.pos.y-RADIUS), (b.pos.x, b.pos.y + RADIUS*0.9), int(RADIUS/2))
            display_text(f"{b.values[1]}", BLACK, b.pos.x, b.pos.y, int(RADIUS*0.9), "circle", WHITE)
                
            # Registrerer krasj for én ball med de som ikke har blitt testet og responderer
            for j in range(index + 1, len(Ball.arr)):
                if coll_det_bb(b, Ball.arr[j]):
                    pen_res_bb(b, Ball.arr[j])
                    coll_res_bb(b, Ball.arr[j])
                    
            # Registrerer kollisjon mellom baller og vegger og responderer
            for w in Wall.arr:
                if coll_det_bw(b, w):
                    pen_res_bw(b, w)
                    coll_res_bw(b, w)
            
            # Flytter på ballene
            b.reposition()

        # Endres når ballene går fra bevegelse til stille
        if self.momentum > 0:
            self.motion = True

        # Runden er ferdig
        if self.momentum == 0 and self.motion == True:
            pling_sound.play()
            # Hvis spiller 1 sin tur
            if self.playerTurn == 1:
                if self.black_ball_in_hole:
                    # Taper pga svart ball
                    if self.player1Balls > 0:
                        self.playerTurn *= -1
                        self.playing = False
                    # Vinner med svart ball
                    if self.player1Balls == 0:
                        self.playing = False

                # Bytter tur
                elif self.player1Balls == self.player1Balls_temp or self.player2Balls != self.player2Balls_temp or self.player_ball_in_hole:
                    self.playerTurn *= -1
                
            # Hvis spiller 2 sin tur
            elif self.playerTurn == -1:
                if self.black_ball_in_hole:
                    # Taper pga svart ball
                    if self.player2Balls > 0:
                        self.playerTurn *= -1
                        self.playing = False
                    # Vinner med svart ball
                    if self.player2Balls == 0:
                        self.playing = False

                # Bytter tur
                elif self.player2Balls == self.player2Balls_temp or self.player1Balls != self.player1Balls_temp or self.player_ball_in_hole:
                    self.playerTurn *= -1

            self.player1Balls_temp = self.player1Balls
            self.player2Balls_temp = self.player2Balls

            self.player_ball_in_hole = False
            self.motion = False
            
        # Tegner veggene
        for index in range(len(Wall.arr)):
            w = Wall.arr[index]
            w.draw_wall()

        # "Flipper" displayet for å vise hva vi har tegnet
        pg.display.flip()

    def endscreen(self):
        self.end_screen_render = True

        # Loop for endscreen
        while self.end_screen_render:
            self.events()
            keys = pg.key.get_pressed()
            self.clock.tick(FPS)
            # Fyller skjermen med en farge
            self.screen.fill(GREEN)
            # Bruker playerTurn for å vise hvem som vant
            display_text(f"SPILLET ER OVER! SPILLER {int(-0.5*self.playerTurn+1.5)} VANT!", WHITE, WIDTH/2, HEIGHT/4, 20)
            display_text(f"TRYKK PÅ 'MELLOMROMTASTEN' FOR Å SPILLE PÅ NYTT", WHITE, WIDTH/2, HEIGHT/2+F_A, 20)

            if keys[pg.K_SPACE]:
                self.end_screen_render = False
                self.new()
        
            pg.display.flip()

game_object = Game()

# Finner punktet på en vegg som er nermest en ball
def closest_point_BW(b1Pos, w1):
    # Vektorer fra ball til start og slutt av veggen
    ball_to_wall_start = w1.start.subtr(b1Pos)
    wall_end_to_ball = b1Pos.subtr(w1.end)

    # Om vinkelen er mer enn 90° er nærmeste punkt start eller slutt
    if Vector.dot(w1.wall_unit(), ball_to_wall_start) > 0:
        return w1.start
    if Vector.dot(w1.wall_unit(), wall_end_to_ball) > 0:
        return w1.end
    
    # Finner lengden på vektoren fra starten av veggen til nærmeste punkt
    closest_dist = Vector.dot(w1.wall_unit(), ball_to_wall_start)

    # Lager vektor fra start av veggen til nærmeste punkt
    closest_vect = w1.wall_unit().mult(closest_dist)
    
    # Returnerer punktet
    return w1.start.subtr(closest_vect)

# Registerer kollisjon mellom to baller
def coll_det_bb(b1, b2):
    # Sjekker om radiusene addert med hverandre er 
    # større enn eller lik lengden på vektoren mellom dem
    if b1.r + b2.r >= b2.pos.subtr(b1.pos).mag():
        return True
    else:
        return False
    
# Registerer ball i hull
def coll_det_bh(b1, h1):
    # Sjekker om radiusen til hullet er større enn eller lik vektoren fra ball til hull
    if h1.r >= h1.pos.subtr(b1.pos).mag():
        return True
    else:
        return False
    
# Registerer kollisjon mellom ball og vegg
def coll_det_bw(b1, w1):
    # Vektor fra ball til nærmeste punkt på veggen
    ball_to_closest = closest_point_BW(b1.pos, w1).subtr(b1.pos)
    
    # Registrerer om enden av fartsvektoren er på forskjellig side av veggen enn ballen
    # Enden av fartsvektoren bestemmer ballens neste posisjon

    if b1.score_ball == False:
        if b1.pos.x < F_A-RADIUS/2:
            b1.pos.x += b1.r
        if b1.pos.x > F_A+LENGTH_P+RADIUS/2:
            b1.pos.x -= b1.r
        if b1.pos.y < F_A-RADIUS/2:
            b1.pos.y += b1.r
        if b1.pos.y > F_A+WIDTH_P+RADIUS/2:
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
def display_text(txt, txt_color, x, y, s, shape="none", background_color = WHITE):
    font = pg.font.Font('freesansbold.ttf', s)
    text = font.render(txt, True, txt_color)
    textRect = text.get_rect(center=(x, y))

    if shape == "rect":
        text = font.render(txt, True, txt_color, background_color)
    elif shape == 'circle':
        radius = textRect.height // 1.3
        pg.draw.circle(game_object.screen, background_color, textRect.center, radius)
    game_object.screen.blit(text, textRect)


# Spill-løkken
game_object.new()

# Avslutter pg
pg.quit()
sys.exit() # Dersom det ikke er tilstrekkelig med pg.quit()
