import re
import copy

timeToRelease = 1
beginValve = 'AA'
T = 30

lines = []
with open('input.txt', 'r') as file_origin: 
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
valveNames = [key for key,val in valves.items() if val['rate'] > 0]
print(valveNames)
		
def getCombinations(names):
	if len(names) == 1:
		yield names
		return

	for i in range(len(names)):
		prefix = [names[i]]
		rest = copy.copy(names)
		del(rest[i])
		combination = getCombinations(rest)
		while(True):
			try:
				result = prefix + next(combination)
				yield result

			except StopIteration:
				break

def getProductivity(names):
	result = 0
	_T = T
	for k in range(len(names)-1):
		distance = valves[names[k]]['valves'].get(names[k+1])
		if distance == None:
			result = None
			print('This path is not possible')
			break
		_T -= (distance + timeToRelease)
		if (T <= 0):
			break
		addendum = _T * valves[names[k+1]]['rate']
		result += addendum
	return result

combination = getCombinations(valveNames)
i = 1
bestProductivity = 0
while True:
	try:
		thisPath = [beginValve] + next(combination)
		thisProductivity = getProductivity(thisPath)
		if thisProductivity > bestProductivity:
			bestProductivity = thisProductivity
		i += 1	
	except StopIteration:
		break

print(f'{i} combinations considered\n{bestProductivity}')
