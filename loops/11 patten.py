""" *
   ***
  *****
 *******
 """
def print_pyramid(n):
    for i in range(1, n + 1):  
        spaces = ' ' * (n - i)  
        stars = '*' * (2 * i - 1)  
        print(spaces + stars)  

rows = int(input("Enter number of rows: "))
print_pyramid(rows)
