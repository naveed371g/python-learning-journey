#!/usr/bin/env python3

import time
seconds = int(input("enter numbers in sec: "))

for i in range(seconds, 0, -1):
    print(f"start counting down {i}")
    time.sleep(2)

print("we are done ")
