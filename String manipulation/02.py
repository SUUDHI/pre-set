#Reverse each word in a sentence (keeping word order intact)

string = 'hello world'

splited_string = string.split()

a = []

for item in splited_string:
    item = item[::-1]
    a.append(item) 
    
print(a)
