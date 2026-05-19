#!/usr/bin/env python3
import sys

filename = sys.argv[1]


try:
    with open(filename, "r") as file:
        content = file.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("Permission denied!")
except Exception as e:
    print(f"Error: {e}")
else:
    print("File read successfully!")
finally:
    print("File operation complete.")

with open(filename,'r') as file:
    print(f"{file.read()}")
