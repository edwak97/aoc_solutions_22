import sys

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = ['1','2','3','4','5','6']

numbers = [int(i) for i in lines]

sys.exit()

indexes = [i for i in range(len(numbers))]

class NumData:

	def __init__(self, numbers):
		self.numbers = numbers
		self.indexes = {i:i for i in range(len(numbers))}
	
	def obtainShift(self, index:int, shift:int)->int:		
		if ((index == 0) and shift > 0) or ((index == len(self.numbers)-1) and shift < 0):
			if abs(shift) >= len(self.numbers):
				new_index = (index + 1) if shift > 0 else (index - 1)
				new_shift = (1 if shift > 0 else -1) * (abs(shift)-len(self.numbers))
				return (1 if shift > 0 else -1)+self.obtainShift(new_index, new_shift)
			return shift
		return (1 if shift > 0 else -1) * (abs(shift) % (len(self.numbers)-1))

	def shiftData(self, index:int, shift:int):
		
		shift = self.obtainShift(index, shift)
		new_index = index + shift
		
		if shift > 0:
			if new_index > len(self.numbers) - 1:
				return self.shiftData(index, -(len(self.numbers)-1)+shift)
			self.numbers = self.numbers[:index] + self.numbers[index+1:new_index+1] + [self.numbers[index]] + self.numbers[new_index+1:]
			return shift
		if shift < 0:
			if new_index < 0:
				return self.shiftData(index, len(self.numbers)-1+shift)
			self.numbers = self.numbers[:new_index] + [self.numbers[index]] + self.numbers[new_index:index] + self.numbers[index+1:]
			return shift
		
		return index
	
	def updateIndexes(self, index:int, shift:int):
		'''
		if not shift:
			return
		forward = shift > 0
		# 0 1 2 3 4 5
		# index 1 shift 4
		begin_index = self.indexes[index] 
		check = lambda x: ((x<begin_index+shift) and forward) or ((x>begin_index+shift) and not forward)
		
		i = begin_index
		while(check(i)):
		'''	

	def move(self, index:int):
		
		absolute_shift = self.numbers[index]
		
		shift = self.shiftData(index, absolute_shift)
		
		self.updateIndexes(index, shift)

#tests:
#general shift

nums1 = NumData([5,4,3,2,1,0])
nums1.shiftData(0,5)
assert nums1.numbers == [4,3,2,1,0,5]
nums1.shiftData(1,3)
assert nums1.numbers == [4,2,1,0,3,5]
nums1.shiftData(3,0)
assert nums1.numbers == [4,2,1,0,3,5]
nums1.shiftData(2,1)
assert nums1.numbers == [4,2,0,1,3,5]
nums1.numbers = [-1,0,1,2,-2,4,5]
assert nums1.shiftData(4,-2) == -2
assert nums1.numbers == [-1,0,-2,1,2,4,5]
#out of range shift
nums1.numbers = [4, -2, 5, 6, 7, 8, 9]
nums1.shiftData(1,-2)
assert nums1.numbers == [4, 5, 6, 7, 8, -2, 9]
nums1.shiftData(6,1)
assert nums1.numbers == [4,9,5,6,7,8,-2]
assert nums1.shiftData(0,6) == 6
assert nums1.numbers == [9,5,6,7,8,-2,4]
nums1.shiftData(3,6)
assert nums1.numbers == [9,5,6,7,8,-2,4]
nums1.shiftData(0,6)
assert nums1.numbers == [5,6,7,8,-2,4,9]
nums1.numbers = [0,1,2,3,4,5,6,7,8,9]
nums1.shiftData(1,9)
assert nums1.numbers == [0,1,2,3,4,5,6,7,8,9]
nums1.shiftData(1,18)
assert nums1.numbers == [0,1,2,3,4,5,6,7,8,9]
nums1.shiftData(9,18)
assert nums1.numbers == [0,1,2,3,4,5,6,7,8,9]
nums1.shiftData(9,-19)
assert nums1.numbers == [0,1,2,3,4,5,6,7,9,8]

nums1.numbers = [0,1,2,3,4,5,6,7,8,9]
assert nums1.shiftData(0,-9) == 0
assert nums1.numbers == [0,1,2,3,4,5,6,7,8,9]
nums1.shiftData(0,51)
assert nums1.numbers == [1,2,3,4,5,6,0,7,8,9]
nums1.shiftData(9,-51)
assert nums1.numbers == [1,2,3,9,4,5,6,0,7,8]
nums1.shiftData(0,4)
assert nums1.numbers == [2,3,9,4,1,5,6,0,7,8]
nums1.shiftData(9,-1)
assert nums1.numbers == [2,3,9,4,1,5,6,0,8,7]
nums1.shiftData(4,111)
assert nums1.numbers == [2,3,9,4,5,6,0,1,8,7]
nums1.shiftData(7,111)
assert nums1.numbers == [2,1,3,9,4,5,6,0,8,7]
nums1.shiftData(1,-578)
assert nums1.numbers == [2,3,9,4,5,6,0,8,1,7]
assert nums1.shiftData(8,2) == -7
assert nums1.numbers == [2,1,3,9,4,5,6,0,8,7]
assert nums1.shiftData(3,-5) == 4
assert nums1.numbers == [2,1,3,4,5,6,0,9,8,7]
