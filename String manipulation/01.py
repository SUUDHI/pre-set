#input = 'my name is sudhanshu meena and output needs to be MY NamE IS SudhanshU MeenA

string = "my name is sudhanshu"

split_string = string.split()

converted_string = []
for i in split_string:
    convert = i[0].upper() + i[1:-1] + i[-1].upper()
    converted_string.append(convert)
    
print(converted_string)
