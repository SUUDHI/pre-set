# #word location in the string
#get this from stackoverflow.com
def manual_split(text):
    result = []
    word = ""

    for char in text:
        if char != " ":        # Not a space? Keep building the word
            word += char
        else:
            if word:           # Word is not empty
                result.append(word)
                word = ""      # Reset for the next word

    # Add the last word if there's any left after loop
    if word:
        result.append(word)

    return result

data = "python is best for Ai and Ml"

find = "Ai"

splited_data = manual_split(data)

for index in range(len(splited_data)):
     if splited_data[index] == find:
         print(f"Index is {index} and Word is {splited_data[index]}")
    