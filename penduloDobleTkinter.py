from tkinter import Label, Checkbutton, Entry, Button, BooleanVar, Tk, Canvas, Scale, HORIZONTAL, DoubleVar, FLAT
import time
from numpy import sin, cos, pi

# VARIABLES #
BARS = "#00FFFF"
LINE = "#FF0099"
BACKGROUND = "#000000"
TEXT = "#00FF00"
ENTRY = "#222222"
SCALE = "#009900"

SIZE = (1200, 600)

canvasW = SIZE[0]/2
canvasH = SIZE[1]

lines = []

fric = 0
g = 0.5
xFix = int(canvasW/2)
yFix = int(canvasH/2)

l1 = 100
l2 = 100
m1 = 100
m2 = 100
O1 = 2
O2 = 0.5*pi

w1 = 0
w2 = 0

paused = False
# VARIABLES #


# FUNCIONES #
def omega1Prime(O1, O2, w1, w2, g, m1, m2, l1, l2):
	
	num1 = g*(2*m1+m2)*sin(O1)
	num2 = m2*g*sin(O1-2*O2)
	num3 = 2*sin(O1-O2)*m2*((w2**2)*l2 + (w1**2)*l1* cos(O1-O2))

	den = l1*(2*m1 + m2 - m2*cos(2*O1-2*O2))

	w1p = (-num1 -num2 -num3)/den

	return w1p

def omega2Prime(O1, O2, w1, w2, g, m1, m2, l1, l2):

	num = 2*sin(O1-O2)*((w1**2)*l1*(m1+m2) + g*(m1+m2)*cos(O1) + (w2**2)*l2*m2*cos(O1-O2))
	den = l2*(2*m1 + m2 - m2*cos(2*O1 - 2*O2))
	w2p = num/den

	return w2p

def pendPos(l, angle, x0, y0):
	x = int(l*sin(angle)) + x0
	y = int(l*cos(angle)) + y0

	return (x, y)

def calculate(O1, O2, w1, w2, m1, m2, l1, l2, g, fric):

	w1p = omega1Prime(O1, O2, w1, w2, g, m1, m2, l1, l2)
	w2p = omega2Prime(O1, O2, w1, w2, g, m1, m2, l1, l2)

	w1 += w1p
	w2 += w2p

	w1 *= 1 - fric/100
	w2 *= 1 - fric/100

	O1 += w1
	O2 += w2

	O1 = O1 % (2*pi)
	O2 = O2 % (2*pi)

	return (O1, O2, w1, w2)

def energy(m1, m2, O1, O2, w1, w2, g):

	kinetic = 0.5*m1*l1**2*w1**2 + 0.5*m2*(l1**2*w1**2 + l2**2*w2**2 + 2*l1*l2*w1*w2*cos(O1-O2))

	potential = m1*g*l1*(1 - cos(O1)) + (l1 + l2 - l1*cos(O1) - l2*cos(O2))*m2*g

	total = potential + kinetic

	return kinetic, potential, total

def Pause():
	global paused
	paused = not paused

def ClearLines():
	global lines
	lines = []

def getO1():
	global O1, w1, w2
	try:
		O1 = float(O1Entry.get())*pi if usePi1.get() else float(O1Entry.get())
		w1 = 0
		w2 = 0
	except:
		pass

def getO2():
	global O2, w1, w2
	try:
		O2 = float(O2Entry.get())*pi if usePi2.get() else float(O2Entry.get())
		w1 = 0
		w2 = 0
	except:
		pass

def move():
	global O1, O2, w1, w2, usePi

	l1 = l1scale.get()
	l2 = l2scale.get()
	m1 = m1scale.get()
	m2 = m2scale.get()
	g = gscale.get()
	fric = fricscale.get()

	kinetic, potential, total = energy(m1, m2, O1, O2, w1, w2, g)

	if not paused:
		O1, O2, w1, w2 = calculate(O1, O2, w1, w2, m1, m2, l1, l2, g, fric)

	print(O1, O2)
	x1, y1 = pendPos(l1, O1, xFix, yFix)
	x2, y2 = pendPos(l2, O2, x1, y1)

	
	if not paused:
		lines.append((x2, y2))
	if len(lines) >= 5000:
		lines.pop(0)

	canvas.delete("all")

	try:
		canvas.create_line(lines, width=1, fill=LINE)
		
	except:
		pass

	r1 = int(20*(m1**0.5/(m1**0.5+m2**0.5)))
	r2 = int(20*(m2**0.5/(m1**0.5+m2**0.5)))

	canvas.create_line(xFix, yFix, x1, y1, width=2, fill=BARS)
	canvas.create_line(x1, y1, x2, y2, width=2, fill=BARS)
	canvas.create_oval(x1-r1, y1-r1, x1+r1, y1+r1, fill=BACKGROUND, outline=BARS, width=2)
	canvas.create_oval(x2-r2, y2-r2, x2+r2, y2+r2, fill=BACKGROUND, outline=BARS, width=2)

	canvas.create_rectangle(5, 5, 20, SIZE[1]-5, fill=LINE)

	div = kinetic/total if (kinetic != 0 and total != 0) else 0
	canvas.create_rectangle(5, 5, 20, max((SIZE[1])*div - 5, 5), fill=BARS)

	root.after(10, move)

