"""
Given a list of tuples representing student names and their scores:
students = [("Alice", 85), ("Bob", 78), ("Charlie", 92), ("David", 88)]
Write a Python program to sort the list based on scores in descending order."""
students_1 = [("Alice", 85), ("Bob", 78), ("Charlie", 92), ("David", 88)]
students_1.sort(key=lambda x: x[1],reverse=True)
print(students_1)

students = [("Alice", 85), ("Bob", 78), ("Charlie", 92), ("David", 88)]

# Implementing Bubble Sort
n = len(students)
for i in range(n):
    for j in range(0, n - i - 1):
        if students[j][1] < students[j + 1][1]:  # Comparing scores for descending order
            students[j], students[j + 1] = students[j + 1], students[j]  # Swap

print(students)
