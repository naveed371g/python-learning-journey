#!/usr/bin/env python3

fruits = ["mangoes", "bananas"]
fruit = input("enter a fruit :")

print(fruit)
if fruits[0] == fruit:
	for i in range(3):
		fruits.append("malta")
		print(len(fruits))
		print(fruits)
else:
	print("nothing to add")
	print(fruits)

for fruit in fruits:
	print(fruit)
