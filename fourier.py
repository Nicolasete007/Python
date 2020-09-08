from numpy import sin, cos, exp, pi, sqrt, arctan2
import pygame as pg


def dft(values):

	X = []
	N = len(values)

	for k in range(len(values)):

		re = 0
		im = 0

		for n in range(len(values)):

			re += values[n] * cos(2*pi*k*n / N)
			im -= values[n] * sin(2*pi*k*n / N)

		re *= 1/N
		im *= 1/N

		freq = k
		amp = sqrt(re**2 + im**2)
		phase = arctan2(im, re)

		X.append({"re": re, "im": im, "f": freq, "A": amp, "phi": phase})

	return(X)


def epicycles(x, y, fourier, offset):

	sorted_dic = fourier[0]
	fourier2 = []
	copy_list = fourier.copy()

	for j in range(len(fourier)):
	    
	    for i in range(len(copy_list)):

	        if sorted_dic["A"] < copy_list[i]["A"]:
	            sorted_dic = copy_list[i]

	    fourier2.append(sorted_dic)
	    copy_list.remove(sorted_dic)
	    sorted_dic = copy_list[0] if len(copy_list) > 0 else None

	for i in range(len(fourier2)):
		
		prevX = x
		prevY = y

		f = fourier2[i]
		freq = f["f"]
		radius = f["A"]
		phase = f["phi"]
		x += radius * cos(freq * time + phase + offset)
		y += radius * sin(freq * time + phase + offset)
 	
		pg.draw.circle(SCREEN, D_GRAY, (int(prevX), int(prevY)), max(int(radius), 1), 1)
		pg.draw.line(SCREEN, GRAY, (int(prevX), int(prevY)), (int(x), int(y)), 1)

	return x, y


def draw_circles():

	global time, DONE, SKETCH

	fourierX = dft(X)
	fourierY = dft(Y)
	
	xx, xy = epicycles(SCREEN_SIZE[0]/2, 50, fourierX, 0)
	yx, yy = epicycles(50, SCREEN_SIZE[1]/2, fourierY, pi*.5)

	pg.draw.line(SCREEN, D_GRAY, (xx, yy), (yx, yy), 1)
	pg.draw.line(SCREEN, D_GRAY, (xx, xy), (xx, yy), 1)
	
	SKETCH.append([int(xx), int(yy)])

	dt = 2*pi/LENGTH
	time += dt

	if time > 2*pi:
		time = 0
		SKETCH = []

	if len(SKETCH) > 1:
		pg.draw.lines(SCREEN, RED, False, SKETCH, 2)

pg.init()

SCREEN_SIZE = (1200, 650)
SCREEN = pg.display.set_mode(SCREEN_SIZE)

WHITE  = (255, 255, 255)
GRAY   = (150, 150, 150)
D_GRAY = ( 50,  50,  50)
BLACK  = (  0,   0,   0)
BLUE   = ( 50,  50, 255)
RED    = (255,  50,  50)

X = []
Y = []

time = 0
SKETCH = []
PRE_SKETCH = []
DRAWN = False
MAX_LENGTH = 100

QUIT = False
while not QUIT:

	for event in pg.event.get():
		if event.type == pg.QUIT:
			QUIT = True

		if event.type == pg.MOUSEBUTTONUP:
			DRAWN = True
			LENGTH = len(X)

			if LENGTH > MAX_LENGTH:
				newX = []
				newY = []
				skip = round(LENGTH/MAX_LENGTH)
				for i in range(LENGTH):
					if i%skip == 0:
						newX.append(X[i])
						newY.append(Y[i])

				X = newX.copy()
				Y = newY.copy()
				LENGTH = len(X)
	
	SCREEN.fill(BLACK)
	
	if pg.mouse.get_pressed()[0] and not DRAWN:
		mouseX, mouseY = pg.mouse.get_pos()

		xFinal = mouseX-SCREEN_SIZE[0]/2
		yFinal = mouseY-SCREEN_SIZE[1]/2

		X.append(xFinal)
		Y.append(yFinal)

		if (mouseX, mouseY) not in PRE_SKETCH:
			PRE_SKETCH.append((mouseX, mouseY))
	
	if len(PRE_SKETCH) > 1:
		pg.draw.lines(SCREEN, BLUE, False, PRE_SKETCH, 2)

	if DRAWN:
		draw_circles()

	pg.display.flip()

pg.quit()