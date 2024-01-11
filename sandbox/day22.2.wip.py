import sys
import re

lines = []

with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

lines = [line.strip('\n') for line in lines]

steps = lines.pop()

steps = re.findall(r'L|R|\d+', steps)

def obtainDescription(y_val:int, x_val:int, positions, max_val_y, max_val_x, form):
	min_x,max_x = max_val_x[y_val]
	min_y,max_y = max_val_y[x_val]

	result = dict()
	
	if y_val+1 > max_y and positions[(coords:=(min_y,x_val))]:
		result['down'] = coords
	if y_val+1 <= max_y and positions[(coords:=(y_val+1,x_val))]:
		result['down'] = coords
	
	if y_val-1 < min_y and positions[(coords:=(max_y,x_val))]:
		result['up'] = coords
	if y_val-1 >= min_y and positions[(coords:=(y_val-1,x_val))]:
		result['up'] = coords

	if x_val+1 > max_x and positions[(coords:=(y_val,min_x))]:
		result['right'] = coords
	if x_val+1 <= max_x and positions[(coords:=(y_val,x_val+1))]:
		result['right'] = coords

	if x_val-1 < min_x and positions[(coords:=(y_val,max_x))]:
		result['left'] = coords
	if x_val-1 >= min_x and positions[(coords:=(y_val,x_val-1))]:
		result['left'] = coords
	
	return result

clockwise =  {'right':0,'down':1,'left':2,'up':3}
_clockwise = {0:'right',1:'down',2:'left',3:'up'}

def getForm(edge_values_x, edge_values_y):
	
	edge_values_x = [edge_values_x[k] for k in edge_values_x]
	vals_x_gaps   = [abs(a-b) for (a,b) in edge_values_x]
	step          = min(vals_x_gaps)+1
	
	mask = {(y//step,x//step):(x>=edge_values_x[y][0]) for y in range(0,len(vals_x_gaps),step) for x in range(0,edge_values_x[y][1],step)}

	for i in range(0,len(vals_x_gaps),step):
		fro,to = edge_values_x[i]
		print(f"{' '*((fro)//step)}{((to-fro+1)//step)*'#'}")
	
	result = dict()
		
	for item in mask:
		
		if not mask[item]:
			continue
		
		y,x = item
		f = {'up':(y-1,x),'right':(y,x+1),'down':(y+1,x),'left':(y,x-1)}
		
		result[item] = dict()

		for k in f:
			if (mask.get(f[k])):
				result[item][k] = f[k]

	return result

def changeDirection(LR:str, base_direction:str):
	base_direction = clockwise[base_direction]
	new_direction = None

	if LR == 'R':
		new_direction = (base_direction+1)%4
	if LR == 'L':
		new_direction = (base_direction-1)%4
	
	return _clockwise[new_direction]

def tryMove(direction, pos, step, positions):
	if step == 0:
		return pos
	description = positions[pos]
	return tryMove(direction, next_pos, step-1,positions) if (next_pos:=description.get(direction)) else pos

positions = {(line_number,char_position):char!='#' for line_number,line in enumerate(lines) for char_position,char in enumerate(line) if char != ' '}

edge_values_x = {y_val:(lambda lst: (min(lst),max(lst)))({x for (y,x) in positions if y==y_val}) for y_val in {y for (y,_) in positions}}
edge_values_y = {x_val:(lambda lst: (min(lst),max(lst)))({y for (y,x) in positions if x==x_val}) for x_val in {x for (_,x) in positions}}

form = getForm(edge_values_x, edge_values_y)
print(form)
positions = {(y,x):obtainDescription(y,x,positions,edge_values_y,edge_values_x,form) for (y,x) in positions if positions[(y,x)]}

init_direction = 'right'
init_position = (0,min([x for (y,x) in positions if y==0]))

for i,step in enumerate(steps):
	if i%2==0:
		init_position = tryMove(init_direction, init_position, int(step), positions)
		continue
	init_direction = changeDirection(step,init_direction)

row,column = init_position

print((row+1)*1000 + (column+1)*4 + clockwise[init_direction])
