#Convert two lists into a dictionary
keys = ['Ten', 'Twenty', 'Thirty']
values = [10, 20, 30]

join_dict = dict()

for i in range(len(keys)):
    join_dict.update({keys[i]: values[i]})
print(join_dict)
