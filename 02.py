"""
Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6."""

def length_of_last_word(sentance):
    split_string = sentance.split()
    last_word = split_string[-1]
    return len(last_word)


def length_Of_Last_Word_2(sentence):
    words = sentence.strip().split(" ")
    last_word = words[-1]
    return len(last_word)


sentance = "luffy is still joyboy"
sentance1 = "   fly me   to   the moon  "

print(length_of_last_word(sentance))
print(length_of_last_word(sentance1))

print(length_Of_Last_Word_2(sentance))
print(length_Of_Last_Word_2(sentance1))
