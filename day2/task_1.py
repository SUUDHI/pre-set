Enter_number = int(input("enter number to check:"))

if Enter_number % 2 == 0:
    print("{} is an even number.".format(Enter_number))
else:
    print(f"{Enter_number} is an odd number.")
    
if Enter_number % 3 ==0 and Enter_number % 5 == 0:
    print(f"{Enter_number} is divide by both 3 and 5")
    