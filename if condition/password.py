"""Take a password input and check if it meets these conditions:

At least 8 characters

Contains both uppercase and lowercase letters

Includes at least one digit

"""
def password_check(x):
    has_lower = False
    has_upper = False
    has_8char = len(x) >= 8

    for char in x:
        if 'A'<= char <= 'Z':
            has_upper = True
        if 'a' <= char <= 'z':
            has_lower = True
        
    if has_upper and has_lower and has_8char:
        print("strong password")
    else:
        print("no input again")

password = input("entaer a password:")

password_check(password)