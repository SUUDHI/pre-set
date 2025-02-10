num = int(input("Enter a number:"))
if num < 0:
    print("enter a positive integer")

else:
    k=0
    while (num > 0):
        digit = num % 10
        k += digit
        num = num // 10
    
print(f"Sum of digits:{k}")
        