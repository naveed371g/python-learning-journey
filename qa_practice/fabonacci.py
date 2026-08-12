
def fibonacci(count):
    a, b = 0, 1
    for _ in range(count): # _ mean it does not care iteration number, you can also use 'for i in range(count)
        yield a            # yeild is like return but it return one at a time whereas return produces at once
        a, b = b, a + b

print(f"  First 8 Fibonacci: {list(fibonacci(8))}")
