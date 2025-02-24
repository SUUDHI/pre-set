"""
Given a list:
numbers = [1, 2, 3, 2, 4, 5, 1, 6, 7, 8, 5, 9]
Write a Python program to find all duplicate elements and store them in a tuple."""

numbers = [1, 2, 3, 2, 4, 5, 1, 6, 7, 8, 5, 9]

dup=tuple({element for element in numbers if numbers.count(element) > 1})
print(dup)



