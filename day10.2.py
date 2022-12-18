lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)((line.strip()).split(' ')) for line in lines]


heap = ['.' for x in range (0,40)]
def enCycle(step:int = 40):
	counter, eol = 0, step - 1
	while True:
		if counter == eol:
			yield (counter, True)
			counter = 0
			continue
		yield (counter, False)
		counter+=1

hannahowo = enCycle()
X = 1
def flush():
	global heap
	print('\n', end = '')
	for c in heap:
		print(c,end = '')
	heap = ['.' for c in heap]

def getcmd():
	value = next(hannahowo)
	if(value[0] in {X-1, X, X+1}):
		heap[value[0]] = '#'
	if value[1]:
		flush()

for pair in lines:
	if pair[0] == 'noop':
		getcmd()
		continue
	delta = int(pair[1])
	i = 0
	while i < 2:
		getcmd()
		i += 1
	X += delta
