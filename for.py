#!/bin/usr/env python3
for i in range(20,8,-2):
	print(f"{i}")

fruits = ["apple", "banana", "orange", "grape"]
 
for i in range(4):
    print(f"{fruits[i]}")
 
# With index
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

print(fruits)