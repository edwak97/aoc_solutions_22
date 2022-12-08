lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = [line.strip() for line in lines]

class Node:
	def __init__(self, node_type, name, parentNode = None, size = None):
		
		self.node_type = node_type # 0 -- files, 1 -- dirs
		self.name = name
		self.parentNode = parentNode
		self.size = None if size == None else int(size)
		self.childNodes = []

rootDir = None
currentDir = None

def changewd(dirname):
	global currentDir
	global rootDir
	if not currentDir:	
		a = Node(1, dirname)
		rootDir = a #not true, to be honest
		#print('root is set')
		currentDir = a
		return
	for item in currentDir.childNodes:
		if item.node_type == 1:
			if item.name == dirname:
				currentDir = item
				#print('wd: ', currentDir.name)
				return
	if dirname == '..':
		currentDir = currentDir.parentNode
		return
	if dirname == '/':
		currentDir = rootDir
		return
	print(f'{dirname} not in {currentDir}')

def readls(args):
	global currentDir
	for arg in args:
		arg = arg.split(' ')
		if arg[0] == 'dir':
			if not currentDir:
				print(f'it cannot be, {arg}')
				return
			newFolder = Node(node_type = 1, name = arg[1], parentNode = currentDir)
			(currentDir.childNodes).append(newFolder)
		else:
			newFile = Node(node_type = 0, name = arg[1], size = arg[0], parentNode = currentDir)
			(currentDir.childNodes).append(newFile)
def cmdRead(linearr):
	cmdarr = linearr.split(' ')
	switch = {
		'ls': readls,
		#'pwd': readwd,
	}
	res = switch.get(cmdarr[0],0)
	if res != 0:
		return res
	switch = {
		'cd': changewd,
		#'rm': rmvfi
	}
	res = switch.get(cmdarr[0], 0)
	if res != 0:
		res(cmdarr[1])
	else:
		print(f'It is not recognized: {res} args {cmdarr[1]}')

def getOutend(lines, i):
	res = []
	k = i+1
	while k < len(lines):
		if lines[k][0] == '$':
			break
		res[len(res):] = [lines[k]]
		k+=1
	return (res, k)

#### Reading Input ####
def beginRead(lines):
		i = 0
		while i < len(lines):
			if lines[i][0] == '$':
				applyf = cmdRead(lines[i][2:])
				if applyf:
					args = getOutend(lines, i)
					applyf(args[0])
					i = args[1]
					continue
			i+=1

def findSize(dire):
	res = 0
	for item in dire.childNodes:
		if item.node_type == 0:
			res+=item.size
		else:
			res+= findSize(item)
	return res

def findrightSize(dire):
	res = 0
	for item in dire.childNodes:
		if item.node_type == 1:
			temp = findSize(item)
			if temp <= 100000:
				res+=temp
			res+=findrightSize(item)
	return res

def freeSpace():
	aim = findSize(rootDir) - 40000000
	dirlist = []
	def flatDir(arg):
		nonlocal dirlist
		if arg.node_type == 1:
			appendix = (arg, findSize(arg))
			dirlist.append(appendix)
			for item in arg.childNodes:
				flatDir(item)
	flatDir(rootDir)
	dirlist = sorted(dirlist, key = lambda x: x[1])
	dirlist = [x for x in dirlist if x[1] >= aim]
	print(f'need to free: {aim}; freed: {dirlist[0][1]}')
def printTree(argtest, k = 0):
	tab = k
	space = ' '*tab
	if argtest.node_type == 0:
		print(f'{space}{argtest.name}: {argtest.size}')
	else:
		print(f'{space}{argtest.name}:')
	for item in argtest.childNodes:
		space = tab*' '
		printTree(item, tab+2)
beginRead(lines)
#printTree(rootDir)
#print(findrightSize(rootDir)) #part 1
freeSpace() #part 2
