#Program to simulate lattice vibrations in a 2 atom lattice#
#Jamie Bull#
#16/10/2017#

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np

#---------------------------------------------------------------------------------#	
class Atom:
	
	SPRING_CONSTANT = 3000
	SPRING_DAMPING = 200000
	N_DIM = 2
	
	def __init__(self, mass):
		self.mass = mass
		self.pos = np.zeros(self.N_DIM, dtype = float)	#position away from equilibrium
		self.vel = np.zeros(self.N_DIM, dtype = float)
		self.acc = np.zeros(self.N_DIM, dtype = float)
		
	def calcExForce(self, n):
		return (self.SPRING_CONSTANT * self.pos[n])# - (self.SPRING_DAMPING * self.vel[n])
	
	def calcAcc(self, exForce):
		for i in range (0, self.N_DIM):
			self.acc[i] = exForce / self.mass
			
	def calcVel(self, step):
		for i in range (0, self.N_DIM):
			self.vel[i] = self.acc[i] * step
			
	def calcPos(self, step): 	
		for i in range (0, self.N_DIM):
			self.pos[i] = self.vel[i] * step
	
	
	
#Performs a single step of physics on the lattice#
#---------------------------------------------------------------------------------#	
def simulateStep(step):
	
	exForce = [[None for x in range (DIM_SIZE)]for y in range (DIM_SIZE)]
	
	for i in range (DIM_SIZE):
		for j in range (DIM_SIZE):
			
			exForce[i][j] = 0
			if i+1 < DIM_SIZE:
				exForce[i][j] += lattice[i+1][j].calcExForce(0)
			if i-1 > -1:
				exForce[i][j] += lattice[i-1][j].calcExForce(0)
			if j+1 < DIM_SIZE:
				exForce[i][j] += lattice[i][j+1].calcExForce(1)
			if j-1 > -1:
				exForce[i][j] += lattice[i][j-1].calcExForce(1)
				
	for i in range(DIM_SIZE):
		for j in range(DIM_SIZE):
			lattice[i][j].calcAcc(exForce[i][j]/2)
			lattice[i][j].calcVel(step)
			lattice[i][j].calcPos(step)
			
	for i in range (DIM_SIZE):
		for j in range (DIM_SIZE):
			lattice[i][j].calcPos(step)
			
	print(lattice[0][0].vel[0])
			

#---------------------------------------------------------------------------------#	
DIM_SIZE = 25

lattice = [[None for x in range (DIM_SIZE)]for y in range (DIM_SIZE)]
for i in range (0, DIM_SIZE):
	for j in range (0, DIM_SIZE):
		if i%2 > 0:
			lattice[i][j] = (Atom(1))
		else:
			lattice[i][j] = (Atom(1))
		
lattice[0][0].pos[0] = 1000000
#lattice[0][0].pos[1] = 0.1
lattice[DIM_SIZE-1][DIM_SIZE-1].pos[0] = -1000000
#lattice[DIM_SIZE-1][DIM_SIZE-1].pos[1] = -0.1
#lattice[20][20].pos[0] = -0.1
#lattice[20][20].pos[1] = -0.1


fig = plt.figure()
ax = plt.axes(xlim = (-1, DIM_SIZE), ylim = (-1, DIM_SIZE))
atoms, = ax.plot([], [], 'mo', ms = 5)

#---------------------------------------------------------------------------------#	
#initialising animation#
def init():
	atoms.set_data([], [])
	return atoms,
	
#---------------------------------------------------------------------------------#	
#Run animation#
def animate(i):

	x = []
	y = []
	
	for i in range (0, DIM_SIZE):
		for j in range (0, DIM_SIZE):
			x.append( lattice[i][j].pos[0] + i )
			y.append( lattice[i][j].pos[1] + j )
			
	atoms.set_data(x,y)
	simulateStep(0.01)
	return atoms,
	
anim = animation.FuncAnimation(fig, animate, init_func = init, frames = 100, interval = 1000/60, blit = True)

plt.show()