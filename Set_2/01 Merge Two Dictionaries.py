dict1 = {"Alice": 85, "Bob": 78}
dict2 = {"Bob": 90, "Charlie": 88}

# Creating an empty dictionary to store merged data
merged_dict = {}

# Copy elements from dict1
for key in dict1:
    merged_dict[key] = dict1[key]

# Merge elements from dict2 while keeping the highest score
for key in dict2:
    if key in merged_dict:
        if merged_dict[key] < dict2[key]:  #checking for higher score
            merged_dict[key] = dict2[key]#if higher thenstore it
    else:
        merged_dict[key] = dict2[key]

# Print the final merged dictionary
print(merged_dict)
