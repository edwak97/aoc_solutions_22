import re

tmax = 24
materialResource = {'ore':0,'clay':0,'obsidian':0,'geode':0}
botResource =      {'ore':1,'clay':0,'obsidian':0,'geode':0}
#units per minute
productivity = 1

#itemToMax = 'geode'

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

lines = ['1 4 2 3 14 2 7']

#the dictionary 'a':{'b':val1, ... 'c':val2} means that there is a_bot type which requires b and c resource in the amount v1 and v2 respectively to produce a unit of a_bot

blueprints = [(lambda x:{'ore':{'ore':int(x[1])}, 'clay':{'ore':int(x[2])}, 'obsidian':{'ore':int(x[3]), 'clay':int(x[4])}, 'geode':{'ore':int(x[5]), 'obsidian': int(x[6])}})(re.findall(r'\d+', line)) for line in lines]

#since the requirements for a bot production are fixed we need to calculate the priority:
priority_sequence = ['geode','obsidian','clay','ore']

def combinationGenerator(mRes, bRes, T, blueprint):
	
	#working with the copy
	mRes, bRes = dict(mRes), dict(bRes)

	#taking the crop:
	mRes = {material:mRes[material]+bRes[material]*productivity for material in mRes}
	
	#decision making algoritm to produce new machines:
	#wrong one; buying only ore because it is available
	#sometimes it is necessary to wait #todo

	for material in priority_sequence:
		while(True):
		#till we can buy a unit of a bot producing "material"
			purchase_snapshot = dict(mRes)
			#since a purchase transaction may consist of several materials the transaction may proceed only if all materials are available for purchase
			transactionComplete = True
			for _material in blueprint[material]:
				if blueprint[material][_material] <= purchase_snapshot[_material]:
					purchase_snapshot[_material] -= blueprint[material][_material]
				else:
					transactionComplete = False
					break
			if not transactionComplete:
				
				break
			mRes = purchase_snapshot
			bRes[material] += 1
	if T == tmax:
		return mRes['geode']
	
	return combinationGenerator(mRes, bRes, T+1, blueprint)
				
for blueprint in blueprints:
	test_result = combinationGenerator(materialResource, botResource, 1, blueprint)
	print(test_result)
	break

