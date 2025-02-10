"""Prime Number Checker  
   - Take a number as input.  
   - Check whether it is prime using a for loop.  

   Example Output:  
   Enter a number: 11  
   11 is a prime number."""
num = int(input("Enter a number: "))

if num < 2:
    print("enter number is 1 or less then 1")

else:
    i=1
    flag=0
    while i<=num:
        if num % i ==0:
            flag=flag+1
        i=i+1
    if flag ==2:
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is nat a prime number.")
        


        