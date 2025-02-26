def character_frequency(s):
    frequency = {}
    for char in s:
        if char != ' ':
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
    return frequency

input_string = "Sudhanshu Manutwal"
print(character_frequency(input_string))