lines = []
import re
import sys

with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

def obtainDescription(line:str):
	rgx = re.compile(r'\s*(\w+)\s*:\s*(\d+|(\w+)\s*([-/+*]){1}\s*(\w+))')
	formula_items = rgx.findall(line)
	#print(formula_items)
	if not formula_items[0][4]:
		return (formula_items[0][0], lambda : int(formula_items[0][1]), [])
	return (formula_items[0][0], eval(f'lambda x,y: x {formula_items[0][3]} y'), [formula_items[0][2], formula_items[0][4]])
monkeys = {monkey:{'func':func,'args':args} for (monkey,func,args) in [obtainDescription(line) for line in lines]}

def evaluate(monkey_name:str):
	args = [evaluate(item) for item in monkeys[monkey_name]['args']]
	return monkeys[monkey_name]['func'](*args)

def sign(val):
	return -1 if val < 0 else 1

def obtainVariable(var_history, diff_history, boundary):
	pass

#obtaining root equality variables:
left_part_key,right_part_key = monkeys['root']['args'][0], monkeys['root']['args'][1]

variable,diff = 0,1
diff_history, var_history, boundary = [],[],None
step = 1

while(diff):
	#some rules to choose new variable
	if boundary:
		variable = obtainVariable(var_history,diff_history,boundary)		
	elif len(diff_history) > 1:
		previous,pre_previous = len(diff_history)-1, len(diff_history)-2
		if(diff_history[previous] > 0 and diff_history[pre_previous] < 0) or (diff_history[previous] < 0 and diff_history[pre_previous] > 0):
			boundary = (min(var_history[previous],var_history[pre_previous]),max(var_history[previous],var_history[pre_previous]))
			print(var_history[-2:])
			print('boundary caught!')
			sys.exit()
			variable = obtainVariable(var_history,diff_history,boundary)
			step = 1
		else:
			if(abs(diff_history[previous])<=abs(diff_history[pre_previous])):
				step *= 2
				variable += sign(variable)*step
			else:
				variable = -sign(variable)*abs(variable)
				step = 1
	
	monkeys['humn'] = {'func':lambda:variable, 'args':[]}
	diff = evaluate(left_part_key)-evaluate(right_part_key)
	
	diff_history.append(diff)
	var_history.append(variable)
	
