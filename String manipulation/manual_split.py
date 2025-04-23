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