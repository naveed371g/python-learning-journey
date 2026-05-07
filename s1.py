#!/usr/bin/env python3
city = "Sunnyvale"
name = input("enter your name: ")
age = input("enter your age: ")
print(f"my name is {name} and I am {age} years old")
print(input("enter you name: "))"""

print(f"I live in {city}")
for i in range(5):
    print(f"\n{i}")

n1 = 10
n2 = 20
print("add these numbers", n1, "and", n2, "to get", n1 + n2)

text = "python programming"
print(text.upper())
print(len(text))    

fruits = [ "angoor", "malta", "aam"]
print(fruits[-2])
"""
"""
person = {
    "name" : "bilal",
    "age" : 20,
    "city" : "Dehli"
}
print(person)
print(person["name"])
print(f"the city is {person['city']}")
person["country"] = "Afghanistan"
print(person)
person.pop("country")
print(person)
person.pop("state","not found")
print(person)
person["state"] = "Pennsylvania"
print(person)
person.pop("city")
print(person)
if person["name"] == "naveed":
    print("name is naveed")
else:
    print("name is not naveed")
"""
def test():
    print("test1")
    return "test"
print(test())

def add(a,b):
    return a + b
a = input("enter first number: ")
b = input("enter second number: ")
print(add(a,b)) 
