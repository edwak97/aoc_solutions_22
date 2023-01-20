from enum import Enum
import math
import copy
import sys

lines = []
with open('input.txt', 'r') as file_origin: 
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
		self.score = None

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


for y, line in enumerate(squares):
	for x, char in enumerate(line):
		squares[y][x].branches = getdirs(x, y)

entrance = [elem for line in squares for elem in line if elem.isentrance][0]
entrance.score = 0
deep = 1
def getPathNumber(steps:int = 1, nodelist = [entrance]):
		newnodelist = []
		for node in nodelist:
			for branch in node.branches:
				if branch.istop:
					return steps
				if branch.score == None:
					branch.score = steps
					newnodelist.append(branch)
		return getPathNumber(steps + 1, nodelist = newnodelist)
print(getPathNumber())

