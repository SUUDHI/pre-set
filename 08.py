numbers = [1, 2, 3, 4, 5]
# Expected: {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

result = {num: num*num for num in numbers }

print(result)
