import re
import copy
import math

timeToRelease = 1
beginValve = 'AA'
T = 26

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

def getCombinations(previousValve1, released1, T1, previousValve2, released2, T2, nextNames):
	
	if not nextNames:
		yield released1 + released2
		return
	
	#combination generation
	for i in range(len(nextNames)):
		
		_nextNames = copy.copy(nextNames)
		del(_nextNames[i])

		if (T1 == None):
			_released1 = released1
			_previousValve1 = None
			_T1 = None
		else:
			_T1 = T1 - (timeToRelease + valves[previousValve1]['valves'][nextNames[i]])
			if (_T1 <= 0):
				_released1 = released1
				_previousValve1 = None
				_T1 = None
			else:
				_released1 = released1 + valves[nextNames[i]]['rate'] * _T1
				_previousValve1 = nextNames[i]

		if not _nextNames:
			yield _released1 + released2
			continue

		for k in range(len(_nextNames)):
			
			if(T2 == None):
				_released2 = released2
				_previousValve2 = None
				_T2 = None
			else:
				_T2 = T2 - (timeToRelease + valves[previousValve2]['valves'][_nextNames[k]])
				if(_T2 <= 0):
					_released2 = released2
					_previousValve2 = None
					_T2 = None
				else:
					_released2 = released2 + valves[_nextNames[k]]['rate'] * _T2
					_previousValve2 = _nextNames[k]
			
			if(_T1 == _T2 == None):
				yield _released1 + _released2
				continue

			__nextNames = copy.copy(_nextNames)
			del(__nextNames[k])
			combination = getCombinations(_previousValve1, _released1, _T1, _previousValve2, _released2, _T2, __nextNames)
			while(True):
				try:
					yield next(combination)
				except StopIteration:
					break
n = 0
bestProductivity = 0
print(f'all names: {valveNames}')
for i in range(len(valveNames)):

	k = i + 1
	beginValve1 = valveNames[i]
	T1 = T - (timeToRelease + valves[beginValve]['valves'][beginValve1])
	
	while(k < len(valveNames)):
		
		print(f'combina {valveNames[i]}-{valveNames[k]}')
		beginValve2 = valveNames[k]
		T2 = T - (timeToRelease + valves[beginValve]['valves'][beginValve2])
		released1 = 0
		released2 = 0
		if (T1 <= 0):
			T1 = None
		else:
			released1 = valves[beginValve1]['rate'] * T1

		if(T2 <= 0):
			T2 = None
		else:
			released2 = valves[beginValve2]['rate'] * T2
		
		_valveNames = copy.copy(valveNames)
		del(_valveNames[k])
		del(_valveNames[i]) # order makes sense
		
		#print(f'next: {_valveNames}')

		k += 1
		baseCombination = getCombinations(
				beginValve1, released1, T1,
				beginValve2, released2, T2,
				_valveNames
		)
		k += 1
		#print(f'{beginValve1} {released1} {T1}\n{beginValve2} {released2} {T2}')
		while True:
			try:
				thisValue = next(baseCombination)
				if thisValue > bestProductivity:
					bestProductivity = thisValue
					print(f'Better solution! combination {n}, value {bestProductivity}\n')
				n += 1	
			except StopIteration:
				break
print(f'{n} combinations considered\n{bestProductivity}')

