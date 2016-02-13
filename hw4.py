import numpy as np

def innerProduct(a,b):
	"""
	Takes two vectors a and b, of equal length, and returns their inner product
	"""
	size = a.size

	vectorSum = 0
	#loop through each element of a and b, multipying and adding to sum
	for i in range(size):
		vectorSum+= a[i] * b[i]

	return vectorSum

def AxIP(A,x):
	"""
	Takes a matrix A and a vector x and returns their product
	"""
	#get limiters
	m, n = np.shape(A)
	#make empty zero array to store sums in
	ipVector = np.zeros(m)

	#loop for number of rows in matrix, storing innerProduct
	#in array
	for i in range(m):
		ipVector[i] = innerProduct(A[i,:],x)

	return ipVector



def AxVS(A,x):
	"""
	Takes a matrix A and a vector x and returns their product
	"""

	m, n = np.shape(A)  # m = rows, n = columns
	#make empty zero array to store sums in
	vsVector = np.zeros(m)

	#loop through all columns
	for h in range(n):
		#get matrix column

		vColumn = A[:,h]

		#loop through matrix column adding what is already in vs[i]
		#with product of column * vector
		for i in range(m):
			vsVector[i] = vsVector[i] + vColumn[i] * x[h]

	return vsVector

A = np.array([[.6,.4,.4],[.3,.3,.5],[.1,.3,.1]])
x = np.array([[.5],[.5],[0.]])

print(AxIP(A,x))

# A = np.loadtxt('h4A1.txt')
# x = np.loadtxt('h4x1.txt')
# print(AxIP(A,x))
# print(AxVS(A,x))

# A = np.loadtxt('h4A2.txt')
# x = np.loadtxt('h4x2.txt')
# print(AxIP(A,x))
# print(AxVS(A,x))





