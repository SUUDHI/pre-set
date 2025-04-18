#Use a lambda function with the map function to square each number in a given list.

lst = [1,2,3,4,5]

squre = list(map(lambda y: y*y, lst))

print(squre)
