#replace duplicate with (_) Input = [1,2,3,4,3,2,1,4]  output = [1,2,3,4,_,_,_,_]

data = [1,2,3,4,3,2,1,4]

unique = []

for number in data:
    if number not in unique:
        unique.append(number)
    else:
        unique.append("_")

print(unique)
