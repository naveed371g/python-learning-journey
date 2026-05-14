#!/usr/bin/env python3
"""
PYTHON EXAMPLES COLLECTION - All lessons covered so far
Save this file for practice tonight!
"""

print("=" * 60)
print("PYTHON EXAMPLES COLLECTION")
print("=" * 60)

# ==================== LESSON 1: VARIABLES AND DATA TYPES ====================
print("\n📚 LESSON 1: VARIABLES AND DATA TYPES")
print("-" * 50)

# Variables
name = "Alice"
age = 25
height = 5.8
price = 19.99
is_student = True
has_car = False

print(f"Name: {name}")
print(f"Age: {age}")
print(f"Height: {height} feet")
print(f"Price: ${price}")
print(f"Is student: {is_student}")
print(f"Has car: {has_car}")

# Math operations
a = 10
b = 3
print(f"\nMath: {a} + {b} = {a + b}")
print(f"Math: {a} * {b} = {a * b}")
print(f"Math: {a} / {b} = {a / b:.2f}")

# String operations
text = "python programming"
print(f"\nString: {text}")
print(f"Uppercase: {text.upper()}")
print(f"Length: {len(text)} characters")

# ==================== LESSON 2: CONTROL FLOW ====================
print("\n📚 LESSON 2: CONTROL FLOW")
print("-" * 50)

# Example 1: Basic if/else
temperature = 10
weather = "sunny"

print(f"\nWeather Check - Temperature: {temperature}°C, Weather: {weather}")

if temperature > 30 and weather == "sunny":
    print("🌞 It's hot and stay hydrated")
elif temperature > 20 and weather == "sunny":
    print("🌞 It's perfect for walk")
else:
    print("🌧️ Don't walk")

# Example 2: Grade calculator
score = 85
print(f"\nGrade Calculator - Score: {score}")

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Grade: {grade}")

# Example 3: For loop with range
print(f"\nCounting 1 to 5:")
for i in range(1, 6):
    print(f"  {i}")

# Example 4: For loop with list
fruits = ["apple", "banana", "orange", "grape"]
print(f"\nFruits loop:")
for fruit in fruits:
    print(f"  🍎 {fruit}")

# Example 5: While loop
print(f"\nCountdown:")
countdown = 5
while countdown > 0:
    print(f"  {countdown}...")
    countdown -= 1
print("  🚀 Blast off!")

# Example 6: Loop control
print(f"\nFind first even number:")
numbers = [1, 3, 5, 7, 8, 9, 11, 12]

for num in numbers:
    if num % 2 == 0:
        print(f"  Found first even number: {num}")
        break
    print(f"  Checking {num}... odd")

# ==================== PRACTICE EXERCISES ====================
print("\n📚 PRACTICE EXERCISES")
print("-" * 50)

# Exercise 1: Age checker
print(f"\nExercise 1: Age Checker")
user_age = 17

if user_age >= 18:
    print("✅ You can vote!")
else:
    print("❌ You're too young to vote")
    years_to_wait = 18 - user_age
    print(f"   Wait {years_to_wait} more years")

# Exercise 2: Even/Odd checker
print(f"\nExercise 2: Even/Odd Checker")
for num in range(1, 11):
    if num % 2 == 0:
        print(f"  {num} is even")
    else:
        print(f"  {num} is odd")

# Exercise 3: Shopping cart
print(f"\nExercise 3: Shopping Cart")
items = [
    {"name": "Laptop", "price": 999.99},
    {"name": "Mouse", "price": 29.99}
]

total = sum(item["price"] for item in items)
print(f"  Cart total: ${total:.2f}")

if total >= 1000:
    print("  🎉 Free shipping!")
else:
    shipping = 9.99
    print(f"  📦 Shipping: ${shipping:.2f}")
    print(f"  Final total: ${total + shipping:.2f}")

# Exercise 4: Temperature converter
print(f"\nExercise 4: Temperature Converter")
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"  {celsius}°C = {fahrenheit:.1f}°F")

if fahrenheit > 90:
    print("  🔥 Very hot!")
elif fahrenheit > 70:
    print("  😊 Warm")
else:
    print("  ❄️ Cold")

# Exercise 5: Password strength checker
print(f"\nExercise 5: Password Strength")
password = "python123"

if len(password) < 8:
    strength = "Weak"
elif len(password) < 12:
    strength = "Medium"
else:
    strength = "Strong"

print(f"  Password: {'*' * len(password)}")
print(f"  Strength: {strength}")

# ==================== TEMPLATES FOR PRACTICE ====================
print("\n📚 TEMPLATES FOR PRACTICE")
print("-" * 50)

print("""
# Template 1: Basic if/else
# Copy and modify this template
number = 10

if number > 0:
    print("Positive")
elif number < 0:
    print("Negative")
else:
    print("Zero")

# Template 2: For loop
# Copy and modify this template
my_list = ["item1", "item2", "item3"]

for item in my_list:
    print(f"Processing: {item}")

# Template 3: While loop
# Copy and modify this template
counter = 0
while counter < 5:
    print(f"Count: {counter}")
    counter += 1

# Template 4: Nested conditions
# Copy and modify this template
age = 25
has_license = True

if age >= 18:
    if has_license:
        print("Can drive")
    else:
        print("Needs license")
else:
    print("Too young to drive")
""")

