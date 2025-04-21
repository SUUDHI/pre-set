#input = 'my name is sudhanshu meena and output needs to be MY NamE IS SudhanshU MeenA

string = "my name is sudhanshu"

split_string = string.split()

converted_string = []
for item in split_string:
    convert = item[0].upper() + item[1:-1] + item[-1].upper()
    converted_string.append(convert)
    
print(converted_string)