# FUNCIONES #

root = Tk()
root.configure(bg=BACKGROUND)
canvas = Canvas(root, width=canvasW, height=canvasH, bg=BACKGROUND, highlightthickness=0)
root.title("Pénulo")
canvas.grid(row=0, column=0, rowspan=20)

PauseButton = Button(root, width=5, text="Pausa", command=Pause, relief=FLAT, bg=ENTRY, fg=TEXT, activeforeground=BACKGROUND, activebackground=TEXT)
PauseButton.grid(row=0, column=1)

ClearButton = Button(root, width=5, text="Esborra", command=ClearLines, relief=FLAT, bg=ENTRY, fg=TEXT, activeforeground=BACKGROUND, activebackground=TEXT)
ClearButton.grid(row=0, column=2)

l1Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Barra 1")
l1Label.grid(row=1, column=1, columnspan=2)
l1scale = DoubleVar()
l1Scale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=1, to=200, orient=HORIZONTAL, variable=l1scale, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
l1Scale.set(l1)
l1Scale.grid(row=2, column=1, columnspan=2)

l2Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Barra 2")
l2Label.grid(row=3, column=1, columnspan=2)
l2scale = DoubleVar()
l2Scale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=1, to=200, orient=HORIZONTAL, variable=l2scale, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
l2Scale.set(l2)
l2Scale.grid(row=4, column=1, columnspan=2)

m1Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Massa 1")
m1Label.grid(row=5, column=1, columnspan=2)
m1scale = DoubleVar()
m1Scale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=1, to=200, orient=HORIZONTAL, variable=m1scale, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
m1Scale.set(m1)
m1Scale.grid(row=6, column=1, columnspan=2)

m2Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Massa 2")
m2Label.grid(row=7, column=1, columnspan=2)
m2scale = DoubleVar()
m2Scale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=1, to=200, orient=HORIZONTAL, variable=m2scale, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
m2Scale.set(m2)
m2Scale.grid(row=8, column=1, columnspan=2)

fricLabel = Label(root, bg=BACKGROUND, fg=TEXT, text="Fricció")
fricLabel.grid(row=9, column=1, columnspan=2)
fricscale = DoubleVar()
fricScale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=0, to=100, resolution=0.01, orient=HORIZONTAL, variable=fricscale, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
fricScale.set(fric)
fricScale.grid(row=10, column=1, columnspan=2)

gLabel = Label(root, bg=BACKGROUND, fg=TEXT, text="Gravetat")
gLabel.grid(row=11, column=1, columnspan=2)
gscale = DoubleVar()
gScale = Scale(root, bg=BACKGROUND, fg=TEXT, from_=-10, to=10, orient=HORIZONTAL, variable=gscale, resolution=0.01, highlightthickness=0, activebackground=BACKGROUND, sliderrelief=FLAT, troughcolor=SCALE)
gScale.set(g)
gScale.grid(row=12, column=1, columnspan=2)

O1Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Angle 1")
O1Label.grid(row=13, column=1, columnspan=2)
O1Entry = DoubleVar()
O1Entry = Entry(root, width=8, bg=ENTRY, fg=TEXT, justify="right", relief=FLAT)
O1Entry.grid(row=14, column=1)

usePi1 = BooleanVar()
O1Check = Checkbutton(root, text="pi", variable=usePi1, bg=BACKGROUND, fg=TEXT, activebackground=BACKGROUND, activeforeground=TEXT,  selectcolor=BACKGROUND)
O1Check.grid(row=14, column=2)
O1Button = Button(root, width=13, text="Okidoki", command=getO1, relief=FLAT, bg=ENTRY, fg=TEXT, activeforeground=BACKGROUND, activebackground=TEXT)
O1Button.grid(row=15, column=1, columnspan=2)

O2Label = Label(root, bg=BACKGROUND, fg=TEXT, text="Angle 2")
O2Label.grid(row=16, column=1, columnspan=2)
O2Entry = DoubleVar()
O2Entry = Entry(root, width=8, bg=ENTRY, fg=TEXT, justify="right", relief=FLAT)
O2Entry.grid(row=17, column=1)

usePi2 = BooleanVar()
O2Check = Checkbutton(root, text="pi", variable=usePi2, bg=BACKGROUND, fg=TEXT, activebackground=BACKGROUND, activeforeground=TEXT,  selectcolor=BACKGROUND)
O2Check.grid(row=17, column=2)
O2Button = Button(root, width=13, text="Okidoki", command=getO2, relief=FLAT, bg=ENTRY, fg=TEXT, activeforeground=BACKGROUND, activebackground=TEXT)
O2Button.grid(row=18, column=1, columnspan=2)


move()
root.mainloop()