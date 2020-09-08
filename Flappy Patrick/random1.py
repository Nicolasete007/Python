import random
import pygame
import math
from settings import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Flappy Patricio")
done = False
clock = pygame.time.Clock()

roboto30 = pygame.font.SysFont('roboto',30, False, False)
roboto50 = pygame.font.SysFont('roboto',50, False, False)

GameState = 1

CUPCAKES = []
spawnCupcake = 2*FPS

HIGHSCORE = 0
oldHigh = 0

class Player:
	
	def __init__(self):
		
		self.x = size[0]/2
		self.y = size[1]/4
		self.xV = 0
		self.yV = 0

		self.player_rotated = PLAYER_IMAGE
		self.centerx = self.player_rotated.get_rect().centerx
		self.centery = self.player_rotated.get_rect().centery
		
		self.stopping = 50
		self.flap_cooldown = 0
		self.angle = 0

		self.life = 100
		self.life_length = 1.2*self.life
		self.life_color = GREEN
	
	def flap(self):
		
		if self.life > 0 and self.flap_cooldown == 0:
			
			#Both sin and cos are changed, because of the angle used
			self.xV = math.sin(math.radians(self.angle)) * VEL
			self.yV = math.cos(math.radians(self.angle)) * VEL

			#Scale, rotate and set fart's alpha and position
			fart.counter = 250
			fart.fart_rotated = pygame.transform.scale(FART_IMAGE, (int(F_SIZE[0]/2), int(F_SIZE[1]/2)))
			fart.fart_rotated = pygame.transform.rotate(fart.fart_rotated, self.angle - 90)
			
			fart.x = player.x + int(math.sin(math.radians(player.angle)) * 120)
			fart.y = player.y + int(math.cos(math.radians(player.angle)) * 120)

	def loseLife(self):

		self.life_length = 1.2*self.life
		
		if self.life <= 50 and self.life > 10:
			self.life_color = YELLOW
		elif self.life <= 10:
			self.life_color = RED

	def update(self):

		if self.flap_cooldown > 0:
			self.flap_cooldown -= 1
		
		#Get the angle
		mousex, mousey = pygame.mouse.get_pos()
		self.angle = math.degrees(math.atan2(mousex-self.x, mousey-self.y))
		
		#Rotate the player with the given angle
		if self.life > 0:
			self.player_rotated = pygame.transform.rotate(PLAYER_IMAGE, self.angle)
		
		self.centerx = self.player_rotated.get_rect().centerx
		self.centery = self.player_rotated.get_rect().centery
		
		#---- P H Y S I C S ----#
		#----- XXX A X I S -----#
		if self.x >= size[0]-100:
			self.x = size[0]-100
			self.xV -= 1.8*self.xV
			
		elif self.x <= 100:
			self.x = 100
			self.xV -= 1.8*self.xV
		#----- XXX A X I S -----#

		#----- YYY A X I S -----#
		if self.y > size[1]-210 and self.y < size[1]-195 and self.stopping > 0: #To avoid vibration patrick
			self.stopping -= 1                                                  #To avoid vibration patrick
		else:                                                                   #To avoid vibration patrick
			self.stopping = 50                                                  #To avoid vibration patrick
		
		if self.y >= size[1]-200 and self.stopping > 0:
			self.y = size[1]-200
			self.yV -= 1.8*self.yV
			self.xV = self.xV * 0.8

		elif self.stopping <= 0:                                                #To avoid vibration patrick
			self.y = size[1]-200                                                #To avoid vibration patrick
			self.yV = 0                                                         #To avoid vibration patrick
			
		else:
			self.yV += GRAVITY
		#----- YYY A X I S -----#

		self.y -= self.yV
		self.x -= self.xV
		#---- P H Y S I C S ----#
	
	def draw(self):
		
		self.player_rotated.convert()
		screen.blit(self.player_rotated, (self.x - self.centerx, self.y - self.centery))

		if self.life > 0:
			pygame.draw.rect(screen,self.life_color,(player.x - self.life_length/2,player.y + 2*P_SIZE[1]/3,self.life_length,15))

player = Player()

class Cupcake:
	
	def __init__(self):
		
		self.x = random.randint(100, size[0]-150)
		self.y = -C_SIZE[1]/2
		self.vel = -CUP_VEL - points.points/10
		self.xS = C_SIZE[0]
		self.yS = C_SIZE[1]
		self.angle = 0
		self.opacity = 255
		self.scale = 1

		self.dtime = time
		self.countdown = FPS
		self.roboto30 = pygame.font.SysFont('roboto',30, False, False)
		self.time_text = self.roboto30.render(str(self.dtime),True,BLACK)

		self.pic = random.randint(0, 4)
		self.centerx = CupcakePics[self.pic].get_rect().centerx
		self.centery = CupcakePics[self.pic].get_rect().centery

	def eaten(self):

		points.plusOne()

		CUPCAKES.remove(self)
		del self

	def explode(self):
		
		self.exp_dist = math.sqrt((player.x-self.x)**2 + (player.y-self.y)**2)
		self.angle = math.degrees(math.atan2(player.x-self.x, player.y-self.y)) + 270
		self.hit = 10000/self.exp_dist
		
		player.xV = -self.hit*math.cos(math.radians(self.angle))
		player.yV = self.hit*math.sin(math.radians(self.angle))
		player.loseLife()
		
	def update(self):
		
		#----- T I M E R -----#
		if self.countdown == 0 and self.dtime > 0:
			self.dtime -= 1
			self.countdown = FPS
		else:
			self.countdown -= 1

		if self.countdown == -1 and player.flap_cooldown <= 0:
			self.explode()
			player.life -= int(self.hit)
			player.flap_cooldown = int(1000/self.exp_dist * FPS)
			self.hit = 0

		self.time_text = self.roboto30.render(str(self.dtime), True, BLACK)
		self.textX = self.time_text.get_rect().centerx
		self.textY = self.time_text.get_rect().centery
		#----- T I M E R -----#
		
		if self.y < size[1] - 200:
			self.y -= self.vel
			
		self.playerX = player.centerx + player.x
		self.playerY = player.centery + player.y
		
		if self.playerX >= self.x and self.playerX <= self.x + self.xS and self.playerY >= self.y and self.playerY <= self.y + self.yS and player.life > 0 and player.flap_cooldown == 0:
			self.eaten()

		if self.opacity == 0:
			CUPCAKES.remove(self)
		del self

	def draw(self):
		
		if self.countdown <= -1:
			self.explode()
			self.opacity = max(0, self.opacity - 50)
			self.scale *= 1.2

		img = CupcakePics[self.pic].convert()
		img.set_alpha(self.opacity)
		imgCol = img.get_at((0,0)) #Remove transparent
		img.set_colorkey(imgCol)   #background
		img = pygame.transform.scale(img, (int(C_SIZE[0]*self.scale), int(C_SIZE[1]*self.scale)))

		screen.blit(img, (self.x - int(C_SIZE[0]*self.scale)/2, self.y - int(C_SIZE[0]*self.scale)/2))
		screen.blit(self.time_text, (self.x - self.textX, self.y - self.textY - self.centery))

