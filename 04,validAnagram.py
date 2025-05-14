"""
Given two strings s and t, return true if t is an anagram of s, and false otherwise.
Example 1:
Input: s = "anagram", t = "nagaram"
Output: true
Example 2:
Input: s = "rat", t = "car"
Output: false

 """
def isAnagram(string1, string2):
    if len(string1) != len(string2):
        return False
    return sorted(string1.lower()) == sorted(string2.lower())

def isAnagram2(string1, string2):
    if len(string1) != len(string2):
        return False
    sorted_string1 = sorted(string1)
    sorted_string2 = sorted(string2)

    return sorted_string1 == sorted_string2

def isAnagram3(string_1, string_2):
    if len(string_1) != len(string_2):
        return False
    
    countString_1 = {}
    countString_2 = {}

    for char in range(len(string_1)):
        countString_1[string_1[char]] = 1 + countString_1.get(string_1[char], 0)
        countString_2[string_2[char]] = 1 + countString_2.get(string_2[char], 0)

    for char in countString_1:
        if countString_1[char] != countString_2.get(char, 0):
            return False
    
    return True

    
print(isAnagram("cat", "bat"))
print(isAnagram3("anagram","nagaram"))