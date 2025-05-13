num = 6789
rrev = 0
num2 = 121

def is_palindrome(num):
    copy_num = num
    rev = 0
    while num > 0:
        digit = num % 10
        rev = rev * 10 + digit
        num //= 10
    if copy_num == rev:
        return True,rev
    else:
        return False

def is_palindrome_2(num):
    if (num2 < 0):
        return False
    copy_num = num2   
    #print(copy_num) 
    rev = 0
    while copy_num > 0:
        digit = copy_num % 10
        rev = rev * 10 + digit
        copy_num //= 10
    #print(rev)
    if num2 == rev:
        return True
    else:
        return False

def is_palindrome_3(num):
    num_str = str(num)

    reverse_str = num_str[::-1]
    #print(num_str)

    if reverse_str == num_str:
        return True
    else:
        return False

print(is_palindrome_2(num2))
print(is_palindrome_3(num2))
