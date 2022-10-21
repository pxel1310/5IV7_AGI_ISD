# -------- Desarrolladores --------
# Astudillo Perez Edwin Uriel
# Ayala Gonzalez Ian
# Linares Medina Fernando Agustín

from re import S
import pygame
import math
import random
import socket
import threading
import sys

def receive(socket, signal):
    while signal:
        try:
            data = socket.recv(32)
        except:
            print("Fuis desconectado")
            signal = False
            break



arc= open("env.txt", "r")
host = arc.read()
arc.close()

acr = open("envpuerto.txt", "r")
port = int(acr.read())
acr.close()

cra = open("user.txt", "r")
user = cra.read()
cra.close()

titleSer= f"{host}:{port} - {user}"


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
except:
    print("Could not make a connection to the server")
    input("Press enter to quit")
    sys.exit(0)

receiveThread = threading.Thread(target = receive, args = (sock, True))
receiveThread.start()

while True:

    pygame.init()

    # Resolución
    largoP = 1280
    anchoP = 720

    # Ventana
    pygame.display.set_caption(f'Asteroides JIJIJAJA - {titleSer}')
    victoria = pygame.display.set_mode((largoP, anchoP))

    clock = pygame.time.Clock()

    # Valores del Juego
    finJIJIJAJA = False
    vidas = 3
    puntuacion = 0
    disparoGOD = False
    mayorPuntuacion = 0
    isSoundOn = True
    # Temporizador por partida
    


    # Importaciones
    fondo = pygame.image.load('src/fondo.png')
    nave = pygame.image.load('src/Nave.png')
    asteroide50 = pygame.image.load('src/asteroide50.png')
    asteroide125 = pygame.image.load('src/asteroide125.png')
    asteroid200 = pygame.image.load('src/asteroide200.png')
    shoot = pygame.mixer.Sound('src/wav-trolos/shoot.wav')
    bangFuerte = pygame.mixer.Sound('src/wav-trolos/bangFuerte.wav')
    bangNormal = pygame.mixer.Sound('src/wav-trolos/bangNormal.wav')
    endTrolo = pygame.mixer.Sound('src/wav-trolos/end-JIJIJAJA.wav')

    # Volumen
    vol = .2
    shoot.set_volume(vol)
    bangFuerte.set_volume(vol)
    bangNormal.set_volume(vol)
    endTrolo.set_volume(vol)


    # Clases
    class Player(object):
        def __init__(self):
            self.img = nave
            self.w = self.img.get_width()
            self.h = self.img.get_height()
            self.x = largoP // 2
            self.y = anchoP // 2
            self.angulo = 0
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosine = math.cos(math.radians(self.angulo + 90))
            self.sine = math.sin(math.radians(self.angulo + 90))
            self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

        def draw(self, vict):
            vict.blit(self.rotatedSurf, self.rotatedRect)

        def turnLeft(self):
            self.angulo += 5
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosine = math.cos(math.radians(self.angulo + 90))
            self.sine = math.sin(math.radians(self.angulo + 90))
            self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

        def turnRight(self):
            self.angulo -= 5
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosine = math.cos(math.radians(self.angulo + 90))
            self.sine = math.sin(math.radians(self.angulo + 90))
            self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

        def moveForward(self):
            self.x += self.cosine * 6
            self.y -= self.sine * 6
            self.rotatedSurf = pygame.transform.rotate(self.img, self.angulo)
            self.rotatedRect = self.rotatedSurf.get_rect()
            self.rotatedRect.center = (self.x, self.y)
            self.cosine = math.cos(math.radians(self.angulo + 90))
            self.sine = math.sin(math.radians(self.angulo + 90))
            self.head = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

        def updateLocation(self):
            if self.x > largoP + 50:
                self.x = 0
            elif self.x < 0 - self.w:
                self.x = largoP
            elif self.y < -50:
                self.y = anchoP
            elif self.y > anchoP + 50:
                self.y = 0


    class Bullet(object):
        def __init__(self):
            self.point = player.head
            self.x, self.y = self.point
            self.w = 4
            self.h = 4
            self.c = player.cosine
            self.s = player.sine
            self.xv = self.c * 10
            self.yv = self.s * 10

        def move(self):
            self.x += self.xv
            self.y -= self.yv

        def draw(self, win):
            pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.w, self.h])

        def checkOffScreen(self):
            if self.x < -50 or self.x > largoP or self.y > anchoP or self.y < -50:
                return True


    class Asteroid(object):
        def __init__(self, rank):
            self.rank = rank
            if self.rank == 1:
                self.image = asteroide50
            elif self.rank == 2:
                self.image = asteroide125
            else:
                self.image = asteroid200
            self.w = 50 * rank
            self.h = 50 * rank
            self.ranPoint = random.choice(
                [(random.randrange(0, largoP - self.w), random.choice([-1 * self.h - 5, anchoP + 5])),
                (random.choice([-1 * self.w - 5, largoP + 5]), random.randrange(0, anchoP - self.h))])
            self.x, self.y = self.ranPoint
            if self.x < largoP // 2:
                self.xdir = 1
            else:
                self.xdir = -1
            if self.y < anchoP // 2:
                self.ydir = 1
            else:
                self.ydir = -1
            self.xv = self.xdir * random.randrange(1, 3)
            self.yv = self.ydir * random.randrange(1, 3)

        def draw(self, vict):
            vict.blit(self.image, (self.x, self.y))


    # Texto Visible
    def redrawGameWindow():
        victoria.blit(fondo, (0, 0))

        font = pygame.font.SysFont('aharoni', 34)
        fontMiembros = pygame.font.SysFont('aharoni', 24, 0, 1)

        vidasT = font.render('Vidas: ' + str(vidas), True, (0, 204, 0))
        playAgainText = font.render('ESC para reiniciar', True, (255, 255, 255))
        puntuacionT = font.render('Puntuación: ' + str(puntuacion), True, (255, 255, 255))
        mayorPuntuacionT = font.render('Mayor Puntuación: ' + str(mayorPuntuacion), True, (0, 204, 204))
        mutexD = fontMiembros.render("Preciona 'M ' si deseas silenciarlo", True, (255, 255, 255))

        miembros = fontMiembros.render('Realizado por: APEU, AGI y LMFA', True, (51, 255, 153))

        player.draw(victoria)
        for i in asteroids:
            i.draw(victoria)
        for j in playerBullets:
            j.draw(victoria)

        if disparoGOD:
            pygame.draw.rect(victoria, (0, 0, 0), [largoP // 2 - 51, 19, 102, 22])

        if finJIJIJAJA:
            victoria.blit(playAgainText,
                        (largoP // 2 - playAgainText.get_width() // 2, anchoP // 2 - playAgainText.get_height() // 2))


        victoria.blit(puntuacionT, (largoP - puntuacionT.get_width() - 25, 25))
        victoria.blit(vidasT, (25, 25))
        victoria.blit(mayorPuntuacionT, (largoP - mayorPuntuacionT.get_width() - 25, 35 + puntuacionT.get_height()))
        victoria.blit(mutexD, (10, 690))
        victoria.blit(miembros, (975, 690))

        pygame.display.update()


    # Arrays
    player = Player()
    playerBullets = []
    asteroids = []
    count = 0

    # Ejecución
    run = True
    while run:
        clock.tick(60)
        count += 1
        if not finJIJIJAJA:
            if count % 50 == 0:
                ran = random.choice([1, 1, 1, 2, 2, 3])
                asteroids.append(Asteroid(ran))

            player.updateLocation()
            for b in playerBullets:
                b.move()
                if b.checkOffScreen():
                    playerBullets.pop(playerBullets.index(b))

            for a in asteroids:
                a.x += a.xv
                a.y += a.yv

                if (player.x - player.w // 2 <= a.x <= player.x + player.w // 2) or (
                        player.x + player.w // 2 >= a.x + a.w >= player.x - player.w // 2):
                    if (player.y - player.h // 2 <= a.y <= player.y + player.h // 2) or (
                            player.y - player.h // 2 <= a.y + a.h <= player.y + player.h // 2):
                        vidas -= 1
                        asteroids.pop(asteroids.index(a))
                        if isSoundOn:
                            bangFuerte.play()
                        break

                for b in playerBullets:
                    if (a.x <= b.x <= a.x + a.w) or a.x <= b.x + b.w <= a.x + a.w:
                        if (a.y <= b.y <= a.y + a.h) or a.y <= b.y + b.h <= a.y + a.h:
                            if a.rank == 3:
                                if isSoundOn:
                                    bangFuerte.play()
                                puntuacion += 10
                                na1 = Asteroid(2)
                                na2 = Asteroid(2)
                                na1.x = a.x
                                na2.x = a.x
                                na1.y = a.y
                                na2.y = a.y
                                asteroids.append(na1)
                                asteroids.append(na2)
                            elif a.rank == 2:
                                if isSoundOn:
                                    bangNormal.play()
                                puntuacion += 20
                                na1 = Asteroid(1)
                                na2 = Asteroid(1)
                                na1.x = a.x
                                na2.x = a.x
                                na1.y = a.y
                                na2.y = a.y
                                asteroids.append(na1)
                                asteroids.append(na2)
                            else:
                                puntuacion += 30
                                if isSoundOn:
                                    bangNormal.play()
                            asteroids.pop(asteroids.index(a))
                            playerBullets.pop(playerBullets.index(b))
                            break

            if vidas <= 0:
                endTrolo.play()
                finJIJIJAJA = True
                sock.sendall(str.encode(f"{puntuacion},{user}"))

                
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_a]:
                player.turnLeft()
            if teclas[pygame.K_d]:
                player.turnRight()
            if teclas[pygame.K_w]:
                player.moveForward()
            if teclas[pygame.K_SPACE]:
                if disparoGOD:
                    playerBullets.append(Bullet())
                    if isSoundOn:
                        shoot.play()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not finJIJIJAJA:
                        if not disparoGOD:
                            playerBullets.append(Bullet())
                            if isSoundOn:
                                shoot.play()
                if event.key == pygame.K_m:
                    isSoundOn = not isSoundOn
                if event.key == pygame.K_ESCAPE:
                    if finJIJIJAJA:
                        finJIJIJAJA = False
                        vidas = 3
                        asteroids.clear()
                        if puntuacion > mayorPuntuacion:
                            mayorPuntuacion = puntuacion
                        puntuacion = 0
        redrawGameWindow()
    pygame.quit()

# JIJIJAJA