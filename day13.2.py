lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
def strtolist(line:str): #pass '[...]' value
	res = []
	line = line[1:-1]
	if line == '':
		return res
	i = 0
	while i < len(line):
		if line[i] == '[':
			opencounter, closecounter = 1,0
			k = i + 1
			while(k < len(line) and opencounter != closecounter):
				if line[k] == '[':
					opencounter += 1
				if line[k] == ']':
					closecounter += 1
				k+=1
			res.append(strtolist(line[i:k]))
			i = k
			continue
		if line[i] != ',':
			k = i
			substr = ''
			while(k < len(line) and line[k] != ','):
				substr += line[k]
				k+=1
			res.append(int(substr))
			i = k
			continue
		i+=1
	return res
def compareItems(left, right): #1 None stands for draw
	listype, intype = type([]), type(1)
	if type(left) == type(right) == listype:
		leftlen, rightlen = len(left), len(right)
		length = leftlen if leftlen < rightlen else rightlen
		pre_answer = None
		if leftlen < rightlen:
			pre_answer = True
		if leftlen > rightlen:
			pre_answer = False
		for i in range(length):
			answer = compareItems(left[i], right[i])
			if answer:
				return True
			if answer == False:
				return False
		return pre_answer
	if type(left) == type(right) == intype:
		if left < right:
			return True
		if left > right:
			return False
		return None
	if type(left) == intype:
		return compareItems([left],right)
	if type(right) == intype:
		return compareItems(left, [right])

signals = []
i = 0
while(i < len(lines)):
	signals.append({'val':strtolist(lines[i]), 'score':0})
	signals.append({'val':strtolist(lines[i+1]), 'score':0})
	i += 3
signals[len(signals):] = [{'val':[[2]], 'score':0}, {'val': [[6]], 'score':0}]
for i, signal in enumerate(signals):
	score = 0
	for k, _signal in enumerate(signals):
		if compareItems(signal['val'], _signal['val']):
			score += 1
	signals[i]['score'] = score
reordered = sorted(signals, key = lambda x:x['score'], reverse = True)
indice1 = [(index+1) for index,value in enumerate(reordered) if value['val'] == [[2]]][0]
indice2 = [(index+1) for index,value in enumerate(reordered) if value['val'] == [[6]]][0]
print(indice1 * indice2)
