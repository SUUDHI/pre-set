students = [
    {"name": "Alice", "age": 25, "grade": "A"},
    {"name": "Bob", "age": 22, "grade": "B"},
    {"name": "Charlie", "age": 23, "grade": "C"}
]

sorted_dicts = sorted(students, key = lambda x: x["age"] ) 

print(sorted_dicts)
