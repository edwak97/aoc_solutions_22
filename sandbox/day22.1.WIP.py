import sys

lines = []

with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

lines = [line.strip('\n') for line in lines]
steps = lines.pop()

def obtainDescription(y_val:int, x_val:int, positions):
	
	x_vals = [x for (y,x) in positions if y == y_val]
	y_vals = [y for (y,x) in positions if x == x_val]

	min_x,max_x = min(x_vals),max(x_vals)
	min_y,max_y = min(y_vals),max(y_vals)
	
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

positions = {(line_number,char_position):char!='#' for line_number,line in enumerate(lines) for char_position,char in enumerate(line) if char != ' '}

positions = {(y,x):obtainDescription(y,x,positions) for (y,x) in positions if positions[(y,x)]}


