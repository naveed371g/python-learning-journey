
def apply_operation(numbers, operation):
    """Apply operation to each number in list"""
    results = []
    for num in numbers:
        results.append(operation(num))
    return results
 
def square(x):
    return x * x
 
def double(x):
    return x * 2
 
# Using functions as parameters
numbers = [1, 2, 3, 4, 5]
squared = apply_operation(numbers, square)    # [1, 4, 9, 16, 25]
doubled = apply_operation(numbers, double)    # [2, 4, 6, 8, 10]
print(f"Original: {numbers}")
print(f"Squared: {squared}")
print(f"Doubled: {doubled}")