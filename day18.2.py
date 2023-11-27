lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

directions = {'front', 'back', 'right', 'left', 'up', 'down'}

#data container
xyz_records = {
	(lambda s: (int(s[0]), int(s[1]), int(s[2])))(line.strip().split(','))
	:
	#the side square is not counted by default
	{direction: False for direction in directions}
for line in lines}


# Defining the "box" where the xyz-objects reside
xyzLimits = { 
	 'front': max(xyz_records.keys(), key=lambda val:val[0])[0]+1
	 ,'back': min(xyz_records.keys(), key=lambda val:val[0])[0]-1
	,'right': max(xyz_records.keys(), key=lambda val:val[1])[1]+1
	 ,'left': min(xyz_records.keys(), key=lambda val:val[1])[1]-1
	   ,'up': max(xyz_records.keys(), key=lambda val:val[2])[2]+1
	 ,'down': min(xyz_records.keys(), key=lambda val:val[2])[2]-1
}

#collision handler
collisionPosition = {
	 'front': lambda x,y,z: (x+1,y,z)
	,'back':  lambda x,y,z: (x-1,y,z)
	,'right': lambda x,y,z: (x,y+1,z)
	,'left':  lambda x,y,z: (x,y-1,z)
	,'up':    lambda x,y,z: (x,y,z+1)
	,'down':  lambda x,y,z: (x,y,z-1)
}

def checkXyz(xyz_tuple, side:str):
	if side in {'front','back'}:
		return xyzLimits['back'] <= xyz_tuple[0] <= xyzLimits['front']
	if side in {'right','left'}:
		return xyzLimits['left'] <= xyz_tuple[1] <= xyzLimits['right']
	if side in {'up', 'down'}:
		return xyzLimits['down'] <= xyz_tuple[2] <= xyzLimits['up']

#the structure is the storage of "dots" corresponding to empty space passed
#the idea of this algorithm is to move from outside to inside and to "scan" all the sides available
#begin from any edge of the container

space_front = {(xyzLimits['front'], xyzLimits['right'], xyzLimits['up'])}
space_passed = set()

res = 0

while(space_front):
	
	new_space_front = set()
	for space_bit in space_front:
		x,y,z = space_bit

		for direction in directions:
			#applying "move" toward direction
			moveResult = collisionPosition[direction](x,y,z)
			
			#if the pointer is beyond the limits or the pointer is part of the front or was passed iteration ago then skip
			if not checkXyz(moveResult, direction) or moveResult in space_passed or moveResult in space_front:
				continue

			if moveResult in xyz_records:
				#the side of the cube marked counted
				res += 1
				xyz_records[moveResult][direction] = True
				continue
			
			new_space_front.add(moveResult)
	
	space_passed = set(space_front)
	space_front = set(new_space_front)

print(res)
