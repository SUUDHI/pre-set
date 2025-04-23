#input = 'my name is sudhanshu meena and output needs to be MY NamE IS SudhanshU MeenA

def manual_split(text):
    result = []
    word = ""

    for char in text:
        if char != " ":        
            word += char
        else:
            if word:           
                result.append(word)
                word = ""      

    if word:
        result.append(word)

    return result

data = "my name is sudhanshu"

splited_data = manual_split(data)

converted_data = []

for item in splited_data:
    convert = item[0].upper() + item[1:-1] + item[-1].upper()
    converted_data.append(convert)
    
print(converted_data)
