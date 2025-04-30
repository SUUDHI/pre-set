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

def manual_split(sentance):
    splited_sen = []
    word = ""
    for char in sentance:
        if char != " ":
            word += char
        else:
            if word:
                splited_sen.append(word)
                word = ""       
    if word:
        splited_sen.append(word)

    return splited_sen


# with [-1]
def len_last(sentance):
    splited_sent = manual_split(sentance)
    return len(splited_sent[-1])

#without using [-1]
def len_last1(sentance):
    splited_sen = manual_split(sentance)
    last_word = splited_sen[len(splited_sen) - 1]
    return len(last_word)

sentance = "hellow world"
print(len_last(sentance))

s = "   fly me   to   the moon  "
print(len_last1(s))
