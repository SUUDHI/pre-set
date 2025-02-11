"""
2. Anagram Detector
Write a program that:
Takes two words as input.
Checks if they are anagrams (contain the same letters but in different orders).
Ignores case differences and spaces.
Example Output:
Enter first word: Listen  
Enter second word: Silent  
The words are anagrams.  
OR
Enter first word: Hello  
Enter second word: World  
The words are not anagrams.  

"""
word1 = input("Enter first word: ")
word2 = input("Enter second word: ")


word1 = word1.replace(" ", "")
word2 = word2.replace(" ", "")

s1=word1.lower()
s2=word2.lower()


if sorted(s1) == sorted(s2):
    print("The words are anagrams.")
else:
    print("The words are not anagrams.")
