lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [line.strip() for line in lines]

tops = [[{'h':int(x), 'score': 0} for x in line] for line in lines]
# True stands for invisible
def encountree(val, arr):
	i = 0
	for item in arr:
		i+=1
		if val['h'] <= item['h']:
			return (i, True)
	return (i, False)

visible = 0
for k,line in enumerate(tops):
	for i,top in enumerate(line):
		
		right = encountree(top, tops[k][i+1:])
		left = encountree(top, (tops[k][:i])[::-1])
	
		colarr = [tops[index][i] for index,row in enumerate(tops)]

		down = encountree(top, colarr[k+1:])
		up = encountree(top, (colarr[:k])[::-1])
		
		tops[k][i]['score'] = right[0]*left[0]*down[0]*up[0]
		if right[1] and left[1] and down[1] and up[1]:
			continue
		visible+=1
score = (sorted([x for line in tops for x in line], key = lambda x: x['score']))[-1]['score']

print(f'{visible}')
print(f'{score}')
			



