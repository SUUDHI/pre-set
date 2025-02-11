"""1. Advanced Number Manipulation
Write a Python program that:
Takes a number as input.
Checks if the number is prime.
Finds and prints the sum of all digits in the number.
Reverses the number and checks if it's a palindrome.
Example Output:
Enter a number: 131  
131 is a prime number.  
Sum of digits: 5  
131 is a palindrome.  
"""
num1 = input("enter a number: ")
#primr check
num = int(num1)
flag=0
i=1
while i<=num:
    if num % i ==0:
        flag=flag+1
    i=i+1
if flag==2:
    print(f"{num} is an primr number.")
else:
    print(f"{num} is not an prime number.")

#sum of digits
sum=0
while num >0:
    dig = num % 10
    sum += dig
    num = num // 10
print(f"Sum of digits: {sum}")

#palindrome
num_0=int(num1)
num_01=int(num1)
rev=0

while num_0 > 0:
    last = num_0 % 10
    rev=rev * 10 + last
    num_0= num_0 //10

if num_01 == rev:
    print(f"{num1} is an palindrome.")
else:
    print(f"{num1} is not a palindrome.")
  