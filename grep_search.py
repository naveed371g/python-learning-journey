#!/usr/bin/env python3
import sys

filename = sys.argv[1]
pattern = sys.argv[2]

with open(filename, 'r') as file:
    for line in file:
        if pattern in line:
            print(line.rstrip())