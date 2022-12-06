lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
line = lines[0].strip()
### Solution 1 ###
step1 = 4
step2 = 14
def getN(arg, step):
	i = step
	while i < len(arg):
		memory = []
		shift = 0
		done = True
		for shift in range(1,step+1):
			if arg[i-shift] in memory:
				done = not True #LMAO
				break
			else:
				memory[len(memory):] = [arg[i-shift]]
		if done:
			print(i)
			break
		i += step-shift+1
#solution1 getN(line,4)
getN(line,14)
		
