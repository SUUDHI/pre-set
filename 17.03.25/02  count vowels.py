#Count Vowels in a String:
#Write a function that counts the number of vowels in a given string

# Total time complexity of this is O(n),
def count_vowels1(string):
    vowels = "aeiou"

    count = 0
    for i in string:
        if i in vowels:
            count += 1
    return count

string =  "SUREASHAA"
string_lower = string.lower()

print(count_vowels1(string_lower))

# Total time complexity of this is O(n),
def is_vowel(char):
    if char == 'a' or char == 'e' or char == 'i' or char == 'o' or char == 'u':
        return True

def count_vowels2(vowel):
    count = 0
    for char in vowel:
        if is_vowel(char):
            count += 1
    return count

string_new =  "sUSdhanshu"
srting_lower2 = string_new.lower()

print(count_vowels2(srting_lower2))

# using set for the for looping for faster loop
def count_vowels3(vowel):
    vowels = {'a', 'e', 'i', 'o', 'u'}  
    count = 0
    for char in string.lower():        
        if char in vowels:
            count += 1
    return count

string = "SUREASHAA"
print(count_vowels3(string))
