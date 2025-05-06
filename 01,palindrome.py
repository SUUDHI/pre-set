n1 = 6789
rrev = 0
def is_palindrome(n1):
    n2 = n1
    rev = 0
    while n1 > 0:
        digit = n1 % 10
        rev = rev * 10 + digit
        n1 //= 10
    if n2 == rev:
        return True,rev
    else:
        return False
n2 = 121
#print(is_palindrome(n2))


if (n2 < 0):
    print("False")
k = n2   
print(k) 
rev = 0
while k > 0:
    digit = k % 10
    rev = rev * 10 + digit
    k //= 10
print(rev)
if n2 == rev:
    print("True")
else:
    print("False")


# n3 = str(n2)

# n4 = n3[::-1]
# print(n3)

# if n4 == n3:
#     print(True)
# else:
#     print(False)


