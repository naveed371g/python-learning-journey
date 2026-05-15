#!/usr/bin/env python3
import sys

filename = sys.argv[1]
pattern = sys.argv[2]

with open(filename, 'r') as file:
    for line in file:
        if pattern in line:
           # print(f"FOUND:\n {line.rstrip()}")
            print(f"FOUND: {line}")
# Reading entire file
with open("temp", "r") as file:
        print(f"reading file:\n {file.read()}")