import sys
import re
import copy

lines = []
with open('test_input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

lines = [line.strip('\n') for line in lines]

steps = lines.pop()

steps = re.findall(r'L|R|\d+', steps)

clockwise =  {'right':0,'down':1,'left':2,'up':3}
_clockwise = {0:'right',1:'down',2:'left',3:'up'}


def getXY(y_val, x_val, positions, final_form, side_name):
	
	step = final_form['step']

	_y,_x = y_val//step,x_val//step

	side_description = final_form['body'][(_y,_x)][side_name]

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
		f = {(y-1,x):'up', (y,x+1):'right', (y+1,x):'down', (y,x-1):'left'}
		
		result[item] = {
			'directions': {yx:f[yx] for yx in f if mask.get(yx)}
			,'sides_coordinates':{'up':((0,y,x),(0,y,x+1)),'right':((0,y,x+1),(0,y+1,x+1)),'down':((0,y+1,x),(0,y+1,x+1)),'left':((0,y,x),(0,y+1,x))}
		}
	
	return {'step':step,'body':result}


def rotateSides(map_to_fold, side_to_rotate, axis_coords, center, were_rotated):
	
	((rz0, ry0, rx0),(rz1,ry1,rx1)) = axis_coords
	
	for direction in map_to_fold[side_to_rotate]['sides_coordinates']:
		
		((z0,y0,x0),(z1,y1,x1)) = map_to_fold[side_to_rotate]['sides_coordinates'][direction]
		
		if rz0 != rz1:
			_z0,_z1 = z0,z1
			pass
		elif ry0 != ry1:
			_y0,_y1 = y0,y1
			pass
		elif rx0 != rx1:
			_x0,_x1 = x0,x1
			pass

		map_to_fold[side_to_rotate['side_coordinates'][direction] = ((_z0,_y0,_x0),(_z1,_y1,_x1))
	were_rotated.add(side_to_rotate)

	for _side in map_to_fold[side]['directions']
		
		if _side in rotated:
			continue
		rotateSides(map_to_fold, _side, around_side, boundary_name, center, were_rotated)


def fold(map_to_fold, base=None, were_passed = set(), center = None):

	if not base:
		base = list(map_to_fold.keys())[0] #base = (0,1)	

	 if not center:
		y,x = base
		center = (0.5, y+0.5, x+0.5)
	
	were_passed.add(base)
	
	for side in map_to_fold[base]['directions']:
		if side in were_passed:
			continue

		boundary_name = map_to_fold[base]['directions'][side]
		
		axis_coords = map_to_fold[base]['sides_coordinates'][boundary_name]

		rotateSides(map_to_fold, side, axis_coords, center, copy.copy(were_passed))

		fold(map_to_fold, side, were_passed, center)

#this is what obtainDescription needs to build the final map properly:

'''
	return {
		'step':50,
		'body':{
			(0,1):{
				'left':   {'yx':(2,0),'side':'left','reverse':True}
				,'up': {'yx':(3,0),'side':'left','reverse':False}
		#no key 'down' because the movement is supposed to happen in the "natural" direction
			},
			(0,2):{
				'up':    {'yx':(3,0),'side':'down',   'reverse':False}
				,'down': {'yx':(1,1),'side':'right', 'reverse':False}
				,'right': {'yx':(2,1),'side':'right', 'reverse':True}
			},
			(1,1):{
				'right':    {'yx':(0,2),'side':'down', 'reverse':False}
				,'left': {'yx':(2,0),'side':'up', 'reverse':False}
			},
			(2,0):{				'up': {'yx':(1,1),'side':'left',   'reverse':False}
				,'left':{'yx':(0,1),'side':'left', 'reverse':True}
			},
			(2,1):{
				'right':  {'yx':(0,2),'side':'right','reverse':True}
				,'down': {'yx':(3,0),'side':'right','reverse':False}
			},
			(3,0):{
				'left':     {'yx':(0,1),'side':'up','reverse':False}
				,'right': {'yx':(2,1),'side':'down','reverse':False}
				,'down':  {'yx':(0,2),'side':'up','reverse':False}
			}
		}
	}
'''

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
		last_direction = final_form['body'][(y_f,x_f)][direction]['side']
		opposed = {'up':'down','down':'up','left':'right','right':'left'}
		
		new_direction = opposed[last_direction]

	return tryMove(new_direction, next_pos, step-1, positions, final_form)

positions = {(line_number,char_position):char!='#' for line_number,line in enumerate(lines) for char_position,char in enumerate(line) if char != ' '}

edge_values_x = {y_val:(lambda lst: (min(lst),max(lst)))({x for (y,x) in positions if y==y_val}) for y_val in {y for (y,_) in positions}}
edge_values_y = {x_val:(lambda lst: (min(lst),max(lst)))({y for (y,x) in positions if x==x_val}) for x_val in {x for (_,x) in positions}}

form = getForm(edge_values_x, edge_values_y)

print(form)

sys.exit()

fold(form['body'])

print(form)
sys.exit()

positions = {(y,x):obtainDescription(y,x,positions,edge_values_y,edge_values_x, form) for (y,x) in positions if positions[(y,x)]}

init_direction = 'right'
init_position = (0,min([x for (y,x) in positions if y==0]))

for i,step in enumerate(steps):
	if i%2==0:
		init_direction,init_position = tryMove(init_direction, init_position, int(step), positions, form)
		continue
	init_direction = changeDirection(step,init_direction)

row,column = init_position

print((row+1)*1000 + (column+1)*4 + clockwise[init_direction])
