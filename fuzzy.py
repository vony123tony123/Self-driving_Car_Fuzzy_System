import matplotlib.pyplot as plt
from drawplot import drawPlot
import numpy as np
from toolkit import *


mapfilepath = './map.txt'
def fuzzifier(sensor_distances):
	if sensor_distances[0] < sensor_distances[2]:
		result = [0,0,1]
	elif sensor_distances[0] == sensor_distances[2]:
		result = [0,1,0]
	else:
		result = [1,0,0]
	return np.array(result)

def fuzzy_rule_base(sensor_distances):
	right_minus_left = sensor_distances[2] - sensor_distances[0]
	if right_minus_left <= -5:
		result = [-40,0,0]
	elif right_minus_left >= 5:
		result = [0,0,40]
	else:
		if right_minus_left == 0:
			result = [0,0,0]
		elif right_minus_left < 0:
			result = [8*right_minus_left, 0, 0]
		else:
			result = [0, 0, 8*right_minus_left]
	return np.array(result)

def defuzzier(firing_stregth, result_fuzzies):
	return np.dot(firing_stregth, result_fuzzies) / sum(firing_stregth)

def fuzzy_system(sensor_distances):
	firing_stregth = fuzzifier(sensor_distances)
	result_fuzzies = fuzzy_rule_base(sensor_distances)
	return defuzzier(firing_stregth, result_fuzzies)



def readMapFile(mapFile):
	goal_points = list()
	boarder_points = list()
	with open(mapFile, 'r') as f:
		lines = f.readlines()
		for i,line in enumerate(lines):
			line = list(map(float, line.strip('\n').split(',')))
			if i == 0 :
				original_point = line
			elif i == 1 or i == 2 :
				goal_points.append(line)
			else:
				boarder_points.append(line)
	original_point = np.array(original_point)
	goal_points = np.array(goal_points)
	boarder_points = np.array(boarder_points)
	return original_point, goal_points, boarder_points

if __name__ == "__main__":
	original_point, goal_points, boarder_points = readMapFile(mapfilepath)
	fig, ax = plt.subplots()

	currentPoint = [0,10]
	currentPhi = original_point[-1]
	currentVector = np.array([100, 0])
	sensor_distances = []
	sensor_vectors = drawPlot.getSensorVector(currentVector, currentPhi)

	for sensor_vector in sensor_vectors:
	    cross_point = drawPlot.findCrossPoint(boarder_points, currentPoint, sensor_vector)
	    ax.scatter(cross_point[0], cross_point[1], c=[[0,0,1]])
	    distance = toolkit.euclid_distance(cross_point, currentPoint)
	    ax.text(cross_point[0]-0.5, cross_point[1]+0.5, round(distance,2))
	    sensor_distances.append(distance)

	ax.plot(boarder_points[:,0], boarder_points[:,1])
	ax.add_patch(plt.Rectangle((goal_points[0,0], goal_points[1,1]), 
				  width = goal_points[1,0] - goal_points[0,0], height = goal_points[0,1] - goal_points[1,1]))
	ax.scatter(currentPoint[0], currentPoint[1], c = [[1,0,0]])
	print(sensor_distances)
	print(pipline(sensor_distances))
	plt.show()