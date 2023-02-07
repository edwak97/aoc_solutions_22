import copy
lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
source_dot = (500, 0)
testlines = [
	'498,4 -> 498,6 -> 496,6',
	'503,4 -> 502,4 -> 502,9 -> 494,9'
	]
geo_objects = set()
for line in testlines:
	line = line.split(' -> ')
	i = 1
	while i < len(line):
		tupl0 = line[i-1].split(',')
		tupl1 = line[i].split(',')
		tupl0 = (int(tupl0[0]), int(tupl0[1]))
		tupl1 = (int(tupl1[0]), int(tupl1[1]))
		geo_objects.add((tupl0, tupl1))
		i += 1

def dotNextPosition(dottuple):
	objects_below = []
	x, y = dottuple[0], dottuple[1]
	next_object = None

	def compareGeoY(geo_object1, geo_object2):
		if not geo_object2:
			return True
		left_sign = geo_object1[1] if type(geo_object1[1]) == int else geo_object[0][1]
		right_sign = geo_object2[1] if type(geo_object2[1]) == int else geo_object2[0][1]
		return left_sign < right_sign

	for geo_object in geo_objects:
		if type(geo_object[0]) == int: #If we deal with a dot
			if (geo_object[0] != x) or (y > geo_objects[1]):
				continue
			if compareGeoY(geo_object, next_object):
				next_object = geo_object
			continue
		#If we deal with a line
		x0, y0, x1, y1 = geo_object[0][0], geo_object[0][1], geo_object[1][0], geo_object[1][1]
		if (y < y0) and ((x == x0 == x1) or (x0 <= x <= x1)):
			if compareGeoY(geo_object, next_object):
				next_object = geo_object
print(straight_lines)
