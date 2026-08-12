
from collections import Counter
text = "this is a long line to read"
tosplit = text.split()


# this will create tosplit file to ["this", "is", "a", "long", "line", "to", "read"]

print(tosplit)

# to bring the file back from array to a line text
tojoin = " ".join(tosplit)
print(tojoin)

# Reverse words in a sentence


def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])


# count number of alphabet
forcount = "aabbcdbbxyz"
print(forcount.count("a"))

# counting each letter
temp = "sdsssdraaasfaa"
temp = Counter(temp)
print(temp)
for key, value in temp.items():
    print(f"{key} {value}")

# will print each letter and number in front a 5, s 5 and so on


# strip will remove all accidental spaces

text = "   Hello, World .  "
cleaned_text = text.strip()
print(f"orignal text,{text}")
print(f"clean text, {cleaned_text}")


# will sort the array
first = ["banana", "cherry", "mango", "apple"]
after_sort = sorted(first)
print("before sort", first)
print("after sort", after_sort)


# These two are same:
arr = [x for x in range(5)]

# SAME as
arr1 = []
for x in range(5):
    arr1.append(x)

# Count the number in arr
# means it will count 1 time in array and output is 6
arr3 = sum([1 for x in arr1])
# same as
arr4 = len(arr1)  # output is 6

# list
fruits = ["apple", "banana", "pine", "graps"]
for index, fruit in enumerate(fruits):
    print(f"{index} {fruit}")

# will print 0 apple
#            1 banana and so on

# dictionary
person = {"name": "eric", "age": 10, "city": "SFO"}
for key, value in person.items():
    print(f"{key} {value}")
# will print
# name eric
# age 10
# city SFO

# for adding
i = 0
while i < 5:
    print(i)
    i += 1  # incrementing one to i

# adding subtotal
items = [
    {"name": "Laptop", "price": 999.99},
    {"name": "Mouse", "price": 29.99},
    {"name": "Keyboard", "price": 79.99}
]

subtotal = sum(item["price"] for item in items)
print(f"Subtotal: ${subtotal:.2f}")

# same as above but long
i = 0
total = 0
for item in items:
    total = total + (items[i]["price"])
    i += 1

print(total)
