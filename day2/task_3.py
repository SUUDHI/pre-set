"""
Task 3: Password Strength Checker
Write a program that:
Takes a password input from the user.
Checks and prints whether the password is strong or weak based on:
At least 8 characters long
Contains both uppercase and lowercase letters
Includes at least one number
Example Output:
Enter a password: Hello123  
Your password is strong!  
"""
passwd = input("enter a password: ")

passwd_len = len(passwd) >= 8
low_check = False
up_check = False
dig_check = False

for char in passwd:
    if 'A'<= char <= 'z':
        up_check = True

    if 'a'<= char <= 'z':
        low_check = True

    if '0' <= char <= '9':
        dig_check = True

if passwd_len and low_check and up_check and dig_check:
    print("strong password")

else:
    print("week password")
