#word location in the string

data = "python is best for Ai and Ml"

find = "Ai"

splited_data = data.split()

for index in range(len(splited_data)):
    if splited_data[index] == find:
        print(f"Index is {index} and Word is {splited_data[index]}")
    