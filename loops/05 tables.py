#Print multiplication table of a number entered by the user

x = int(input("enter a number:"))

for i in range(11):
    print(f"{x} X {i} = {x*i}")