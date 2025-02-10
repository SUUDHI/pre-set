"""
 Multiplication Table Generator  
   - Take a number as input.  
   - Print its multiplication table up to 10.  

   Example Output:  
   Enter a number: 5  
   5 x 1 = 5  
   5 x 2 = 10  
   ...  
   5 x 10 = 50  
"""
num = int(input("Enter A Number: "))

i=1
while(i<=10):
    print(f"{num} * {i} = {num*i}")
    i=i+1