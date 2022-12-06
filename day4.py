lines = []
with open('input_origin.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

def getRange(args):
	args = args.split('-')
	return [int(item) for item in args]

def overlapped(args):
	args = sorted(args, key = lambda x:x[0])
	i = 0
	while(i < len(args)-1):
		if args[i][1] >= args[i+1][0]:
			return 1
		i+=1
	return 0
testLines = [
	'2-4,6-8', '2-3,4-5','5-7,7-9','2-8,3-7','6-6,4-6','2-6,4-8']
totalScore = 0
for line in lines:
	line = line.strip().split(',')
	args = []
	args.append(getRange(line[0]))
	args.append(getRange(line[1]))
	totalScore += overlapped (args)
print(totalScore)
