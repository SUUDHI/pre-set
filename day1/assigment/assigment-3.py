First_input = input("Enter first string:")
Second_input = input("Enter second string:")

len1=len(First_input)
len2=len(Second_input)

if len1 > len2:
    print(f"{First_input} is greter then {Second_input}")

elif len2 > len1 :
    print(f"{Second_input} is greter then {First_input}")

else:
    print (f"{First_input} boyh are equal {Second_input}")

first_diff = ord(First_input[0]) - ord(Second_input[0])
print(f"ASCII Difference ({First_input[0]} - {Second_input[0]}): {first_diff}")


