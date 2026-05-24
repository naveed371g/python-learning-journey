#!/usr/bin/env python3

# Basic class definition
class Person:
    def __init__(self, name, age):
        """Constructor method"""
        self.name = name
        self.age = age
    
    def greet(self):
        """Instance method"""
        return f"Hello, I'm {self.name} and I'm {self.age} years old!"
        

# Creating objects (instances)
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)
 
# Using objects
print(person1.greet())  # Hello, I'm Alice and I'm 25 years old!
print(person2.greet())  # Hello, I'm Bob and I'm 30 years old!

