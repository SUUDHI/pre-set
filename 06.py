#check for most frequent characater:

Input = "Soareyouperforming"

def freq_calc(word):
    freq = {}

    for i in word:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    #print(freq)

    max_keys = None
    max_value = 0

    for key, val in freq.items():
        if val > max_value:
            max_value = val
            max_keys = key

    return max_keys

print(freq_calc(Input))
