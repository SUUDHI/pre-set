#using .update methord
dict_1 = {"Alice": 85, "Bob": 78} 
dict_2 = {"Bob": 90, "Charlie": 88} 
dict_1.update(dict_2)
print(dict_1)

dict1 = {"Alice": 85, "Bob": 78}
dict2 = {"Bob": 90, "Charlie": 88}

# Creating an empty dictionary
merged_dict = {}

for key in dict1:
    merged_dict[key] = dict1[key]
print(merged_dict)

# Add all key-value pairs from dict2, updating scores if necessary
for key in dict2:
    if key in merged_dict:
        # Keep the highest score if the name exists in both dictionaries
        merged_dict[key] = max(merged_dict[key], dict2[key])
    else:
        merged_dict[key] = dict2[key]

# Print the final merged dictionary
print(merged_dict)


