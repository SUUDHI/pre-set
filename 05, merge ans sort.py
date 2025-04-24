# input = s = [1,3,4,8]
# input = a = [2,5,6]
# Merge Sorted Array

lst_1 = [1,3,4,8]
lst_2 = [2,5,6]

merge_list = lst_1 + lst_2

for num_1 in range(len(merge_list)):
    for num_2 in range(num_1 + 1,len(merge_list)):
        if merge_list[num_1] > merge_list[num_2]:
            merge_list[num_1] , merge_list[num_2] = merge_list[num_2] , merge_list[num_1]

print(merge_list)
