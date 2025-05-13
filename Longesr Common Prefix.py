"""
Input: strs = ["flower","flow","flight"]
Output: "fl"""

strs = ["flower","flow","flight"]

#Total Time Complexity: O(n * m)
def  longestCommonPrefix_1(strs):
    CommonPrefix = ""

    for char in range(len(strs[0])):
        for s in strs:
            if char == len(s) or s[char] != strs[0][char]:
                return CommonPrefix

        CommonPrefix += strs[0][char]
    return CommonPrefix

 #Total Time Complexity: O(n * m²)       
def longestCommonPrefix_2(strs):
        if not strs:
            return ""
        prefix = strs[0]
        for string in strs[1:]:
            while string.find(prefix) != 0:
                prefix = prefix[:-1]
                if not prefix:
                    return ""
        return prefix

print( longestCommonPrefix_1(strs))
print(longestCommonPrefix_2(strs))
