import numpy as np
import sys
import matplotlib as mp
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import obj2clist as obj

####################################################
# modify the following 5 functions
# all functions assume homogeneous coordinates in 3D
####################################################
def project(d):
	"""
	returns the projection matrix corresponding to having the viewpoint at (0,0,d)
	and the viewing plane at z=0 (the xy plane).
	"""
	#returns identity matrix but with perspective included
	return np.array([[1.,0.,0.,0.], [0.,1.,0.,0.], [0.,0.,0.,0.], [0.,0.,-1./d,1.]])

def moveTo(start, end):
	"""
	returns the matrix corresponding to moving an obj from position 'start' to position 'end.'
	positions are given in 3D homogeneous coordinates.
	"""
	#calculates distance needed to travel in this instance
	diff = end - start

	#forms transformation matrix based on diff which contains x,y, and z coordinate differences
	return np.array([[1.,0.,0.,diff[0]], [0.,1.,0.,diff[1]], [0.,0.,1., diff[2]], [0.,0.,0.,1.]])


def rotate(x,y,z,loc):
	"""
	returns the matrix corresponding to first rotating a value 'x' around the x-axis,
	then rotating 'y' around the y-axis, and then 'z' around the z-axis.   All angles
	are in radians. The center of rotation is at point given by 'loc' (3D homogeneous coord).
	"""
	#matrix for shifting ball to origin
	shift1 = moveTo(loc, np.array([0.,0.,0.,0.]))

	#rotation matrices given x,y,z radians for each
	xRotation = np.array([[1,0,0,0], [0,np.cos(x),-np.sin(x),0], [0,np.sin(x),np.cos(x),0], [0,0,0,1]])
	yRotation = np.array([[np.cos(y),0,np.sin(y),0], [0,1,0,0], [-np.sin(y),0,np.cos(y),0], [0,0,0,1]])
	zRotation = np.array([[np.cos(z),-np.sin(z),0,0], [np.sin(z),np.cos(z),0,0], [0,0,1,0], [0,0,0,1]])

	fullRotation = np.dot(xRotation,yRotation).dot(zRotation)

	#matrix to shift back to original spot
	shift2 = moveTo(np.array([0.,0.,0.,0.]), loc)

	return np.dot(shift2, fullRotation).dot(shift1)
	

def ballTransform(i,loc):
	"""
	returns the appropriate transformation matrix for the ball.  The center of the ball
	before transformation is given by 'loc'.  The appropriate transformation depends on the
	timestep which is given by 'i'.
	"""
	origLoc = loc.copy()
	newLoc = loc.copy()

	#default projection
	projection = project(100)

	#for i 0-49, move 1/2 foot towards viewer per i and rotate/roll
	if(i >= 0 and i <= 49):
		newLoc[2] = newLoc[2] + .5*i

		#angle== taken from lecture notes
		angle = 2.0 * np.pi * (i/100.0)
		rotation = rotate(angle,0,0,newLoc)

	#for i 50-64, move ball to left 2 feet total and rotate/roll
	elif(i >= 50 and i <= 64):
		#set newLoc to permanent coordinates reflecting
		#transformation done previously
		newLoc[0] = newLoc[0] + -2*(i-50)
		newLoc[2] = newLoc[2] + 24.5

		angle = 2.0 * np.pi * ((i-50)/100.0)
		rotation = rotate(0,0,angle,newLoc)

	#for i 65-149, rotate camera around origin/ball
	elif(i >= 65 and i <= 149):
		#set newLoc to permanent coordinates reflecting
		#transformation done previously
		newLoc[0] = newLoc[0] + -28
		newLoc[2] = newLoc[2] + 24.5

		#calculates radians needed to do one full circle
		angle = ((-2. * np.pi)/84.) * (i - 65)
		rotation = rotate(0,angle,0,np.array([0.,0.,0.,0.]))

		#rotation = rotate() 84 to move 1 whole circle

	translation = moveTo(origLoc, newLoc)
	return np.dot(projection, rotation).dot(translation)

def houseTransform(i,loc):
	"""
	returns the appropriate transformation matrix for the house.  The center of the house
	before transformation is given by 'loc'.  The appropriate transformation depends on the
	timestep which is given by 'i'.
	"""

	#for i 65-149, rotate camera around origin/house
	if(i >= 65 and i <= 149):
		#calculates radians needed to do one full circle
		angle = ((-2. * np.pi)/84.) * (i - 65)
		rotation = rotate(0,angle,0,np.array([0.,0.,0.,0.]))

		return np.dot(project(100),rotation)

	#if not rotating, just return projection matrix
	return project(100)

#######################################
# No need to change any code below here
#######################################
def scale(f):
	"""
	returns a matrix that scales a point by a factor f
	"""
	return(np.array([[f,0.,0,0],[0,f,0,0],[0,0,f,0],[0,0,0,1]]))

# This function implements the animation.  It will be called automatically if you
# run this entire file in the python interpreter.  Or you call call runShow() directly from the
# interpreter prompt if you wish.
def runShow():

	# read house data
	# house is 10*houseScale feet high
	with open('basicHouse.obj','r') as fp:
		house = obj.obj2flist(fp)
	house = obj.homogenize(house)
	houseScale = 3.0
	S = scale(houseScale)
	d = np.array([-5., 4., 3., 1]) - obj.objCenter(house) 
	M = np.array([[1.,0,0,d[0]],[0,1,0,d[1]],[0,0,1,d[2]],[0,0,0,1]])
	house = [S.dot(M).dot(f) for f in house]

	# read ball data
	# ball has radius equal to ballScale feet
	with open('snub_icosidodecahedron.wrl','r') as fp:
		ball = obj.wrl2flist(fp)
	ball = obj.homogenize(ball)
	ballScale = 2.0
	S = scale(ballScale)
	d = np.array([10.0, -0.5, 0., 1]) - obj.objCenter(ball)
	M = np.array([[1.,0,0,d[0]],[0,1,0,d[1]],[0,0,1,d[2]],[0,0,0,1]])
	ball = [S.dot(M).dot(f) for f in ball]

	# set up drawing region
	fig = plt.figure()
	ax = plt.axes(xlim=(-50,50),ylim=(-50,50))
	plt.plot(-40,-40,'')
	plt.plot(40,40,'')
	plt.axis('equal')

	# create drawables
	ballLines = []
	for b in ball:
		ballLines += ax.plot([],[],'b')
	houseLines = []
	for h in house:
		houseLines += ax.plot([],[],'r')

	# this is the drawing routine that will be called on each timestep
	def animate(i):
		M = ballTransform(i,obj.objCenter(ball))
		for b,l in zip(ballLines, ball):
			n = M.dot(l)
			b.set_data(n[0]/n[3],n[1]/n[3])
		M = houseTransform(i,obj.objCenter(house))
		for b,l in zip(houseLines, house):
			n = M.dot(l)
			b.set_data(n[0]/n[3],n[1]/n[3])
		fig.canvas.draw()
		return houseLines,ballLines
	
	# instantiate the animator.
	# we are animating at max rate of 25Hz
	# about the slowest that gives a sense of continuous motion
	# but this will slow down if the scene takes too long to draw
	anim = animation.FuncAnimation(fig, animate, 
									frames=150, interval=1000/25, repeat=False, blit=False)
	plt.show()
	
if __name__ == "__main__":
	runShow()


	
