import re

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
rounds = 10000
monkey = []
divisors = set()
i = 1

while(i < len(lines)):
	monket = {}

	def getVal(oof:str):
		return (oof.split(':'))[1]

	st_items = getVal(lines[i])
	st_items = re.findall(r'\d+', st_items)
	items = [{'val':int(item)} for item in st_items]
	monket['items'] = items

	st_op = getVal(lines[i+1])
	st_op = (st_op[11:]).split(' ')
	formula = None
	_num = None
	if st_op[1] == 'old':
		def localf(**kwargs):
			item = kwargs.get('item')
			for _divisor in divisors:
				item[_divisor] = (item[_divisor]**2) % _divisor
			return item
		formula = localf
	else:
		_num = int(st_op[1])
		if st_op[0] == '+':
			def localf(**kwargs): 
				item = kwargs.get('item')
				m = kwargs.get('m')
				num = monkey[m]['num']
				item['val'] += num
				for _divisor in divisors:
					item[_divisor] = (item[_divisor] + (num % _divisor)) % _divisor
				return item
			formula = localf
		else:
			def localf(**kwargs):
				item = kwargs.get('item')
				m = kwargs.get('m')
				num = monkey[m]['num']
				for _divisor in divisors:
					item[_divisor] = (item[_divisor] * (num % _divisor)) % _divisor
				return item
			formula = localf

	monket['op'] = formula
	monket['num'] = _num

	st_test = getVal(lines[i+2])
	test = int((re.findall(r'\d+', st_test))[0])
	monket['test'] = test
	divisors.add(test)

	st_iftrue = getVal(lines[i+3])
	iftrue = int((re.findall(r'\d+', st_iftrue))[0])
	monket['iftrue'] = iftrue

	st_iffalse = getVal(lines[i+4])
	iffalse = int((re.findall(r'\d+', st_iffalse))[0])
	monket['iffalse'] = iffalse
	
	monket['count'] = 0
	monkey.append(monket)

	i+=7

for divisor in divisors:
	for monk in monkey:
		for j,item in enumerate(monk['items']):
			monk['items'][j][divisor] = (item['val'] % divisor)

for i in range(rounds):
	for m,monket in enumerate(monkey):
		formula = monket['op']
		divisor = monket['test']
		for k,item in enumerate(monket['items']):
			level = formula(item=item, m=m)
			if level[divisor] == 0:
				(monkey[monket['iftrue']]['items']).append(level)
			else:
				(monkey[monket['iffalse']]['items']).append(level)
			monkey[m]['count']+=1
		monkey[m]['items'] = []

twobest = (sorted(monkey, key = lambda x:x['count']))[-2:]
level_business = twobest[0]['count'] * twobest[1]['count']
print(f'{level_business}')

