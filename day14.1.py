import copy
lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
source_dot = (500, 0)

geo_objects = set()
for line in lines:
	line = line.split(' -> ')
	i = 1
	while i < len(line):
		tupl0 = line[i-1].split(',')
		tupl1 = line[i].split(',')
		tupl0 = (int(tupl0[0]), int(tupl0[1]))
		tupl1 = (int(tupl1[0]), int(tupl1[1]))
		geo_objects.add((tupl0, tupl1))
		i += 1

def dotNextObstacle(dottuple):
	result = None #None means precipice is reached
	# result is a tuple (int, int) that stands for coordinates of the current dot on a clash
	x, y = dottuple[0], dottuple[1]
	
	for geo_object in geo_objects:
		min_x, max_x = min(geo_object[0][0], geo_object[1][0]), max(geo_object[0][0], geo_object[1][0])
		min_y = min(geo_object[0][1], geo_object[1][1])	
		if y < min_y and (min_x <= x <= max_x):
			if (not result):
				result = (x, min_y)
				continue
			if min_y < result[1]:
				result = (x, min_y)
	
	if not result:
		return None #there is no life in the void, only death.

	def checkPositionFilled(_x, _y):
		for geo_object in geo_objects:
			min_x, max_x = min(geo_object[0][0], geo_object[1][0]), max(geo_object[0][0], geo_object[1][0])
			min_y, max_y = min(geo_object[0][1], geo_object[1][1]), max(geo_object[0][1], geo_object[1][1])
			if (min_x <= _x <= max_x) and (min_y <= _y <= max_y):
				return True
		return False
	
	if not checkPositionFilled(x-1, result[1]):
		return dotNextObstacle((x-1, result[1]-1))
	if not checkPositionFilled(x+1, result[1]):
		return dotNextObstacle((x+1, result[1]-1))
	return result

new_objects = []
while True:
	taken = dotNextObstacle(source_dot)
	if taken:
		newitem = (taken[0], taken[1]-1)
		geo_objects.add((newitem, newitem))
		new_objects.append(newitem)
		i+=1
		continue
	break
print(len(new_objects))
