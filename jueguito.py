import pygame
import sys
import random
from donas import Dona

from config import *

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Donuts")

icono = pygame.image.load("./src/images/homero.png").convert_alpha()
icono = pygame.transform.scale(icono, SIZE_ICON)
pygame.display.set_icon(icono)

font = pygame.font.Font("./src/font/simpsons.ttf", 48)

score = 0

sonido = pygame.mixer.Sound("./src/sounds/ouch.mp3")
pygame.mixer.music.load("./src/sounds/ouch.mp3")
flag_sound = True


fondo = pygame.image.load("./src/images/background.jpg").convert_alpha()
fondo = pygame.transform.scale(fondo, SIZE)

donas = []

for i in range(10):
    x = random.randrange(30, WIDTH-30)
    y = random.randrange(-1000, 0)
    dona = Dona(DONA_SIZE, (x,y), "./src/images/dona.png")
    #dona = pygame.image.load("./src/images/dona.png").convert_alpha()
    #dona = pygame.transform.scale(dona, DONA_SIZE)
    #dona.get_rect().center = (random.randrange(30, WIDTH-30), random.randrange(-1000, 0))
    donas.append(dona)



homero_l= pygame.transform.scale(pygame.image.load("./src/images/homer_left.png").convert_alpha(), HOMER_SIZE)


homero_r = pygame.transform.scale(pygame.image.load("./src/images/homer_right.png").convert_alpha(), HOMER_SIZE)

homero = homero_l
homero_rect = homero_l.get_rect()
homero_rect.midbottom = (CENTER_X, DISPLAY_BOTTOM)
rect_boca = pygame.rect.Rect(0,0, 50, 10)
rect_boca.x = homero_rect.x + 40
rect_boca.y = homero_rect.y+ 130


while True:

    clock.tick(FPS)

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
         pygame.quit()
         sys.exit()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
       if homero_rect.left > DISPLAY_LEFT:
          homero_rect.x -= HOMER_SPEED
          rect_boca.x = homero_rect.x + 40
          rect_boca.y = homero_rect.y+ 130
          homero = homero_l
    if keys[pygame.K_RIGHT]:
       if homero_rect.right < DISPLAY_RIGHT:
          homero_rect.x += HOMER_SPEED
          rect_boca.x = homero_rect.x + 70
          rect_boca.y = homero_rect.y+ 130
          homero = homero_r
       
       
       
    screen.blit(fondo, ORIGIN)
    texto = font.render("Score: " + str(score), True, GREEN)
    screen.blit(texto, SCORE_POS)
    pygame.draw.rect(screen, RED, rect_boca)
    screen.blit(homero, homero_rect)

    for dona in donas:

       if dona.rect.bottom < DISPLAY_BOTTOM:
        flag_dona = True
        flag_sound = True
        if dona.active:
                dona.update()
        else:
            dona.rect.y = 0
        if rect_boca.colliderect(dona.rect):
            dona.active = False
            if flag_sound:
                score += 1
                pygame.mixer.music.play()
                pygame.mixer.music.set_pos(0.3)
                flag_sound = False
            else:
                flag_sound = True
        if dona.active:
            screen.blit(dona.image, dona.rect)



    pygame.display.flip()