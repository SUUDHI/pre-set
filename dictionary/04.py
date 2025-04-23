# sort a dictionary by value

#Approach 1: using loop 

data = {'x': 10, 'y': 44, 'z': 30, 'k':1}

myValues = list(data.values())
#print(myValues)

for item1 in range(len(myValues)):
    for item2 in range(item1+1,len(myValues)):
        if myValues[item1] > myValues[item2]:
            myValues[item1], myValues[item2] = myValues[item2], myValues[item1]

#print(myValues)

sorted_dict = {}

for value in myValues:
    for key in list(data.keys()):
        if data[key] == value:
            sorted_dict[key] = value
            del data[key]
            break

print(sorted_dict)

# Approach 2: using sorted and kambda
data = {'x': 10, 'y': 44, 'z': 30, 'k':1}

sorted_list = sorted(data.items(), key = lambda x:x[1])

print(dict(sorted_list))
