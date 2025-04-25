# Reverse Every Alternate Word in a Sentence
from manual_split import manual_split

data = "object cannot be interpreted as an integer"

splited_data =  manual_split(data)

length = len(splited_data)

iteration = 0

while iteration <= length:
    if iteration % 2 == 0:
        word = ""
        for char in splited_data[iteration]:
            word = char + word
            splited_data[iteration] = word

    iteration += 1

print(splited_data) 
