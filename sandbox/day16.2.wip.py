import re
import copy
import time

start_time = time.time()

timeToRelease = 1
beginValve = ['AA']
T = 26

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

#track is the array of opened valves
def getCombinationSingle(previousValves, released, T, nextNames):
	
	if not nextNames:
		yield (released, copy.copy(previousValves))
		return
	
	for i in range(len(nextNames)):
		
		_T = T - (timeToRelease + valves[previousValves[-1]]['valves'][nextNames[i]])
		if _T <= 0:
			yield (released, copy.copy(previousValves))
			continue

		_previousValves = copy.copy(previousValves)
		_previousValves.append(nextNames[i])
		_nextNames = copy.copy(nextNames)
		del(_nextNames[i]) #the rest part is remained to consider

		_released = released + valves[nextNames[i]]['rate'] * _T
		
		combination = getCombinationSingle(_previousValves, _released, _T, _nextNames)
		while True:
			try:
				yield next(combination)
			except StopIteration:
				break

def getMaxForSingle(previousValves, released, T, nextNames):
	
	combination = getCombinationSingle(previousValves, released, T, nextNames)
	bestPath, bestProductivity = [], 0
	while True:
		try:
			thisValue = next(combination)
			if thisValue[0] > bestProductivity:
				bestProductivity = thisValue[0]
				bestPath = thisValue[1]
		except StopIteration:
			break
	
	return (bestProductivity, bestPath)

bestPath, bestProductivity = [], 0

baseCombination = getCombinationSingle(beginValve, 0, T, valveNames)

#print(getMaxForSingle(beginValve, 0, 30, valveNames)) #This one is correct :(

while True:
	try:
		myResult = next(baseCombination)
		
		elephantNodes = [name for name in valveNames if name not in myResult[1]]
			
		elephantBestResult = getMaxForSingle(beginValve, 0, T, copy.copy(elephantNodes))

		totalResult = myResult[0] + elephantBestResult[0]

		if totalResult > bestProductivity:
			bestProductivity = totalResult
			message = f'my path: {myResult[1]}\n elephant path: {elephantBestResult[1]}\nmy score: {myResult[0]} elephant score: {elephantBestResult[0]}'
			print(f'Better path found {bestProductivity}\n{message}')

	except StopIteration:
		break
print(valves)
print('\n')
print(f'{bestProductivity}')

print(f'\nExecution required {time.time() - start_time}')
