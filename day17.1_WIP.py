
toBottom, width, rocksToPass = 3, 7, 2022 

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
arrows = [letter for directionLine in lines for letter in directionLine]

rocks = [
	[
		[1,1,1]
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

arrow_counter, rock_counter, current_rock = 0, 0, 0

while(rock_counter < rocksToPass):
	bottomReached = False

	if arrows:
		arrow_counter = arrow_counter if arrow_counter < len(arrows) else 0
		current_rock = current_rock if current_rock < len(rocks) else 0

		bottomReached = applyMove(arrows[arrow_counter])
		arrow_counter += 1

	else:
		bottomReached = applyDown()
	
	if bottomReached:
		rock_counter += 1
		current_rock += 1
		
		current_rock
			
