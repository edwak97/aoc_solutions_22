import math
lines = []
nknots = 10
maxdiff = math.sqrt(2)
positions = {(0,0)}
th = [(0,0) for x in range(nknots)]

with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x: (x[0],int(x[1])))((line.strip()).split(' ')) for line in lines]

mv = {
	'U':  lambda arg: (arg[0],   arg[1]+1),
	'UL': lambda arg: (arg[0]-1, arg[1]+1),
	'UR': lambda arg: (arg[0]+1, arg[1]+1),
	'D':  lambda arg: (arg[0],   arg[1]-1),
	'DL': lambda arg: (arg[0]-1, arg[1]-1),
	'DR': lambda arg: (arg[0]+1, arg[1]-1),
	'R':  lambda arg: (arg[0]+1, arg[1]),
	'L':  lambda arg: (arg[0]-1, arg[1]),
	}

def delta(node1, node2):
	return math.sqrt((node1[0]-node2[0])**2 + (node1[1]-node2[1])**2)

for pair in lines:
	move, i = mv.get(pair[0]), pair[1]
	while i > 0:
		th[-1] = move(th[-1])
		k = len(th)-2 
		while k > -1:
			head = th[k+1]
			tail = th[k]
			if delta(head, tail) > maxdiff:
				leastdiff = sorted([(movement, delta(head,movement(tail))) for key, movement in mv.items()], key = lambda x:x[1])
				func = leastdiff[0][0]
				th[k] = func(tail)
			if k == 0:
				positions.add(th[k])
			k-=1
		i-=1

print(len(positions))
print(th)
