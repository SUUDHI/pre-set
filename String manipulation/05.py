#Remove duplicate characters from a string
#Input: "programming" → Output: "progamin"

string = "programming"

non_duplicate = ""

for i in string:
    if i not in non_duplicate:
        non_duplicate = non_duplicate + i

print(non_duplicate)