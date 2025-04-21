# Remove vowels from a string.

string = "python programming"

vowels = "AEIOUaeiou"

for i in string:
    if i in vowels:
        string = string.replace(i,"")

print(string)
