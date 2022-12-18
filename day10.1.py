lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [(lambda x:x)((line.strip()).split(' ')) for line in lines]


def enCycle(bottom:int = 20, step:int = 40):
	num, counter, bottomaway = 1,1, False
	while True:
		if not bottomaway and counter == bottom:
			bottomaway = True
			yield (counter, True)
			counter, num = 1, num + 1
			continue
		if counter == step:
			yield (num, True)
			counter, num = 1, num + 1
			continue
		yield (num, False)
		counter+=1
		num +=1

hannahowo = enCycle(bottom = 20, step = 40)
X = 1
res = 0
counter = 1
for pair in lines:
	if pair[0] == 'noop':
		value = next(hannahowo)
		if value[1] and counter < 7:
			res += X * value[0]
			counter +=1
		continue
	delta = int(pair[1])
	iterlim = delta if delta > 0 else -delta
	print(f'{delta} {iterlim}')
	i = 0
	while i < 2:
		value = next(hannahowo)
		if value[1] and counter < 7:
			res += X * value[0]
			counter += 1
		i += 1
	X += delta

print(f'\n{X}, {res}, {counter}')
