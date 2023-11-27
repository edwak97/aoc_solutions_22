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
	 'front': max(xyz_records.keys(), key=lambda val:val[0])[0]
	 ,'back': min(xyz_records.keys(), key=lambda val:val[0])[0]
	,'right': max(xyz_records.keys(), key=lambda val:val[1])[1]
	 ,'left': min(xyz_records.keys(), key=lambda val:val[1])[1]
	   ,'up': max(xyz_records.keys(), key=lambda val:val[2])[2]
	 ,'down': min(xyz_records.keys(), key=lambda val:val[2])[2]
}

print(xyzLimits)

#collision handler
collisionPosition = {
	 'front': lambda x,y,z: (x+1,y,z)
	,'back':  lambda x,y,z: (x-1,y,z)
	,'right': lambda x,y,z: (x,y+1,z)
	,'left':  lambda x,y,z: (x,y-1,z)
	,'up':    lambda x,y,z: (x,y,z+1)
	,'down':  lambda x,y,z: (x,y,z-1)
}

pairs = {
	 'right': 'left'
	,'front': 'back'
	 ,'back': 'front'
	 ,'left': 'right'
	 ,'down': 'up'
	   ,'up': 'down'
}

def checkXyz(xyz_tuple, side:str):
	if side in {'front','back'}:
		return xyzLimits['back']-1 <= xyz_tuple[0] <= xyzLimits['front']+1
	if side in {'right','left'}:
		return xyzLimits['left']-1 <= xyz_tuple[1] <= xyzLimits['right']+1
	if side in {'up', 'down'}:
		return xyzLimits['down']-1 <= xyz_tuple[2] <= xyzLimits['up']+1

