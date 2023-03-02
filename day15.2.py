import re

x_limit, y_limit = 4000000, 4000000

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
sensbeac = []
for line in lines:
	numbers = re.findall(fr'-*\d+', line)
	numbers = [int(number) for number in numbers]
	sensbeac.append(numbers)

plane_objects = []
beacons = []

for item in sensbeac:
	steps = abs(item[0]-item[2]) + abs(item[1]-item[3])
	left = (item[0]-steps, item[1])
	right = (item[0]+steps, item[1])
	down = (item[0], item[1]-steps)
	up = (item[0], item[1]+steps)
	plane_object = {'left': left, 'right': right, 'up': up, 'down': down}
	plane_objects.append(plane_object)
	
	beacons.append((item[2], item[3])) #(x, y) of a beacon

def getNoBeaconsIntervals(y = 10):
		coords = [] # lines for y with no beacons taken into consideration
		for plane_object in plane_objects:
			if not (plane_object['down'][1] <= y <= plane_object['up'][1]):
				continue
			middle_y = plane_object['left'][1]
			x0 = plane_object['left'][0] + abs(middle_y - y)
			x1 = plane_object['right'][0] - abs(middle_y - y)
			coords.append((x0, x1)) # inte
		#Merjing intervals to exclude overlaping effect
		k = 0
		while(k < len(coords)):
			x0, x1 = coords[k][0], coords[k][1]
			i = k+1
			merged = False
			while(i < len(coords)):
				xi0, xi1 = coords[i][0], coords[i][1]
				if (xi0 <= x0 <= xi1) or (xi0 <= x1 <= xi1) or (x0 <= xi0 <= x1) or (x0 <= xi1 <= x1):
					x0, x1 = min(x0, xi0), max(x1, xi1)
					coords[i] = (x0, x1)
					del(coords[k])
					merged = True
					break
				i += 1
			if not merged:
				k += 1
		_beacons = [elem for elem in beacons if elem[1] == y]
		k = 0
		while(k < len(_beacons)):
			_x = _beacons[k][0]
			i = 0
			while(i < len(coords)):
				x0, x1 = coords[i][0], coords[i][1]
				if x0 < _x < x1:
					coords.append((x0, _x-1))
					coords.append((_x+1, x1))
					del(coords[i])
					continue
				if x0 == x1 == _x:
					del(coords[i])
					continue
				if _x == x0:
					coords.append((_x+1, x1))
					del(coords[i])
					continue
				if _x == x1:
					coords.append((x0, _x-1))
					del(coords[i])
					continue
				i += 1
			k += 1

		return coords
for i in range(0, y_limit+1):
	intervals = getNoBeaconsIntervals(i)
	intervals = sorted(intervals, key = lambda x:x[0])
	if len(intervals) > 1:
		k = 1
		while(k < len(intervals)):
			x_after = intervals[k][0]-1
			x_pre = intervals[k-1][1]+1
			if (x_pre == x_after) and (0 <= x_pre <= x_limit) and not ((x_after,i) in beacons):
				signal = x_after*y_limit + i
				print(f'Distress signal: {signal}') 
			k += 1
