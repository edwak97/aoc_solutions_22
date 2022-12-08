lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [line.strip() for line in lines]
testlines = [
	'30373',
	'25512',
	'65332',
	'33549',
	'35390'
	]
tops = [[{'h':int(x),'up':True,'down':True,'left':True,'right':True} for x in line] for line in lines]
visible, invisible = 0,0
for k,line in enumerate(tops):
	for i,top in enumerate(line):

		compar = sorted(tops[k][i+1:], key = lambda x: x['h']) #right
		if compar == [] or top['h'] > compar[-1]['h']:
			tops[k][i]['right'] = False
	
		compar = sorted(tops[k][:i], key = lambda x: x['h']) #left
		if compar == [] or top['h'] > compar[-1]['h']:	
			tops[k][i]['left'] = False
		
		colarr = [tops[index][i] for index,row in enumerate(tops)]

		compar = sorted(colarr[k+1:], key = lambda x: x['h']) #down
		if compar == [] or top['h'] > compar[-1]['h']:
			tops[k][i]['down'] = False

		compar = sorted(colarr[:k], key = lambda x: x['h'])
		if compar == [] or top['h'] > compar[-1]['h']:
			tops[k][i]['up'] = False
		
		if tops[k][i]['right'] and tops[k][i]['left'] and tops[k][i]['down'] and tops[k][i]['up']:
			invisible+=1
			continue
		visible+=1
print(f'{visible}, {invisible}')
			



