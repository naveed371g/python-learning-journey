import sys

file1 = sys.argv[1]
pattern = sys.argv[2]

with open(file1, 'r') as file:
#	lines = file.readlines()
	for line in file:
		if pattern in line:
			print(f"{line}")	
