import re

T = 30
lines = []
with open('testinput.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]

valves = {}
for line in lines:
	strPointers = re.findall(r'[A-Z]{2}', line)
	rate = int(re.findall(r'\d+', line)[0])
	key, rest = strPointers[0], strPointers[1:]
	rest = {val:1 for val in rest}
	rest[key] = 0
	valves[key] = {'rate':rate, 'valves': rest}

for key in valves: #getting the distance between this valve and other valves
	front = {_key for _key,dist in valves[key]['valves'].items() if dist == 1} # the current front line
	steps = 2	
	while(front):
		newfront = set()
		for branch in front:
			branch_keys = {_key for _key,dist in valves[branch]['valves'].items() if dist == 1}
			for _key in branch_keys:
				if _key not in valves[key]['valves']:
					valves[key]['valves'][_key] = steps
					newfront.add(_key)
		steps += 1
		front = newfront
#building combinations
#excluding valves producing nothing
valves = {key:val for key,val in valves.items() if val['rate'] > 0}
combination = [key for key in valves]

busy = [[i+x for x in range(i+2)] for i in range(len(combination)-1)]
print(busy)
	
	
