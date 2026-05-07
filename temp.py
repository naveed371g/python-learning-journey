def temp_converter():
    print("Temperature Converter")
    print("1. Celsius to Fahrenheit")
    print("2. Fahrenheit to Celsius")
    
    choice = input("Choose: ")
    temp = float(input("Enter temperature: "))
    
    if choice == "1":
        fahrenheit = (temp * 9/5) + 32
        print(f"{temp}°C = {fahrenheit:.2f}°F")
    elif choice == "2":
        celsius = (temp - 32) * 5/9
        print(f"{temp}°F = {celsius:.2f}°C")
 
temp_converter()
