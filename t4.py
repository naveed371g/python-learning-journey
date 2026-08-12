#!/usr/bin/env python3

# 3. Simple Password Generator (Lists & Random Choice)
import random
import string

chars = string.ascii_letters + string.digits + "!@#$"
length = int(input("Enter password length (min 4): "))

# Picks random characters and joins them into one string
password = "".join(random.choice(chars) for i in range(length))
print(f"Your generated password: {password}")
