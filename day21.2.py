lines = []
import re
import sys

with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

def obtainDescription(line:str):
	rgx = re.compile(r'\s*(\w+)\s*:\s*(\d+|(\w+)\s*([-/+*]){1}\s*(\w+))')
	formula_items = rgx.findall(line)
	if not formula_items[0][4]:
		return (formula_items[0][0], lambda : int(formula_items[0][1]), [])
	return (formula_items[0][0], eval(f'lambda x,y: x {formula_items[0][3]} y'), [formula_items[0][2], formula_items[0][4]])
monkeys = {monkey:{'func':func,'args':args} for (monkey,func,args) in [obtainDescription(line) for line in lines]}

def evaluate(monkey_name:str):
	args = [evaluate(item) for item in monkeys[monkey_name]['args']]
	return monkeys[monkey_name]['func'](*args)

def sign(val):
	return -1 if val < 0 else 1

variable,diff = 0,1
diff_history, var_history, boundary = [],[],None
step = 1
#the root function must converge to 0
#if then we find x1 and x2 so that sign(func(x1)) != sign(func(x2))
#then there is a boundary
monkeys['root']['func'] = lambda x,y:x-y

while(diff):
	#some rules to choose new variable
	if boundary:
		((boundary1,value1),(boundary2,value2)) = boundary
		variable = (boundary1 + boundary2)//2
		monkeys['humn'] = {'func':lambda:variable, 'args':[]}
		diff = evaluate('root')

		if abs(value1) > abs(value2):
			boundary = ((variable, diff),(boundary2,value2))
		else:
			boundary = ((boundary1,value1),(variable,diff))

		continue

	elif len(diff_history) > 1:
		previous,pre_previous = len(diff_history)-1, len(diff_history)-2
		if sign(diff_history[previous]) != sign(diff_history[pre_previous]):
			boundary1, boundary2 = var_history[previous],  var_history[pre_previous]
			value1,    value2 =    diff_history[previous], diff_history[pre_previous]

			boundary = ((boundary1,value1), (boundary2,value2))
			
			#it must be int?
			variable = (boundary1 + boundary2)//2

		else:
			if(abs(diff_history[previous])<=abs(diff_history[pre_previous])):
				step *= 2
				variable += sign(variable)*step
			else:
				variable = -sign(variable)*abs(variable)
				step = 1
	
	monkeys['humn'] = {'func':lambda:variable, 'args':[]}
	diff = evaluate('root')
	
	diff_history.append(diff)
	var_history.append(variable)

print(variable)	
