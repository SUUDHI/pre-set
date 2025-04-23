#Reverse each word in a sentence (keeping word order intact)
from manual_split import manual_split

data = 'hello world'

splited_data = manual_split(data)

reversed_data = []

for item in splited_data:
    reversed_item = ''
    for char in item:
        reversed_item = char + reversed_item
    reversed_data.append(reversed_item)
    
print(reversed_data)
