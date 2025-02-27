Passwd = input("enter a password: ")

passwd_len = len(Passwd) >= 8
Lower_case_check = False
Upper_case_check = False
digit_check = False

for char in Passwd:
    if 'A'<= char <= 'Z':
        Upper_case_check = True

    if 'a'<= char <= 'z':
        Lower_case_check = True

    if '0' <= char <= '9':
        digit_check = True

if passwd_len and Lower_case_check and Upper_case_check and digit_check:
    print("strong password")
else:
    print("week password")
