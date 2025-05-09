"""
Example 1:

Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
Example 2:

Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1."""

haystack = "butsad"
needle = "sad"

def remove_first(haystack, needle):
    for i in range(len(haystack)):
        if haystack[i] == needle[0] and haystack[i+1] == needle[1] and haystack[i+2] == needle[2]:
            return i
        
    return -1


print(remove_first(haystack, needle))

#this is the fastast approch for this question
def remove_first01(str, rem):
    return str.find(rem)

print(remove_first01(haystack, needle))

#
def remove_first02(str,rem):
    if str == rem:
        return 0

    n = len(str)
    left = 0
    right = len(rem)
    index = 0

    while(left < n and right < n + 1):
        sub = str[left : right]
        if sub == rem:
            return index
        index += 1
        left += 1
        right += 1
    
    return -1

print(remove_first02(haystack,needle))
