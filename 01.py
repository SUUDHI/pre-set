#Input = ["eat","tea","tan","ate","nat","bat"]

#Output: [["bat"],["nat","tan"],["ate","eat","tea"]]

def sort_string(s):
    sorted_s = ''.join(sorted(s))

    return sorted_s

def group_anagrams(strs):
    anagrams = {}
    for word in strs:
        sorted_word = sort_string(word)
        if sorted_word in anagrams:
            anagrams[sorted_word].append(word)
        else:
            anagrams[sorted_word] = [word]
    return (list(anagrams.values()))

strs = ["eat", "tea", "tan", "ate", "nat", "bat"]

result = group_anagrams(strs)
print(result)
