# Remove vowels from a string.

string = "python programming"

vowels = "AEIOUaeiou"

for item in string:
    if item in vowels:
        string = string.replace(item,"")

print(string)
