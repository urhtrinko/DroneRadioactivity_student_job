import numpy as np

class TripleVector:
	x = 0
	y = 0
	z = 0

	def __init__(self, x, y, z):
		self.x = float(x)
		self.y = float(y)
		self.z = float(z)

    # String represntation
	def __str__(self):
		return '[%s, %s, %s]' % (self.x, self.y, self.z)

	# Produce a copy of itself
	def __copy(self):
		return TripleVector(self.x, self.y, self.z)

	# Signing
	def __neg__(self):
		return TripleVector(-self.x, -self.y, -self.z)

	# Scalar Multiplication
	def __mul__(self, number):
		return TripleVector(self.x * number, self.y * number, self.z * number)

	def __rmul__(self, number):
		return self.__mul__(number)

	# Division
	def __div__(self, number):
		return self.__copy() * (number**-1)

	# Arithmetic Operations
	def __add__(self, operand):
		return TripleVector(self.x + operand.x, self.y + operand.y, self.z + operand.z)

	def __sub__(self, operand):
		return self.__copy() + -operand

	# Cross product
	# cross = a ** b
	def __pow__(self, operand):
		return TripleVector(self.y*operand.z - self.z*operand.y, 
			                self.z*operand.x - self.x*operand.z, 
			                self.x*operand.y - self.y*operand.x)

	# Dot Project
	# dp = a & b
	def __and__(self, operand):
		return (self.x * operand.x) + \
		       (self.y * operand.y) + \
		       (self.z * operand.z)
 
	# Operations
	def magnitude(self):
		return np.sqrt(self.x**2 + self.y**2 + self.z**2)

	def normal(self):
		return self.__copy().__div__(self.magnitude())
	def dist_2Points(self, operand):
		return (self.__copy() - operand).magnitude()
	
	def compt(self, number):
		if number == 0:
			return self.x
		elif number == 1:
			return self.y
		elif number == 2:
			return self.z

	

ZERO = TripleVector(0,0,0)
vector1 = TripleVector(1, 2, 4)
vector2 = TripleVector(5, 6, 7)
vector3 = vector2.normal()

array = np.array((10, vector1, vector2, vector3))
array2 = np.vstack((array, np.array((11, vector1 + vector2, vector1 + vector3, vector2 + vector3))))

# print(vector3)

# vect1 = TripleVector(1, 1, 1)
# vect2 = TripleVector(2, 2, 1)

# print(vect1.dist_2Points(vect2))

