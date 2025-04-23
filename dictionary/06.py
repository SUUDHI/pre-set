#Group Words by First Letter

# Input: ['apple', 'ant', 'banana', 'bat']
# Output: {'a': ['apple', 'ant'], 'b': ['banana', 'bat']}

data = ['apple', 'ant', 'banana', 'bat']

data_dict = {}

length = len(data)

for i in range(length):
    for j in range(i+1,length):
        if data[i][0] == data[j][0]:
            data_dict[data[i][0]] = [data[i],data[j]]

print(data_dict)
