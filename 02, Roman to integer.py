"""Symbol       Value
I             1
V             5
X             10
L             50
C             100
D             500
M             1000
"""
def roman_to_int(roman_num):
    roman = {"I" : 1, "V" : 5, "X" : 10, "L" : 50, "C" : 100, "D" : 500, "M" : 1000 }

    res = 0
    for char in range(len(roman_num)):
        if char + 1 < len(roman_num) and roman[roman_num[char]] < roman[roman_num[char + 1]]:
            res = res - roman[roman_num[char]]
        else:
            res = res + roman[roman_num[char]]
    
    return res

print(roman_to_int("V"))
