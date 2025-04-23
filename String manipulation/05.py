#Remove duplicate characters from a string
#Input: "programming" → Output: "progamin"

string = "programming"

non_duplicate = ""

for char in string:
    if char not in non_duplicate:
        non_duplicate = non_duplicate + char

print(non_duplicate)
