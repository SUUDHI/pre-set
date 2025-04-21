def check_digit(string):
    digit = []
    for char in string:
        if char > "0" and char <= "9":
            digit.append(char)
    return digit

def check_digit_2(string):
    digit2 = []
    for char in string:
        if char.isdigit():
            digit2.append(char)
    return(digit2)


raw_data = "asas1213jbdja"
print(check_digit(raw_data))
print(check_digit_2(raw_data))
