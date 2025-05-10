#Count Vowels in a String:
#Write a function that counts the number of vowels in a given string

def count(string):
    vowels = "aeiouAEIOU"
    count = 0
    for i in string:
        if i in vowels:
            count += 1
    return count

string =  input("Enter a string: ")

print(count(string))