class Fart:
	
	def __init__(self):
		
		self.x = 0
		self.y = 0
		self.counter = 0
		self.fart_rotated = pygame.transform.rotate(FART_IMAGE, 0)

	def update(self):
		
		if self.counter > 0:
			self.counter -= 10

	def draw(self):
		
		self.final_fart = self.fart_rotated.convert()   #Convert to change alpha
		self.final_fart.set_alpha(self.counter)         #Set alpha to self.counter
		self.transColor = self.final_fart.get_at((0,0)) #Remove transparent
		self.final_fart.set_colorkey(self.transColor)   #background
		
		screen.blit(self.final_fart, (self.x - 30, self.y - 50))

fart = Fart()

class Points:
	
	def __init__(self):
		
		self.points = 0

		self.roboto50 = pygame.font.SysFont('roboto',50, False, False)
		self.text = self.roboto50.render("Score: " + str(self.points),True,BLACK)
		self.textX = self.text.get_rect().centerx
		self.textY = self.text.get_rect().centery

		global HIGHSCORE
		with open("highScore.txt", "r") as t:
			HIGHSCORE = t.readline()
		self.high = self.roboto50.render("High score: " + str(HIGHSCORE),True,BLACK)
		self.highX = self.high.get_rect().centerx
		self.highY = self.high.get_rect().centery
		
	def plusOne(self):
		
		self.points += 1

		self.text = self.roboto50.render("Score: " + str(self.points),True,BLACK)
		self.textX = self.text.get_rect().centerx
		self.textY = self.text.get_rect().centery

	def reset(self):

		self.points = 0

points = Points()

class Arrow:

	def __init__(self):

		self.x = 0
		self.image = pygame.transform.scale(ARROW_IMAGE,(25,25))
		self.centerx = self.image.get_rect().centerx

	def draw(self):
		
		if player.y + P_SIZE[1]/2 < 0:
			screen.blit(self.image, (player.x - self.centerx,0))
		
arrow = Arrow()

# -------- Main Program Loop -----------
while not done:
	# --- Main event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		
		if event.type == pygame.KEYDOWN:
			
			if GameState == 1 or GameState == 3:
				GameState = 2
				player.__init__()
				points.__init__()
			
			if event.key == pygame.K_SPACE:
				player.flap()

		if event.type == pygame.MOUSEBUTTONDOWN:

			if GameState == 1 or GameState == 3:
				GameState = 2
				player.__init__()
				points.__init__()

			if event.button == 1:
				player.flap()

	if player.life <= 0:
		if GameState != 3:
			with open("highScore.txt", "r") as t:
				oldHigh = int(t.readline())
			if oldHigh < points.points:
				with open("highScore.txt", "w") as t:
					t.write(str(points.points))

		GameState = 3

	screen.fill(SKY)
	pygame.draw.rect(screen,GRASS,(0,size[1]-200,size[0],200))

	if GameState == 1:
		
		text = roboto50.render("Press any key to play",True,BLACK)
		textX = text.get_rect().width
		textY = text.get_rect().height
		screen.blit(text,((size[0]/2 - (textX / 2)),(size[1]/2 - (textY / 2))))

	elif GameState == 2:
		
		screen.blit(points.text, (size[0]/2 - (points.textX), size[1]/3 - (points.textY)/2))
		screen.blit(points.high, (size[0]/2 - (points.highX), size[1]/3 + 2*(points.highY)))
		
		if spawnCupcake > 0:
			spawnCupcake -= 1
		else:
			CUPCAKES.append(Cupcake())
			spawnCupcake = max(3*FPS - points.points, 0.5*FPS)

		for cup in CUPCAKES:
			cup.update()
			cup.draw()
		
		fart.update()
		fart.draw()
		
		arrow.draw()

		player.update()
		player.draw()

	elif GameState == 3:

		for cup in CUPCAKES:
			cup.update()
			cup.draw()
		
		fart.update()
		fart.draw()
		
		arrow.draw()

		player.update()
		player.draw()
		
		text = roboto50.render("Press any key to continue",True,BLACK)
		textX = text.get_rect().width
		textY = text.get_rect().height
		screen.blit(text,((size[0]/2 - (textX / 2)),(size[1]/2 - (textY / 2))))        
	
	pygame.display.flip()
	
	clock.tick(FPS)

pygame.quit()
