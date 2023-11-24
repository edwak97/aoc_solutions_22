lines = []
with open('input.txt', 'r') as file_origin: 
		lines = file_origin.readlines()

class XYZ_object:
	def __init__(self, item:tuple):
		self.item = (int(item[0]), int(item[1]), int(item[2]))

xyz_items = [XYZ_object(tuple(line.strip().split(','))) for line in lines]

#to have common surface two xyz-objects must have two equal coordinates
#since xyz indexes are 0,1,2 respectively: we need to group them by xy, xz, yz ((0,1),(0,2),(1,2))

collisions = 0;

for i in range(3):
	#indexes to compare:
	itc = tuple([k for k in range(3) if k != i])
	
	#need to find all xyz-objects having the same coordinates on itc[0] and itc[1]
	#finding all unique itc[0], itc[1] pairs and using it as dictionary keys:	
	#when it is grouped we need to sort itc_dict[key] values by i coordinate

	itc_dict = {(xyz_item.item[itc[0]], xyz_item.item[itc[1]]):sorted([_xyz_item.item[i] for _xyz_item in xyz_items if (_xyz_item.item[itc[0]],_xyz_item.item[itc[1]]) == (xyz_item.item[itc[0]], xyz_item.item[itc[1]])], key=lambda x:x) for xyz_item in xyz_items}
	
	itc_values = [itc_dict[key] for key in itc_dict]
	del(itc_dict)

	for itc_value in itc_values:
		for c,value in enumerate(itc_value):
			if c == 0:
				continue
			if(value - itc_value[c-1] == 1):
				collisions += 1

print(len(xyz_items)*6 -collisions*2)
	
	#the_res = [item[i] for val in itc_dict.items() for
	
