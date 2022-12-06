lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
step = 4
axis_string = []
crates_string = []
cmd_string = []
delim = 0
for i,line in enumerate(lines):
	if line == '\n':
		delim = i
		break
axis_string = (lines[delim-1])[1:-2]
crates_string = lines[:delim-1]
cmd_string = lines[delim+1:]
nstacks = len(axis_string.split(3*' '))
stacks = [[] for x in range (nstacks)]

i = len(crates_string)-1
while(i > -1):
	x = 0
	for k in range(1,2+step*(nstacks-1),step):
		if crates_string[i][k] not in {' ', '[', ']'}:
			stacks[x][len(stacks[x]):] = crates_string[i][k]
		x+=1
	i-=1

def move(N, fromw, tow, keeporder = False):
	fromw,tow = fromw-1,tow-1
	global stacks
	stacks[tow][len(stacks[tow]):] = stacks[fromw][-N:] if keeporder else (stacks[fromw][-N:])[::-1]
	stacks[fromw] = stacks[fromw][:-N]

for cmdline in cmd_string:
	cmdline = cmdline.strip().split(' ')
	n,fr,t = int(cmdline[1]), int(cmdline[3]), int(cmdline[5])
	#move(n,fr,t) #solution 1
	move(n,fr,t,True) #Solution 2
for item in stacks:
	print(item[-1],end='')
