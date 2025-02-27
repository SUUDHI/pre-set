Input_word_01 = input("Enter first word: ")
Input_word_02 = input("Enter second word: ")

Input_word_01 = Input_word_01.replace(" ", "")
Input_word_02 = Input_word_02.replace(" ", "")

Sorted_word_01=Input_word_01.lower()
Sorted_word_02=Input_word_02.lower()

if sorted(Sorted_word_01) == sorted(Sorted_word_02):
    print("The words are anagrams.")
else:
    print("The words are not anagrams.")
