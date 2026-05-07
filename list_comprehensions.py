#!/usr/bin/env python3
"""
List Comprehensions - Advanced Python
"""

def list_comprehensions_examples():
    print("=== List Comprehensions Examples ===\n")
    
    # Basic list comprehension
    numbers = [1, 2, 3, 4, 5]
    squares = [x**2 for x in numbers]
    print(f"Original: {numbers}")
    print(f"Squares: {squares}")
    print()
    
    # With condition
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    print(f"Even squares: {even_squares}")
    print()
    
    # String manipulation
    words = ["python", "is", "fun", "learning"]
    uppercase_words = [word.upper() for word in words]
    print(f"Uppercase: {uppercase_words}")
    print()
    
    # Nested list comprehension
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    print(f"Matrix: {matrix}")
    print(f"Flattened: {flattened}")
    print()
    
    # Practice exercise
    print("=== Practice Exercise ===")
    user_numbers = input("Enter numbers separated by spaces: ").split()
    try:
        nums = [int(num) for num in user_numbers]
        doubled = [num * 2 for num in nums if num > 0]
        print(f"Positive numbers doubled: {doubled}")
    except ValueError:
        print("Please enter valid numbers")

if __name__ == "__main__":
    list_comprehensions_examples()
