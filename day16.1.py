import re
import copy
import math

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
	
def getCombinations(previousValve, released, T, nextNames):
	
	if not nextNames:
		yield released
		return
	
	for i in range(len(nextNames)):
		
		_T = T - (timeToRelease + valves[previousValve]['valves'][nextNames[i]])
		if _T <= 0:
			yield released
			continue

		_previousValve = nextNames[i]
		_nextNames = copy.copy(nextNames)
		del(_nextNames[i]) #the rest part is remained to consider

		_released = released + valves[_previousValve]['rate'] * _T
		combination = getCombinations(_previousValve, _released, _T, _nextNames)
		while(True):
			try:
				yield next(combination)
			except StopIteration:
				break
	
combination = getCombinations(beginValve, 0, T, valveNames)
i = 1
bestProductivity = 0
while True:
	try:
		thisValue = next(combination)
		if thisValue > bestProductivity:
			bestProductivity = thisValue
			#print(f'Better solution! combination {i}, value {bestProductivity}\n')
		i += 1	
	except StopIteration:
		break

print(f'{i} combinations considered\n{bestProductivity}')
