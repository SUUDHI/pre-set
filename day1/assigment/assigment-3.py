""" String Length & ASCII Difference Challenge
Take two string inputs.
Compare their lengths and print which is longer.
Calculate the ASCII difference between the first character of both strings.
Example Output:
Enter first string: Hello
Enter second string: World
Both strings have the same length: 5
ASCII Difference (H - W): -15
(Hint: Use  ord() to get ASCII values.)"""
s = input("Enter first string:")
u = input("Enter second string:")

len1=len(s)
len2=len(u)

if len1 > len2:
    print(f"{s} is greter then {u}")

elif len2 > len1 :
    print(f"{u} is greter then {s}")

else:
    print (f"{s} boyh are equal {u}")

first_diff = ord(s[0]) - ord(u[0])
print(f"ASCII Difference ({s[0]} - {u[0]}): {first_diff}")


