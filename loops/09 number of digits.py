#Count the number of digits in a number using a while loop

def count_digits(n):
    count = 0
    n = abs(n) 
    if n == 0:
        return 1  
    
    while n > 0:
        n //= 10  
        count += 1  
    
    return count

num = int(input("Enter a number: "))
print("Number of digits:", count_digits(num))
