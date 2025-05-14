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

def isAnagram3(s, t):
    if len(s) != len(t):
        return False
    
    countS = {}
    countT = {}

    for i in range(len(s)):
        countS[s[i]] = 1 + countS.get(s[i], 0)
        countT[t[i]] = 1 + countT.get(t[i], 0)

    for j in countS:
        if countS[j] != countT.get(j, 0):
            return False
    
    return True

    
print(isAnagram("cat", "bat"))
print(isAnagram3("anagram","nagaram"))