import pygame

pygame.font.init()

FPS = 60
size = (1400,900)
time = 7
#BACKGROUND = pygame.image.load('background.png')

#---- C O L O R S ----#
WHITE = (255,255,255)
BLACK = (0,0,0)

RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)

GRASS = (117,190,49)
GROUND = (224,215,146)
SKY = (78,192,202)
#---- C O L O R S ----#

#---- P L A Y E R ----#
PLAYER_IMAGE = pygame.image.load('player.png')
P_SIZE = PLAYER_IMAGE.get_size()

ARROW_IMAGE = pygame.image.load('arrow.png')
A_SIZE = ARROW_IMAGE.get_size()

VEL = 14
GRAVITY = -0.8
CUP_VEL = 1
#---- P L A Y E R ----#

#--- C U P C A K E ---#
CupcakePics = [pygame.image.load('cupcake1.png'),
               pygame.image.load('cupcake2.png'),
               pygame.image.load('cupcake3.png'),
               pygame.image.load('cupcake4.png'),
               pygame.image.load('cupcake5.png')]
C_SIZE = (128,128)
#--- C U P C A K E ---#

#------ F A R T ------#
FART_IMAGE = pygame.image.load('fart.png')
F_SIZE = FART_IMAGE.get_size()
#------ F A R T ------#
