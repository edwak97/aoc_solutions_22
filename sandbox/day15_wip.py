import copy
import re

y = 10
lines = []
with open('testinput.txt', 'r') as file_origin: 
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
	beacos.append((item[2], item[3]))

coords = [] # lines for y = 10 with no beacons
for plane_object in plane_objects:
	if not (plane_object['down'] <= y <= plane_object['up']):
		continue
	middle_y = plane_object['left'][1]
	x0 = plane_object['left'][0] + abs(middle_y - y)
	x1 = plane_object['right'][0] - abs(middle_y - y)
	coords.append((x0, x1))

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

beacons = [elem for elem in beacons if elem[1] == y]
k = 0
while(k < (len(beacons)):
	_x = beacons[k][0]
	i = 0
	while(i < len(coords)):
		x0, x1 = coords[i][0], coords[i][1]
		if x0 < x < x1:
			coords.append((x0, _x-1))
			coords.append((_x+1, x1))
			del(coords[i])
			continue
		if x0 == x:
			coords
			
print(f'\nFinal:{coords}')
