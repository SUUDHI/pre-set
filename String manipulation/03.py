# Remove vowels from a string.

def is_vowel(char):
    if char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u':
        return True
    
data = "python prgroamming"

new_data = []

for item in data:
    if is_vowel(item):
        continue
    new_data.append(item)

new_data = ''.join(new_data)

print(new_data)
