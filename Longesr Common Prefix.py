"""
Input: strs = ["flower","flow","flight"]
Output: "fl"""

strs = ["flower","flow","flight"]

#Total Time Complexity: O(n * m)
def long(strs):
    lon = ""

    for i in range(len(strs[0])):
        for s in strs:
            if i == len(s) or s[i] != strs[0][i]:
                return lon

        lon += strs[0][i]
    return lon

 #Total Time Complexity: O(n * m²)       
def longestCommonPrefix(strs):
        if not strs:
            return ""
        prefix = strs[0]
        for string in strs[1:]:
            while string.find(prefix) != 0:
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

print(long(strs))
print(longestCommonPrefix(strs))
