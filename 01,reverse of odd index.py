# Write a program to print reverse of odd index string element i.e. 
# "hello good morning sir" to "hello doog morning ris".
from manual_split import manual_split

data = "hello good morning sir"

splited_data = manual_split(data)
print(splited_data)


for i in range(len(splited_data)):
    if i % 2 == 0:
        continue
    else:
        rev_word = ""

        for char in splited_data[i]:
            rev_word = char + rev_word
    splited_data[i] = rev_word

print(splited_data)
            