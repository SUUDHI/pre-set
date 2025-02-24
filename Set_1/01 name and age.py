""" 
Create a dictionary to store the names and ages of three people. Write a program to:
Print the age of a specific person from the dictionary.
Add a new person with their age to the dictionary.
Update the age of an existing person.
Remove one person from the dictionary.
"""
# d={ 'name_1':'sudhanshu , 21',
#     'name_2':'ram , 10',
#     'name_3':'sham , 21'
#     }
# print(d['name_2'])
# d ['name_4']='lala , 50'

# d['name_2']= 'ram , 22'

# del d['name_3']
# print(d)

# print()

dic={'ram'    :22,
     'sham'   :20,
     'sharma' :30}

print(dic.get('ram'))

dic['govind'] = 40
dic['ram'] = 25
del dic['sharma']
print(dic)