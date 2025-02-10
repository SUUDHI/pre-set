"""Reverse a Number Without Using Strings  
   - Take a number as input.  
   - Reverse the number using a while loop (without converting it to a string).  

   Example Output:  
   Enter a number: 1234  
   Reversed number: 4321"""
num = int(input("Enter a number: "))

reversed_num = 0

while num > 0:
      dig = num % 10
      reversed_num = reversed_num * 10 + dig
      num = num // 10

print("Reversed number:", reversed_num)