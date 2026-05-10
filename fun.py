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

def print_message(message):
    print(f"Message: {message}")
    # No return statement
print_message("Hello World")
