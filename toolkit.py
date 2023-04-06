import numpy as np

class toolkit:
	def rotation_matrix(angle):
		theta = np.radians(angle)
		c, s = np.cos(theta), np.sin(theta)
		rotation_matrix = np.array([[c ,-s], [s, c]])
		return rotation_matrix


	# calculate cross point between vector and horizontal line 
	def calculate_crossPoint_in_horizontalLine(point, vector, y_value):
		if vector[1] == 0:
			return False
		time_of_vector = (y_value - point[1]) / vector[1]
		if time_of_vector < 0:
			return False
		x = vector[0] * time_of_vector + point[0]
		return [x, y_value]

	# calculate cross point between vector and vertical line 
	def calculate_crossPoint_in_verticalLine(point, vector, x_value):
		if vector[0] == 0:
			return False
		time_of_vector = (x_value - point[0]) / vector[0]
		if time_of_vector < 0:
			return False
		y = vector[1] * time_of_vector + point[1]
		return [x_value, y]


	# x = 1 dim matrix
	# m = 1 dim matrix
	# return scalar
	def euclid_distance(x, m):
	    distance = np.linalg.norm(x-m, axis=-1)
	    return distance

	# x = 2 dim matrix
	# m = 2 dim matrix
	# return 2 dim matrix
	def euclid_distance_2d(x, m):
	    x_minus_m_seperate = list(map(lambda a: a-m, x))
	    distance = np.linalg.norm(x_minus_m_seperate, axis=-1)
	    return distance


