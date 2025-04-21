#Flatten a 2D list

list = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in list for num in row]
print(flat)
