import sys
import re

lines = []

with open('test_input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

lines = [line.strip('\n') for line in lines]

steps = lines.pop()

steps = re.findall(r'L|R|\d+', steps)

def getXY(y_val, x_val, positions, final_form, side_name):
	
	step = final_form['step']

	_y,_x = y_val//step,x_val//step

	side_description = final_form['form'][(_y,_x)][side_name]

	new_y,new_x = side_description['yx']
	side = side_description['side']
	reverse = side_description['reverse']
	
	y,x = new_y*step,new_x*step
	
	delta = (x_val % step) if side_name in {'up','down'} else (y_val % step)
	
	if side in {'up','down'}:
		x = (x+step-1-delta) if reverse else (x+delta)
		y = y if side == 'up' else (y+step-1)
	elif side in {'left','right'}:
		y = (y+step-1-delta) if reverse else (y+delta)
		x = x if side == 'left' else (x+step-1)
	
	return (y,x) if positions[(y,x)] else None

def obtainDescription(y_val:int, x_val:int, positions, max_val_y, max_val_x, final_form):
	
	result = dict()

	min_x,max_x = max_val_x[y_val]
	min_y,max_y = max_val_y[x_val]
	
	args = [y_val,x_val,positions,final_form]

	if y_val+1 > max_y and (coords:=getXY(*(args+['down']))):
		result['down'] = coords
	elif y_val+1 <= max_y and positions[(coords:=(y_val+1,x_val))]:
		result['down'] = coords
	
	if y_val-1 < min_y and (coords:=getXY(*(args+['up']))):
		result['up'] = coords
	elif y_val-1 >= min_y and positions[(coords:=(y_val-1,x_val))]:
		result['up'] = coords

	if x_val+1 > max_x and (coords:=getXY(*(args+['right']))):
		result['right'] = coords
	elif x_val+1 <= max_x and positions[(coords:=(y_val,x_val+1))]:
		result['right'] = coords

	if x_val-1 < min_x and (coords:=getXY(*(args+['left']))):
		result['left'] = coords
	elif x_val-1 >= min_x and positions[(coords:=(y_val,x_val-1))]:
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
	
	return {'step':step,'form':result}

def buildForm(form):
	return {
		'step':4,
		'form':{
			(0,2):{
				'left':   {'yx':(1,1),'side':'up',   'reverse':False}
				,'up':    {'yx':(1,0),'side':'up',   'reverse':True}
				,'right': {'yx':(2,3),'side':'right','reverse':True}
		#no key 'down' because the movement is supposed to happen in the "natural" direction
			},
			(1,0):{
				'up':    {'yx':(0,2),'side':'up',   'reverse':True}
				,'down': {'yx':(2,2),'side':'down', 'reverse':True}
				,'left': {'yx':(2,3),'side':'down', 'reverse':True}
			},
			(1,1):{
				'up':    {'yx':(0,2),'side':'left', 'reverse':False}
				,'down': {'yx':(2,2),'side':'left', 'reverse':True}
			},
			(1,2):{
				'right': {'yx':(2,3),'side':'up',   'reverse':True}
			},
			(2,2):{
				'left':  {'yx':(1,1),'side':'down','reverse':True}
				,'down': {'yx':(1,0),'side':'down','reverse':True}
			},
			(2,3):{
				'up':     {'yx':(1,2),'side':'right','reverse':True}
				,'right': {'yx':(0,2),'side':'right','reverse':True}
				,'down':  {'yx':(1,0),'side':'left', 'reverse':True}
			}
		}
	}

def changeDirection(LR:str, base_direction:str):
	
	base_direction = clockwise[base_direction]
	new_direction = None

	if LR == 'R':
		new_direction = (base_direction+1)%4
	if LR == 'L':
		new_direction = (base_direction-1)%4
	
	return _clockwise[new_direction]

def tryMove(direction, pos, step, positions, final_form):
	
	if step == 0:
		return (direction,pos)
	
	description = positions[pos]
	next_pos = description.get(direction)

	#if the movement is not possible
	if not next_pos:
		return (direction,pos)

	#checking if this direction has been ALTERED when jumping to the NEW SIDE
	y,x = pos
	_y,_x = next_pos
	f = {(y-1,x),(y,x+1),(y+1,x),(y,x-1)}
	
	new_direction = direction

	if next_pos not in f:
	#need to define NEW direction after crossing the border
		y_f, x_f = y//final_form['step'], x//final_form['step']
		
		#where new side is:
		last_direction = final_form['form'][(y_f,x_f)][direction]['side']
		opposed = {'up':'down','down':'up','left':'right','right':'left'}
		
		new_direction = opposed[last_direction]
	
	#print(next_pos)
	return tryMove(new_direction, next_pos, step-1, positions, final_form)

positions = {(line_number,char_position):char!='#' for line_number,line in enumerate(lines) for char_position,char in enumerate(line) if char != ' '}

edge_values_x = {y_val:(lambda lst: (min(lst),max(lst)))({x for (y,x) in positions if y==y_val}) for y_val in {y for (y,_) in positions}}
edge_values_y = {x_val:(lambda lst: (min(lst),max(lst)))({y for (y,x) in positions if x==x_val}) for x_val in {x for (_,x) in positions}}

form = getForm(edge_values_x, edge_values_y)

final_form = buildForm(form)

positions = {(y,x):obtainDescription(y,x,positions,edge_values_y,edge_values_x,final_form) for (y,x) in positions if positions[(y,x)]}

init_direction = 'right'
init_position = (0,min([x for (y,x) in positions if y==0]))

for i,step in enumerate(steps):
	if i%2==0:
		init_direction,init_position = tryMove(init_direction, init_position, int(step), positions, final_form)
		continue
	init_direction = changeDirection(step,init_direction)

row,column = init_position
print(positions[(5,11)])
print(row,' ',column)
print((row+1)*1000 + (column+1)*4 + clockwise[init_direction])
