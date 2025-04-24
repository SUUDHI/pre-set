# Prime number check

number = int(input("Enter Number: "))

def is_prime(number):
    flag = 0
    if number < 1:
        return "number is 1 or less then 1"
    
    for i in range(2,number + 1):
        if number % i == 0:
            flag += 1
        
    if flag == 1:
        return(f"{number} is prime number")
    else:
        return(f"{number} is not a Prime number")

print(is_prime(number))  

