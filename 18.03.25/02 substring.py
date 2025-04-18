# Print those string that are a substring in other

string = ["mass","as","hero","superhero","mass","per"]
sub_string = []
for i in string:
    for j in string:
        if j != i and j in i:
            sub_string.append(j)

print(sub_string)
