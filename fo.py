# This test will open a file to read

#!/usr/bin/env python3
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
