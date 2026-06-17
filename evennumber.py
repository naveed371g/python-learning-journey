
#!/usr/bin/env python3

numbers = [1, 3, 5, 7, 8, 9, 11, 12]
odd_numbers = []
even_numbers = []
 
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
        print(f"Even: {num}")
    else:
        odd_numbers.append(num)
        print(f"Odd: {num}")
 
print(f"\nAll odd numbers: {odd_numbers}")
print(f"All even numbers: {even_numbers}")