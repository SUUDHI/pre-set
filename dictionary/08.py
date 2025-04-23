# Check Anagrams using Dictionary

# Input: "listen", "silent"
# Output: True

def is_anagram(str1,str2):
    freq = {}

    if len(str1) != len(str2):
        return False
    
    for char in str1:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    
    for char in str2:
        if char not in freq:
            return False
        freq[char] -= 1

        if freq[char] < 0:
            return False

    return True

word_1 = 'listen'
word_2 = 'silent'

print(is_anagram(word_1,word_2))
