from enum import Enum
import math
import copy
import sys

lines = []
with open('testinput.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]

class Squarepath:
	def __init__(self, x:int, y:int, height:int, istop:bool, isentrance:bool):
		self.branches = None #yet to be initialized
		self.height = height
		self.istop = istop
		self.isentrance = isentrance
		self.x = x
		self.y = y
		self.distance = 0

squares = [[Squarepath(x = x, y = y, isentrance = (xval == 'S'), istop = (xval == 'E'), height = (lambda arg: ord('z')-97 if arg == 'E' else (ord('a')-97 if arg == 'S' else ord(arg)-97 ))(xval)) for x, xval in enumerate(line)] for y,line in enumerate(lines)]

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

entrance = [elem for line in squares for elem in line if elem.isentrance][0]
for y, line in enumerate(squares):
	for x, char in enumerate(line):
		squares[y][x].branches = getdirs(x, y)
print(entrance.x, ' ', entrance.y)
steps_max = 0
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
			if item.istop:
				_line += '@'
				continue
			_line+= ' '
		print(_line)
	sys.stdout.flush()
calls_counter = 0

def getPathNumbers(steps:int = 1, node = entrance, nodelist = [entrance]):
		global way, steps_max, calls_counter
		if calls_counter == 10**5:
			printPath(nodelist)
			print(flag1, ' ', flag2)
			calls_counter = 0
		else:
			calls_counter += 1
		if steps == steps_max:
			return steps_max
		
		for branch in node.branches:
			if branch.istop:
				steps_max = steps
				way = copy.copy(nodelist)
				return steps_max
			if branch in nodelist:
				continue
			_nodelist = copy.copy(nodelist)
			_nodelist.append(branch)
			getPathNumbers(steps = steps+1, node = branch, nodelist = _nodelist)
		return steps_max
print(getPathNumbers())
printPath(way)

