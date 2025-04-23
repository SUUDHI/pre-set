#Print a Triangle Pattern
"""
1
12
123
1234
12345
"""

number = int(input("Enter a number: "))

for i in range(number):
    for j in range(1,i+1):
        print(j, end="")
    print("")