# ==================== CHAPTER 4 EXTRA PRACTICE ====================
print("\n📚 CHAPTER 4: EXTRA CONTROL FLOW PRACTICE")
print("-" * 50)

# Practice 1: Grade calculator
print("\nPractice 1: Grade Calculator")
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"  Score: {score}")
print(f"  Grade: {grade}")

# Practice 2: Number guessing logic
print("\nPractice 2: Number Range Checker")
secret_number = 42
guess = 35

if guess == secret_number:
    print("  🎉 Correct!")
elif abs(guess - secret_number) <= 5:
    print("  🔥 Very close!")
elif abs(guess - secret_number) <= 10:
    print("  👍 Close")
else:
    print("  ❄️ Far off")

# Practice 3: For loop with range
print("\nPractice 3: Multiplication Table")
number = 7
for i in range(1, 6):
    result = number * i
    print(f"  {number} × {i} = {result}")

# Practice 4: While loop with condition
print("\nPractice 4: Countdown Timer")
countdown = 5
while countdown > 0:
    print(f"  T-minus {countdown}...")
    countdown -= 1
print("  🚀 Launch!")

# Practice 5: Nested loops
print("\nPractice 5: Pattern Printing")
for row in range(3):
    line = ""
    for col in range(row + 1):
        line += "* "
    print(f"  {line}")

# Practice 6: List comprehension
print("\nPractice 6: Even Numbers Filter")
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = [num for num in numbers if num % 2 == 0]
print(f"  Original: {numbers}")
print(f"  Even: {even_numbers}")

# Practice 7: Break and continue
print("\nPractice 7: Loop Control")
for i in range(1, 11):
    if i == 7:
        print(f"  Skipping {i} (continue)")
        continue
    if i == 9:
        print(f"  Stopping at {i} (break)")
        break
    print(f"  Processing {i}")

# Practice 8: Multiple conditions
print("\nPractice 8: Login Validation")
username = "admin"
password = "secret123"
is_active = True

if username == "admin" and password == "secret123" and is_active:
    print("  ✅ Login successful - Admin access")
elif username and password:
    print("  ⚠️ Login successful - Limited access")
else:
    print("  ❌ Login failed")

# ==================== DUMMY EXAMPLES ====================
print("\n📚 DUMMY EXAMPLES FOR PRACTICE")
print("-" * 50)

# Dummy 1: Simple variables
print("\nDummy 1: Basic Variables")
name = "John Doe"
age = 30
city = "New York"
print(f"  Name: {name}")
print(f"  Age: {age}")
print(f"  City: {city}")

# Dummy 2: Simple math
print("\nDummy 2: Basic Math")
x = 15
y = 3
print(f"  {x} + {y} = {x + y}")
print(f"  {x} - {y} = {x - y}")
print(f"  {x} * {y} = {x * y}")
print(f"  {x} / {y} = {x / y}")

# Dummy 3: String operations
print("\nDummy 3: String Operations")
first_name = "Alice"
last_name = "Smith"
full_name = first_name + " " + last_name
print(f"  First: {first_name}")
print(f"  Last: {last_name}")
print(f"  Full: {full_name}")

# Dummy 4: Simple list
print("\nDummy 4: Basic List")
fruits = ["apple", "banana", "orange", "grape"]
print(f"  Fruits: {fruits}")
print(f"  First fruit: {fruits[0]}")
print(f"  Last fruit: {fruits[-1]}")
print(f"  Number of fruits: {len(fruits)}")

# Dummy 5: Simple if statement
print("\nDummy 5: Basic If Statement")
temperature = 25
if temperature > 20:
    print("  It's warm today!")
else:
    print("  It's cold today!")

# Dummy 6: Simple for loop
print("\nDummy 6: Basic For Loop")
colors = ["red", "green", "blue"]
for color in colors:
    print(f"  Color: {color}")

# Dummy 7: Simple while loop
print("\nDummy 7: Basic While Loop")
count = 0
while count < 3:
    print(f"  Count: {count}")
    count += 1

# Dummy 8: Simple function
print("\nDummy 8: Basic Function")
def greet(person):
    return f"Hello, {person}!"

message = greet("World")
print(f"  {message}")

# Dummy 9: Simple boolean
print("\nDummy 9: Boolean Logic")
is_raining = True
has_umbrella = False

if is_raining and not has_umbrella:
    print("  You'll get wet!")
else:
    print("  You'll stay dry!")

# Dummy 10: Simple input/output
print("\nDummy 10: Input/Output Simulation")
user_input = "Python"
print(f"  You entered: {user_input}")
print(f"  Length: {len(user_input)} characters")

print("\n" + "=" * 60)
print("EXAMPLES COLLECTION COMPLETE!")
print("💡 Practice these examples tonight!")
print("📝 Try modifying values and adding your own logic")
print("🚀 Ready for Lesson 3: Data Structures tomorrow!")
print("=" * 60)
