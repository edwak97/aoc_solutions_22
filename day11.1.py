import re

lines = []
with open('testinput.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
rounds = 20
monkey = []
i = 1
while(i < len(lines)):
	monket = {}

	def getVal(oof:str):
		return (oof.split(':'))[1]

	st_items = getVal(lines[i])
	st_items = re.findall(r'\d+', st_items)
	items = [int(item) for item in st_items]
	monket['items'] = items

	st_op = getVal(lines[i+1])
	st_op = (st_op[11:]).split(' ')
	formula = None
	_num = None
	if st_op[1] == 'old':
		formula = (lambda old,num:old**2)
	else:
		_num = int(st_op[1])
		if st_op[0] == '+':
			formula = lambda old,num: old+num
		else:
			formula = lambda old,num: old*num
	monket['op'] = formula
	monket['num'] = _num

	st_test = getVal(lines[i+2])
	test = int((re.findall(r'\d+', st_test))[0])
	monket['test'] = test

	st_iftrue = getVal(lines[i+3])
	iftrue = int((re.findall(r'\d+', st_iftrue))[0])
	monket['iftrue'] = iftrue

	st_iffalse = getVal(lines[i+4])
	iffalse = int((re.findall(r'\d+', st_iffalse))[0])
	monket['iffalse'] = iffalse
	
	monket['count'] = 0
	monkey.append(monket)

	i+=7

for i in range(0, rounds):
	for m,monket in enumerate(monkey):
		formula = monket['op']
		for k,item in enumerate(monket['items']):
			level = formula(item, monket['num']) // 3
			if level % monket['test'] == 0:
				(monkey[monket['iftrue']]['items']).append(level)
			else:
				(monkey[monket['iffalse']]['items']).append(level)
			monkey[m]['count']+=1
		monkey[m]['items'] = []

twobest = (sorted(monkey, key = lambda x:x['count']))[-2:]
level_business = twobest[0]['count'] * twobest[1]['count']
print(f'{level_business}')

