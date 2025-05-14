import re
"""
A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, 
it reads the same forward and backward. Alphanumeric characters include letters and numbers.

Given a string s, return true if it is a palindrome, or false otherwise.

Example 1:

Input: s = "A man, a plan, a canal: Panama"
Output: true
Explanation: "amanaplanacanalpanama" is a palindrome.
Example 2:

Input: s = "race a car"
Output: false
Explanation: "raceacar" is not a palindrome.
Example 3:

Input: s = " "
Output: true
Explanation: s is an empty string "" after removing non-alphanumeric characters.
Since an empty string reads the same forward and backward, it is a palindrome."""

def isPalindrome(string):
    result = ""
    
    for char in string:
        if char.isalnum():
            result += char.lower()

    reve_result = result[::-1]

    if result == reve_result:
        return True
    else:
        return False

#best on leet code using re.findall
def isPalindrome_2(string):
        string = "".join(re.findall("[a-zA-Z0-9]+", string)).lower()
        return string == string[::-1]

def alphaNum(char):
     return (ord('A') <= ord(char) <= ord('Z') or
             ord('a') <= ord(char) <= ord('z') or
             ord('0') <= ord(char) <= ord('9') )

def isPalindrome_3(string):
    left = 0
    right = len(string) - 1

    while left < right:
        while left < right and not alphaNum(string[left]):
            left += 1
        while right > left and not alphaNum(string[right]):
            right -= 1
        
        if string[left].lower() != string[right].lower():
            return False
        left = left + 1
        right = right - 1
    return True
    
print(isPalindrome_3("mam"))
print(isPalindrome_2("A man, a plan, a canal: Panama"))

print(isPalindrome("race a car"))

print(isPalindrome(" "))