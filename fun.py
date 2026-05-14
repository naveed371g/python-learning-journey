#!/usr/bin/env python3

"""
def test(a,b):
    a=10
    b=20
    return (a,b)


result = test(1,2)
print(result)


def fruits(a,b):
    a = "apple"
    b = "banana"    
    return (a,b)

print(fruits(1,2))



def stock(a,b):
   a = 7
   b = 4
   c = 550
   if a > b:
       return (a,b)
   else:
       return (b,a)

print(stock(1,2))


def greet (name):
    print(f"hello my name is {name}")

greet("Naveed")
"""

"""
def new(apple, banana):
    apple = 6
    banana = 14 
    if apple > banana:
        return ("apple", "banana")
    else:
        return ("banana", "apple")

result = new(6,14)
print(result)
"""
"""
global_var = "APPLE"
def test():
    localvar = "MANGO"
    print(f"inside the function global: {global_var}")
    print(f"inside the function local: {localvar}")
    return localvar
    
print(f"outside the function global: {global_var}")
localvar = test()
print(f"outside the function local: {localvar}")

"""
""" 
def print_message(message):
    print(f"Message: {message}")
    # No return statement
print_message("Hello World")

"""
"""
def celtofar(cel):
    far = cel * 9/5 + 32
    return far

result = celtofar(5)
print(result)

def fartocel(far):
    cel = (far - 32) * 5/9
    return cel
temp = input("Please enter temperature in Fahrenheit:")
result = fartocel(float(temp))
print(f"{result:.2f} degrees Celsius")

"""
"""
print(f"\nExercise 5: Password Strength")
password = input("Enter password: ")
# print(f"Input: {password}")

if len(password) < 8:
    strength = "Weak"
elif len(password) < 12:
    strength = "Medium"
else:
    strength = "Strong"

print(f"  Password: {'*' * len(password)}")
print(f"  Strength: {strength}")

"""
"""
def name(x,y):
    z = x + y
    print(z)
x=int(input("Enter first number: "))
y=int(input("Enter second number: "))
name(x,y)
"""
"""
#from lesson_1_basics import x


def temp(x):
    if x < 0:
        print("its cold")
    elif x > 40:
        print("its hot")

temp(-1)
"""

def temp(x):
    if x < 0:
        print("its cold")
    elif x > 40:
        print("its hot")
    else:
        print("its moderate")
x=input("Press enter a number: ")
temp(int(x))

