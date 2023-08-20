
toBottom, toLeft, width, rocksToPass = 3, 2, 7, 2022

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
arrows = [letter for directionLine in lines for letter in directionLine]

rocks = [
	[
		[1,1,1,1]
	],
	[
		[0,1],
		[1,1,1],
		[0,1]
	],
	[
		[0,0,1],
		[0,0,1],
		[1,1,1]
	],
	[
		[1],
		[1],
		[1],
		[1]
	],
	[
		[1,1],
		[1,1]
	]
]

#baseState
rel_rock, rock_counter, currentRockIndex, currentRockState = 0, 0, -1, None

currentBundle = None

state = [[1 for x in range(width)]]

def arrow_handler():
	arrow_counter = 0
	while(True):
		if arrow_counter == len(arrows):
			arrow_counter = 0
		yield (arrows[arrow_counter], arrow_counter)
		arrow_counter += 1

#removing empty height except for $toBottom given by initial data
def shortenSpace():
	global state
	i = len(state) - 1
	while(True):
		rockFoundInLine = False
		for item in state[i]:
			if item:
				rockFoundInLine = True
				break
		#there is always 1-1-1-1-1-1-1 line on the bottom
		if rockFoundInLine:
			break
		del(state[i])
		i -= 1
	state += [[0 for x in range(width)] for y in range(toBottom)]

def initRockAppear():
	global currentRockState
	global currentRockIndex
	global state
	shortenSpace()

	currentRockIndex = currentRockIndex+1 if currentRockIndex+1 < len(rocks) else 0
	
	rock_height = len(rocks[currentRockIndex])
	#getting initial rock coordinates
	currentRockState = set()
	i = rock_height-1
	while(i > -1):
		for width_index,width_rock in enumerate(rocks[currentRockIndex][i]):
			if width_rock:
				currentRockState.add((width_index+toLeft, len(state) + rock_height-i-1))
		i -= 1
	
	#addingEmptySpace where the rock resides in
	state = state + [[0 for x in range(width)] for y in range(rock_height)]


#return True if bottom reached
def applyDown():
	global state
	global currentRockState
	bottomReached = False

	for elem in currentRockState:
		if state[elem[1]-1][elem[0]]:
			bottomReached = True
			break

	if not bottomReached:
		currentRockState = set(map(lambda x: (x[0], x[1]-1), currentRockState))
		return False
	
	#the rock is saved into the state
	for elem in currentRockState:
		state[elem[1]][elem[0]] = 1
	return True

#return True if bottom reached
def applyArrow(arrow: str):
	global currentRockState
	collision = False
	
	moveByArrow = (lambda x: (x[0]-1, x[1])) if arrow == '<' else (lambda x:(x[0]+1, x[1]))
	
	for elem in currentRockState:
		elem = moveByArrow(elem)
		if elem[0] < 0 or elem[0] == width or state[elem[1]][elem[0]]:
			collision = True
			break
	if not collision:
		currentRockState = set(map(moveByArrow, currentRockState))
	return applyDown()

def saveRockToCurrentBundle(arrow: int):
	global currentBundle

	if not currentBundle:
		delta_y = -min([item[1] for item in currentRockState])
		x = min([item[0] for item in currentRockState])
		currentBundle = {'delta_y': delta_y, 'arrow': arrow, 'rocks_state': (x,)}
		return
	
	y = min([item[1] for item in currentRockState])+currentBundle['delta_y']
	x = min([item[0] for item in currentRockState])
	
	currentBundle['rocks_state'] += (x, y)

bundleStorage = set()
arrow = arrow_handler()
initRockAppear()
found = False
while(True):
	
	current_arrow = next(arrow)
	#if bottom has been reached
	if applyArrow(current_arrow[0]):
		saveRockToCurrentBundle(current_arrow[1])
		if rel_rock == len(rocks)-1:		
			#comparing this bundle of (0-1-2-3)_n rock combination with other saved bundles
			if (currentBundle['arrow'], currentBundle['rocks_state']) in bundleStorage:
				print(rock_counter)
			else:
				bundleStorage.add((currentBundle['arrow'], currentBundle['rocks_state']))
			currentBundle = None
		rock_counter += 1
		rel_rock += 1
		rel_rock = 0 if rel_rock == len(rocks) else rel_rock
		if(rock_counter < rocksToPass):
			initRockAppear()
			continue
		break
shortenSpace()
print('\nresult: ',len(state)-toBottom-1)

