Enter_number= int(input("Enter a number:"))

if Enter_number < 0:
    print("enter a positive integer")
else:
    Count=0
    while (Enter_number > 0):
        digit = Enter_number % 10
        Count += digit
        Enter_number = Enter_number // 10
    
print(f"Sum of digits:{Count}")
        