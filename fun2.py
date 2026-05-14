#!/usr/bin/env python
# 11. LIST COMPREHENSIONS
#from lesson_1_basics import x


print("\n=== LIST COMPREHENSIONS ===")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Traditional way
squares = []
for num in numbers:
    squares.append(num ** 2)
    #add_values.append(num + 2)
add_values = sum(numbers)
print(f"Squares (traditional): {squares}")
print(f"Add values (traditional): {add_values}") 
# print(f"this is a test : {add_values}")

# List comprehension
squares_comp = [num ** 2 for num in numbers]
add_comp = [num+2 for num in numbers]
print(f"Squares (comprehension): {squares_comp}")
print(f" increment by 2 : {add_comp}")

# Conditional list comprehension
even_numbers = [num for num in numbers if num % 2 == 0]
print(f"Even numbers: {even_numbers}") 

temp = [num*8 for num in numbers]
print(f"print temp : {temp}")

temp1 = [num/2 for num in numbers]
print(f"temp1 : {temp1})")


temp3 = [num/5 for num in numbers]
print(f"this is temp3: {temp3}")

temp4 = [num**3 for num in numbers]
print(f"temp4 is:  {temp4}")
"""
def power(x, numbers):
    temp4 = [num**x for num in numbers]
    print(f"temp4 is:  {temp4}")

x=int(input("enter a number to multiply: "))
power(x, numbers)
"""
def power(x):
    temp4 = [num**x for num in numbers]
    print(f"temp4 is:  {temp4}")
 
x = int(input("enter a number to multiply: "))
power(x)