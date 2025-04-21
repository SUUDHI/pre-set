table_till = int(input("enter number: "))

table = [[i * j for j in range(1, 11)] for i in range(1, table_till+1)]
print(table)