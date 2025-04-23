numbers = [1, 2, 3, 2, 4, 5, 1, 6, 7, 8, 5, 9]

dup=tuple({element for element in numbers if numbers.count(element) > 1})
print(dup)
