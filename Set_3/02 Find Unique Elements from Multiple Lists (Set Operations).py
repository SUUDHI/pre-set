list1 = [1, 2, 3, 4]
list2 = [3, 4, 5, 6]
list3 = [5, 6, 7, 8]

all_num=list1 + list2 + list3

count_dict = {}
for num in all_num:
        count_dict[num] = count_dict.get(num, 0) + 1  

unique_set = {num for num, count in count_dict.items() if count == 1}

print(unique_set)
