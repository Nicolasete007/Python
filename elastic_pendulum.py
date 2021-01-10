from vpython import *
from numpy import sin, cos, pi

grav  = 9.81
mass  = 2
long0 = 1.5
kCons = 40
dt = 1e-2

def createAxis():
	size = 2*long0
	xaxis = arrow(pos=vector(0, 0, 0), axis=vector(1, 0, 0) * size, color=color.green, shaftwidth=0.05)
	yaxis = arrow(pos=vector(0, 0, 0), axis=vector(0, 1, 0) * size, color=color.green, shaftwidth=0.05)
	zaxis = arrow(pos=vector(0, 0, 0), axis=vector(0, 0, 1) * size, color=color.green, shaftwidth=0.05)
	xText = text(text="X Axis", pos=xaxis.axis*0.62 + vector(0, size*0.1, 0), axis=xaxis.axis, height=size/10, color=color.green)
	yText = text(text="Y Axis", pos=yaxis.axis*0.62 + vector(size*0.15, 0, 0), axis=yaxis.axis, height=size/10, color=color.green)
	zText = text(text="Z Axis", pos=zaxis.axis + vector(0, size*0.1, 0), axis=-zaxis.axis, height=size/10, color=color.green)

def KinEn(longi, dLongi, dTheta):
	return 0.5*mass*(dLongi**2 + longi**2 * dTheta**2)

def GravPotEn(longi, theta):
	return - longi*cos(theta)*mass*grav

def ElasPotEn(longi):
	return 0.5*kCons*(longi - long0)**2

def d2Longi(longi, theta, dTheta):
	d2Longi = longi * dTheta**2 + grav*cos(theta) - kCons/mass * (longi-long0)
	return d2Longi

def d2Theta(longi, theta, dLongi, dTheta):
	d2Theta = - (2*dLongi*dTheta + grav*sin(theta)) / longi
	return d2Theta

def deriv(longi, theta, dLongi, dTheta):

	lOut = dLongi
	tOut = dTheta
	dLOut = d2Longi(longi, theta, dTheta)
	dTOut = d2Theta(longi, theta, dLongi, dTheta)

	return (lOut, tOut, dLOut, dTOut)

def RK4Step(yIn, dt):

	k1 = deriv(yIn[0], 				yIn[1], 			 yIn[2],			  yIn[3]			 )
	k2 = deriv(yIn[0] + dt*k1[0]/2, yIn[1] + dt*k1[1]/2, yIn[2] + dt*k1[2]/2, yIn[3] + dt*k1[3]/2)
	k3 = deriv(yIn[0] + dt*k2[0]/2, yIn[1] + dt*k2[1]/2, yIn[2] + dt*k2[2]/2, yIn[3] + dt*k2[3]/2)
	k4 = deriv(yIn[0] + dt*k3[0]  , yIn[1] + dt*k3[1]  , yIn[2] + dt*k3[2]	, yIn[3] + dt*k3[3]	 )

	yOut1 = yIn[0] + dt*(k1[0] + 2*k2[0] + 2*k3[0] + k4[0]) / 6
	yOut2 = yIn[1] + dt*(k1[1] + 2*k2[1] + 2*k3[1] + k4[1]) / 6
	yOut3 = yIn[2] + dt*(k1[2] + 2*k2[2] + 2*k3[2] + k4[2]) / 6
	yOut4 = yIn[3] + dt*(k1[3] + 2*k2[3] + 2*k3[3] + k4[3]) / 6

	return (yOut1, yOut2, yOut3, yOut4)

winSize = 400

animation = canvas(width=winSize, height=winSize, align='left')
animation.title = "Elastic pendulum simulation"
animation.caption = """This simulation was made using the RK4 method (Runge Kutta order 4) with a time step of 0.01 seconds at 100 fps.
Constants:
  - Gravity = 9.81 m/s²
  - Mass (ball) = 2 kg
  - Natural spring length = 1.5 m
  - Spring constant = 40 N/m"""
animation.center = long0*vector(1, 1, 1)

energyGraph  = graph(width=2*winSize, height=winSize, align='left', xtitle='Time (s)', ytitle='Energy (J)')
kineticCurve = gcurve(color=color.cyan, label="Kinetic Energy")
elasticCurve = gcurve(color=color.red, label="Elastic Potential Energy")
gravitaCurve = gcurve(color=color.purple, label="Gravitational Potential Energy")
totalEnergy  = gcurve(color=color.green, label="Total Energy")

pendPos = vector(long0/2, 2*long0, long0/2)

ball = sphere(radius=0.3, color=color.orange, make_trail=True, retain=200, trail_color=color.red, trail_radius=0.02)
spring = helix(pos=pendPos, radius=0.15, thickness=0.05, coils=10, color=color.orange)
bar0 = arrow(pos=spring.pos, color=color.red, shaftwidth=0.05)

ballCoords = (long0*0.75, pi/3, 0, 0)

createAxis()

t = 0
while True:

	rate(100)

	ballCoords = RK4Step(ballCoords, dt)

	ball.pos = vector(ballCoords[0]*sin(ballCoords[1]),
					 -ballCoords[0]*cos(ballCoords[1]),
					  0) + pendPos
	spring.axis = ball.pos - pendPos
	bar0.axis = vector(long0*sin(ballCoords[1]),
					  -long0*cos(ballCoords[1]), 0)

	t += dt

	kinE  = KinEn(ballCoords[0], ballCoords[2], ballCoords[3])
	ePotE = ElasPotEn(ballCoords[0])
	gPotE = GravPotEn(ballCoords[0], ballCoords[1])
	totE  = kinE + ePotE + gPotE

	kineticCurve.plot(t, kinE)
	elasticCurve.plot(t, ePotE)
	gravitaCurve.plot(t, gPotE)
	totalEnergy.plot(t, totE)

	energyGraph.xmin = t - 10
	energyGraph.xmax = t