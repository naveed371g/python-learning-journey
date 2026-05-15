#!/usr/bin/env python3
import sys

filename = sys.argv[1]

with open(filename, 'r') as file:
    for line in file:
        fields = line.split()
        if fields:
            print(fields[0])
