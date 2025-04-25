# Filter Only Even Numbers

numbers = [1, 2, 3, 4, 5, 6]
# Expected: {2: 4, 4: 16, 6: 36}

result = {num: num ** 2 for num in numbers if num % 2 == 0 }

print(result)
