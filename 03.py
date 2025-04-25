# Given a string (a2b3c2) print output (aabbbcc)

data = 'a2b3c2'

new_data = ""

for i in range(len(data)):
    if '0' < data[i] < '9' :
        #print(data[i])
        word = data[i - 1] * int(data[i])
        new_data += word

print(new_data)