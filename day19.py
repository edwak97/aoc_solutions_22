import re
import sys
import copy
import time

start_time = time.time()
tmax = 32

#order makes sense
materials = ['geode', 'obsidian', 'clay', 'ore']

m_resource = {'ore':0,'clay':0,'obsidian':0,'geode':0}
b_resource = {'ore':1,'clay':0,'obsidian':0,'geode':0}

#units per minute by a bot
productivity = 1

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

#the dictionary 'a':{'b':val1, ... 'c':val2} means that there is a_bot type which requires b and c resource in the amount v1 and v2 respectively to produce a unit of a_bot

#lines = ['1 4 2 3 14 2 7', '2 2 3 3 8 3 12']

blueprints = [(lambda x:{'ore':{'ore':int(x[1])}, 'clay':{'ore':int(x[2])}, 'obsidian':{'ore':int(x[3]), 'clay':int(x[4])}, 'geode':{'ore':int(x[5]), 'obsidian': int(x[6])}})(re.findall(r'\d+', line)) for line in lines]

def getAvailableToBuy(mRes):
	result = []
	for bot in materials:
		canBuy = True
		for material in blueprint[bot]:
			if blueprint[bot][material] > mRes[material]:
				canBuy = False
				break
		if canBuy:
			result.append(bot)
			if bot == 'geode':
				return ['geode']
	return result

def doesMakeSense(mRes, bRes, bot, blueprint):
	#buying a bot at minute tmax does not make sense
	if bot == 'geode':
		return True
	
	bot_max = max([val[material] for val in blueprint.values() for material in val if material == bot])
	return bot_max > bRes[bot]

	#consier we have 7 obsidian bots. Would buying yet another one benefit us?
	#7 obsidian bots produce 7 unit that are enough to build a geode. Having 8 bots is excessive

def combinationGenerator(mRes, bRes, T, blueprint, previous_availableToBuy, previous_option, record_highs):
	
	#the bot has started the production; the first material unit will have been produced by the end of this minute
	if T == 0:
		yield mRes['geode']
		return
	
	#some performance optimization using caching
	bRes_record, mRes_record = record_highs[T-1]
	if bRes['geode'] < bRes_record and mRes['geode'] < mRes_record:
		return
	if bRes['geode'] > bRes_record and mRes['geode'] > mRes_record:
		record_highs[T-1] = (bRes['geode'], mRes['geode'])

	availableToBuy = getAvailableToBuy(mRes)
	for bot in availableToBuy:
		#It does not make sense to buy a bot now if it was available to buy a minute before but skip was chosen!
		if previous_option == None and bot in previous_availableToBuy:
			continue
		if not doesMakeSense(mRes, bRes, bot, blueprint):
			continue
		mRes_snapshot, bRes_snapshot = copy.deepcopy(mRes), copy.deepcopy(bRes)
		for material in blueprint[bot]:
			mRes_snapshot[material] -= blueprint[bot][material]
		
		mRes_snapshot = {_material:(mRes_snapshot[_material]+bRes[_material]*productivity) for _material in mRes_snapshot}
			
		#new bot is ready!:
		bRes_snapshot[bot] += 1
			
		combinations = combinationGenerator(mRes_snapshot, bRes_snapshot, T-1, blueprint, availableToBuy, bot, record_highs)

		while(True):
			try:
				yield(next(combinations))
			except StopIteration:
				break
		#buying geode is always the best ooption if possible
	#considering skipping (does not make sense if geode-cracking bot can be bought)
	if availableToBuy == ['geode']:
		return

	#skipping: no new bots, but those made before has produced something;
	mRes_snapshot = {material:(mRes[material]+bRes[material]*productivity) for material in mRes}
	
	combinations = combinationGenerator(mRes_snapshot, copy.deepcopy(bRes), T-1, blueprint, availableToBuy, None, record_highs)
	while(True):
		try:
			yield(next(combinations))
		except StopIteration:
			break
'''			
#part1
tmax = 24
res = 0
for i,blueprint in enumerate(blueprints):	
	record_highs = [(0,0) for i in range(tmax)]
	test_result = combinationGenerator(m_resource, b_resource, tmax, blueprint, [], None, record_highs)
	best_result = 0
	while(True):
		try:
			thisPath = next(test_result)
			if(thisPath > best_result):
				best_result = thisPath
		except StopIteration:
			break
	res += best_result*(i+1)
'''
res = 1
blueprints = blueprints[:3]
for blueprint in (blueprints):
	record_highs = [(0,0) for i in range(tmax)]
	test_result = combinationGenerator(m_resource, b_resource, tmax, blueprint, [], None, record_highs)
	best_result = 0
	while(True):
		try:
			thisPath = next(test_result)
			if(thisPath > best_result):
				best_result = thisPath
		except StopIteration:
			break
	res *= best_result

print(res)
print(f'Execution required: {time.time() - start_time}')
