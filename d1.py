#!/usr/bin/env python3
stocks = {"csco": 55.74, "aapl": 178.50, "msft": 388.15}
stocks["goog"] = 187.50
stocks["aapl"] = 180.00
stocks["netpp"] = 200.00
price = stocks.get("netpp")
price = stocks.pop("netpp") 
print(price)    
print(stocks)
if "dell" in stocks:
        print("Dell is in the stocks dictionary")
else:
    print("Dell is not in the stocks dictionary")
keys = stocks.keys()  # All stock symbols
values = stocks.values()  # All prices
items = stocks.items()  # Both as tuples
print(keys)
print(values)
print(items)    
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    