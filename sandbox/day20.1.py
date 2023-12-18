import sys

lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()
lines = ['1','2','-3','3','-2','0','4']

numbers = [int(i) for i in lines]

class NumData:

	def __init__(self, numbers):
		self.numbers = numbers
		self.indexes = [i for i in range(len(numbers))]
	
	def obtainShift(self, shift:int)->int:
		return (1 if shift > 0 else -1) * (abs(shift) % (len(self.numbers)-1))
	
	def shiftForward(self, index:int, shift:int):
		shift = self.obtainShift(shift)
		new_index = index+shift
		
		if new_index > len(self.numbers)-1:
			self.shiftBackward(index, len(self.numbers)-1-shift)
			return
		
		self.numbers = self.numbers[:index] + self.numbers[index+1:new_index+1] + [self.numbers[index]] + self.numbers[new_index+1:]
		self.indexes = self.indexes[:index] + self.indexes[index+1:new_index+1] + [self.indexes[index]] + self.indexes[new_index+1:]
			
	def shiftBackward(self, index:int, shift:int):
		shift = self.obtainShift(shift)
		new_index = index-shift

		if new_index < 0:
			self.shiftForward(index, len(self.numbers)-1-shift)
			return

		self.numbers = self.numbers[:new_index] + [self.numbers[index]] + self.numbers[new_index:index] + self.numbers[index+1:]
		self.indexes = self.indexes[:new_index] + [self.indexes[index]] + self.indexes[new_index:index] + self.indexes[index+1:]

	def shiftData(self, index:int, shift:int):
		if shift > 0:
			self.shiftForward(index, shift)
			return
		if shift < 0:
			self.shiftBackward(index, -shift)

	def move(self, index:int):
		index = self.indexes.index(index)
		absolute_shift = self.numbers[index]
		self.shiftData(index, absolute_shift)

nums = NumData(numbers)
print(nums.indexes)

for i in range(len(numbers)):
	nums.move(i)
	print(f'move result: {nums.numbers}\n-------\n')
#print(nums.numbers)

def obtainItem(nums:NumData, positive_skip:int):
	index = nums.indexes[0]
	#index = nums.numbers.index(0)
	positive_skip = positive_skip % len(nums.numbers)
	
	if index+positive_skip > len(nums.numbers)-1:
		return nums.numbers[index  - len(nums.numbers)+positive_skip+1]	
	return nums.numbers[index+positive_skip]

print(obtainItem(nums,1000))
print(obtainItem(nums,2000))
print(obtainItem(nums,3000))

print(sum([obtainItem(nums,1000*i) for i in range(1,4)]))
