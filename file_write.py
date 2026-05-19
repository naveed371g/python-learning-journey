#!/usr/bin/env python3

with open("file.txt",'a') as file:
	file.write("this is a test\n")
	file.write("more to write\n")

with open("file.txt",'r') as file:
	print(file.read())

