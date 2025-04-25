"""
You are given a list of numbers. Write a dictionary comprehension to create a dictionary where:
The key is the number.
The value is "even" if the number is even, and "odd" if the number is odd.
"""
numbers = [1,2,3,4,5,6,7]

result = {num: 'even' if num % 2 == 0 else 'odd' for num in numbers}

print(result)
