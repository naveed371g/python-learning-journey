#!/usr/bin/env python3
"""
Reads a file and prints the first column of each line.
Equivalent to: cat temp3 |awk '{print $1}'
"""
import sys
filename = sys.argv[1]
x = int(sys.argv[2])
try:
    with open(filename, 'r') as f:
        for line in f:
            # Split line by whitespace and print first column
            fields = line.split()
            if fields:
                print(fields[x])
except FileNotFoundError:
    print(f"Error: File '{filename}' not found")
except Exception as e:
    print(f"Error: {e}")

