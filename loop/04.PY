# Reverse a Number

def rev_number(number):
    rev = 0

    while number > 0:
        digit = number % 10
        rev = rev * 10 + digit  
        number = number // 10            
    return rev

number = 123456
print(rev_number(number))
 