import copy
lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
geo_objects = set()
bottom, min_x, max_x = None, None, None
for line in lines:
	line = line.split(' -> ')
	i = 1
	while i < len(line):
		tupl0 = line[i-1].split(',')
		tupl1 = line[i].split(',')
		i += 1
		tupl0 = (int(tupl0[0]), int(tupl0[1]))
		tupl1 = (int(tupl1[0]), int(tupl1[1]))
		geo_objects.add((tupl0, tupl1))
		temp_bottom = max(tupl0[1], tupl1[1])
		temp_min_x, temp_max_x = min(tupl0[0], tupl1[0]), max(tupl0[0], tupl1[0])
		if bottom:
			if temp_bottom > bottom:
				bottom = temp_bottom
		else:
			bottom = temp_bottom
		if min_x:
			if temp_min_x < min_x:
				min_x = temp_min_x
		else:
			min_x = temp_min_x
		if max_x:
			if temp_max_x > max_x:
				max_x = temp_max_x
		else:
			max_x = temp_max_x
bottom += 2
piles = {}

def initPileX(x):
	piles[x] = [False for i in range(0, bottom + 1)]
	piles[x][bottom] = True # True means blocked

for geo_object in geo_objects:
	x0, y0 = min(geo_object[0][0], geo_object[1][0]), min(geo_object[0][1], geo_object[1][1])
	x1, y1 = max(geo_object[0][0], geo_object[1][0]), max(geo_object[0][1], geo_object[1][1])
	if x0 == x1:
		if not (x0 in piles):
			initPileX(x0)
		for i in range(y0, y1+1):
			piles[x0][i] = True
		continue
	#if y0 == y1
	for i in range(x0, x1+1):
		if not (i in piles):
			initPileX(i)
		piles[i][y0] = True

def getObstacleXY(dottuple):
	x, y = dottuple[0], dottuple[1]
	y += 1
	while(not piles[x][y]):
		y += 1
	def checkXYblocked(_x, _y):
		if not (_x in piles):
			initPileX(_x)
		return piles[_x][_y]
	if not checkXYblocked(x-1, y):
		return getObstacleXY((x-1, y-1))
	if not checkXYblocked(x+1, y):
		return getObstacleXY((x+1, y-1))
	piles[x][y-1] = True
	return

counter = 0
while(True):
	getObstacleXY((500, 0))
	counter += 1
	if piles[500][0]:
		break
print(counter)
 
