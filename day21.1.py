lines = []
import re

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
	global monkeys
	monkeys[monkey_name]['args'] = [evaluate(item) for item in monkeys[monkey_name]['args']]

	return monkeys[monkey_name]['func'](*monkeys[monkey_name]['args'])
print(evaluate('root'))
	
