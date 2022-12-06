lines = []
with open('input_origin.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
charList = [chr(x) for x in range(ord('a'), ord('z')+1)] + [chr(x) for x in range(ord('A'), ord('Z')+1)]

def getIndexByValue(char):
	for x in range(len(charList)):
		if charList[x] == char:
			return x

def getBadge(group):
	for char in charList:
		found = False
		for line in group:
			found = False
			for c in line:
				if c == char:
					found = True
					break
			if not found:
				break
		if found:
			return getIndexByValue(char)+1

totalScore = 0
group = []
for line in lines:
	line = line.strip()
	group.append(line)
	if len(group) == 3:
		totalScore += getBadge(group)
		group = []

print(totalScore)
