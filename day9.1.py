import math
lines = []
testlines = [
	'R 4',
	'U 4',
	'L 3',
	'D 1',
	'R 4',
	'D 1',
	'L 5',
	'R 2',
	]
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x: (x[0],int(x[1])))((line.strip()).split(' ')) for line in lines]
maxdiff = math.sqrt(2)
positions = {(0,0)}
pT, pH =(0,0), (0,0)
for pair in lines:
	switch = {
		'U': lambda arg: (arg[0],  arg[1]+1),
		'D': lambda arg: (arg[0],  arg[1]-1),
		'R': lambda arg: (arg[0]+1,arg[1]),
		'L': lambda arg: (arg[0]-1,arg[1])
		}
	move, i = switch.get(pair[0]), pair[1]
	print('\n')
	while i > 0:
		nH = move(pH)
		
		delta:float = math.sqrt((nH[0]-pT[0])**2 + (nH[1]-pT[1])**2)
		print (f'Head moves {pair[0]}\ndelta = {delta}')
		if delta > maxdiff:
			pT = move(pT)
			if ((nH[0] != pT[0]) and (nH[1] != pT[1])):
				move2 = None
				if pair[0] in {'R','L'}:
					move2 = switch['U'] if nH[1] > pT[1] else switch['D']
				else:
					move2 = switch['R'] if nH[0] > pT[0] else switch['L']
				pT = move2(pT)
			print(f'T position changed to {pT}')
			positions.add(pT)
		pH = nH
		i-=1
print(len(positions))


'''
........
........
........
........
........
'''
