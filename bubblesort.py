import pygame
from pygame import *
from random import randint

pygame.init()
FPS = 60
clock = pygame.time.Clock()

columns = 800
rows = 600

maxnum = columns-2
num = 0
sortedLines = 0

lines = []

def restart_lines(lines):

	for l in range(columns):
		line = Surface((1, randint(1, rows)))
		line.fill(Color(('#ffffff')))
		lines.append(line)

	return lines

lines = restart_lines(lines)

def Sort(line1, line2):
	if line1.get_height() > line2.get_height():
		lines[num], lines[num+1] = lines[num+1], lines[num]

screen = pygame.display.set_mode((columns, rows))

done = False
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == K_r:
			lines = restart_lines(lines)
			maxnum = columns-2
			num = 0
			sortedLines = 0

	screen.fill(Color(('#000000')))

	for i in range(300):
		if num < maxnum-sortedLines:
			num += 1
		else:
			num = 0
			sortedLines += 1

		Sort(lines[num], lines[num+1])

	for l in lines:
		screen.blit(l, (lines.index(l), rows-l.get_height()))

	pygame.display.flip()
    
	clock.tick(FPS)

pygame.quit()