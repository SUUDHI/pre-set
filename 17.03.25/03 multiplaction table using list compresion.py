r = int(input("enter number: "))

table = [[i * j for j in range(1, 11)] for i in range(1, r+1)]
print(table)