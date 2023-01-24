lines = []
with open('testinput.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)(line.strip()) for line in lines]
pairs = []
i = 0
while(i < len(lines)):
	pair = []
	pair.append(lines[i])
	pair.append(lines[i+1])
	pairs.append(pair)
	i += 3

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
for pair in pairs:
	list1 = strtolist(pair[0])
	list2 = strtolist(pair[1])
	print(list1)
	print(list2)
	print('\n')


