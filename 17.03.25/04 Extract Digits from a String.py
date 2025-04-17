def isdigit(string):
    digit = []
    for i in string:
        if i > "0" and i <= "9":
            digit.append(i)
    return digit

def isdigit2(s1):
    digit2 = []
    for i in s1:
        if i.isdigit():
            digit2.append(i)
    return(digit2)


string = "asas1213jbdja"
print(isdigit(string))
print(isdigit2(string))
