"""Even or Odd Number Checker  
   - Take an integer as input.  
   - Print whether it's even or odd.  

   Example Output:  
   Enter a number: 7  
   7 is an odd number."""
num = int(input("Enter a number: "))

if num % 2 ==0:
    print(f"{num} is an even number. ")

else:
    print(f"{num} is an odd number.")
    