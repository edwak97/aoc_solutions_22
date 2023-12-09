import re
import sys
import copy

tmax = 24
#order makes sense!
materials = ['geode', 'obsidian', 'clay', 'ore']

m_resource = {'ore':0,'clay':0,'obsidian':0,'geode':0}
b_resource = {'ore':1,'clay':0,'obsidian':0,'geode':0}

#units per minute by a bot
productivity = 1

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

#for testing purposes
lines = ['1 4 2 3 14 2 7']

#the dictionary 'a':{'b':val1, ... 'c':val2} means that there is a_bot type which requires b and c resource in the amount v1 and v2 respectively to produce a unit of a_bot

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
	#if geode bot is available to buy then it is the best option!
	if 'geode' in result:
		result = ['geode']
	
	return result

#it is not right option to buy
def combinationGenerator(mRes, bRes, T, blueprint, previous_availableToBuy, previous_option):
	
	#the bot has started the production; the first material unit will have been produced by the end of this minute
	if T == 0:
		yield mRes['geode']
		return
	
	availableToBuy = getAvailableToBuy(mRes)
	for bot in availableToBuy:
		#It does not make sense to buy a bot now if it was available to buy a minute before but skip was chosen!
		if previous_option == None and bot in previous_availableToBuy:
			continue
		mRes_snapshot, bRes_snapshot = copy.deepcopy(mRes), copy.deepcopy(bRes)
		for material in blueprint[bot]:
			mRes_snapshot[material] -= blueprint[bot][material]
		
		mRes_snapshot = {_material:(mRes_snapshot[_material]+bRes[_material]*productivity) for _material in mRes_snapshot}
			
		#new bot is ready!:
		bRes_snapshot[bot] += 1
			
		combinations = combinationGenerator(mRes_snapshot, bRes_snapshot, T-1, blueprint, availableToBuy, bot)

		while(True):
			try:
				yield(next(combinations))
			except StopIteration:
				break
	#considering skipping (does not make sense if geode-cracking bot has been bought)
	if availableToBuy and (bot == 'geode'):
		return

	#skipping: no new bots, but those made before has produced something;
	mRes_snapshot = {material:(mRes[material]+bRes[material]*productivity) for material in mRes}
	
	combinations = combinationGenerator(mRes_snapshot, copy.deepcopy(bRes), T-1, blueprint, availableToBuy, None)
	while(True):
		try:
			yield(next(combinations))
		except StopIteration:
			break

for blueprint in blueprints:
	availableToBuy = []
	option = None
	test_result = combinationGenerator(m_resource, b_resource, tmax, blueprint, availableToBuy, option)
	best_result = 0
	while(True):
		try:
			thisPath = next(test_result)
			if(thisPath > best_result):
				print(f'wow, new top! {thisPath}')
				best_result = thisPath
		except StopIteration:
			break
	break

