#Reverse each word in a sentence (keeping word order intact)

string = 'hello world'

splited_string = string.split()

a = []

for i in splited_string:
    i = i[::-1]
    a.append(i) 
    
print(a)
