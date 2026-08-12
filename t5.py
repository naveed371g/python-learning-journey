

bill = float(input("enter the bill amount: "))
tip_percent = int(input("enter the tip percentage 5, 10, 15 or more: "))

tip_amount = bill * (tip_percent / 100)
total_bill = bill+tip_amount

print(f"the tip amount is {tip_amount:.2f}")
print(f"the total bill is {total_bill:.2f}")
