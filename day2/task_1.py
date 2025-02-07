"""
Task 1: Even/Odd & Divisibility Check
Write a program that:
Takes an integer input from the user.
Checks if the number is even or odd using % modulus operator.
Checks if the number is divisible by both 3 and 5 using and operator.
Example Output:
Enter a number: 15  
15 is an odd number.  
15 is divisible by both 3 and 5.  
"""
num = int(input("enter number to check:"))

if num % 2 == 0:
    print("{} is an even number.".format(num))

else:
    print(f"{num} is an odd number.")

if num % 3 ==0 and num % 5 == 0:
    print(f"{num} is divide by both 3 and 5")