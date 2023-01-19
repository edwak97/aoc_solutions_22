from enum import Enum
import math
import copy
import sys

#sys.setrecursionlimit(2000) dangerous thing

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]

class Squarepath:
	def __init__(self, x:int, y:int, height:int, istop:bool):
		self.branches = set()
		self.height = height
		self.istop = istop
		self.x = x
		self.y = y
		self.distance = 0

squares = [[Squarepath(x = x, y = y, istop = (xval == 'E'), height = (lambda arg: ord('z')-97 if arg == 'E' else (ord(arg)-97))(xval)) for x, xval in enumerate(line)] for y,line in enumerate(lines)]

class Directions (Enum):
	left = lambda x, y: (x-1, y)
	right = lambda x,y: (x+1, y)
	up = lambda x,y: (x, y-1)
	down = lambda x,y: (x, y+1)

bright = len(squares[0]) - 1
bdown = len(lines) - 1
def getdirs(x, y):
	res = set()
	def getsquare(tupl):
		return squares[tupl[1]][tupl[0]]
	if (x < bright) and (squares[y][x+1].height - squares[y][x].height < 2):
		tupl = Directions.right(x, y)
		res.add(getsquare(tupl))
	if (x > 0) and (squares[y][x-1].height - squares[y][x].height < 2):
		tupl = Directions.left(x, y)
		res.add(getsquare(tupl))
	if (y > 0) and (squares[y-1][x].height - squares[y][x].height < 2):
		tupl = Directions.up(x, y)
		res.add(getsquare(tupl))
	if (y < bdown) and (squares[y+1][x].height - squares[y][x].height < 2):
		tupl = Directions.down(x, y)
		res.add(getsquare(tupl))
	
	return res
_x, _y = 0, 0
for y, line in enumerate(squares):
	for x, char in enumerate(line):
		squares[y][x].branches = getdirs(x, y)
		if squares[y][x].istop:
			_x, _y = x, y

for y, line in enumerate(squares):
	for x, char in enumerate(line):
		line[x].distance = round(math.sqrt((_x-x)**2 + (_y-y)**2), 3)
		#print(line[x].distance)
steps_max, steps_max_set = 0, False
way = []

def printPath(way):
	coords = set()
	for el in way:
		print(f'({el.x},  {el.y}) ->', end = ' ')
		tupl = (el.x, el.y)
		coords.add(tupl)
	print('\n- - - -')
	for li in squares:
		_line = ''
		for item in li:
			if (item.x, item.y) in coords:
				_line += '#'
				continue
			if item.x == _x and item.y == _y:
				_line += '@'
				continue
			_line+= ' '
		print(_line)
	sys.stdout.flush()
calls_counter = 0
flag1, flag2 = False, False
def getPathNumbers(steps:int = 1, node = squares[0][0], nodelist = [squares[0][0]]):
		global way, steps_max, steps_max_set, calls_counter, flag1, flag2
		if calls_counter == 10**5:
			printPath(nodelist)
			calls_counter = 0
		else:
			calls_counter += 1
		if steps_max_set and steps == steps_max:
			flag1 = True
			return steps_max
		
		branches_srt = sorted([el for el in node.branches], key = lambda key:key.distance) #alg 1
		#branches_srt = sorted([el for el in node.branches], key = lambda key:key.distance) #alg 2
		for branch in branches_srt:
			if branch.istop:
				steps_max = steps
				steps_max_set = True
				way = copy.copy(nodelist)
				return steps_max
			if branch in nodelist:
				flag2 = True
				continue
			_nodelist = copy.copy(nodelist)
			_nodelist.append(branch)
			
			getPathNumbers(steps = steps+1, node = branch, nodelist = _nodelist)
		return steps_max
print(getPathNumbers())
printPath(way)

