"""
Write a Python program to print a specified list after removing the 0th, 4th  elements.
Sample List : ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']
Expected Output : ['Green', 'White', 'Black','Yellow']
"""
# approch 1, to get output only
Sample_List = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']

output = []

for element in Sample_List:
    if element == 'Red' or element == 'Pink':
        Sample_List.remove(element)

print(Sample_List)

#
Sample_List_2 = ['Red', 'Green', 'White', 'Black', 'Pink', 'Yellow']

result = []

# Loop through the list using index
for i in range(len(Sample_List_2)):
    if i != 0 and i != 4:  # Skip 0th and 4th elements
        result.append(Sample_List_2[i])

# Print the final list
print(result)

    