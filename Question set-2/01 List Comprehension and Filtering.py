#List Comprehension and Filtering
# use list comprehension to create a new list containing only the even numbers.

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_num=[element for element in numbers if element % 2 == 0]

print(even_num)