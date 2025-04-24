# Merge Sorted Array without including zero
lst_1 = [1,2,3,0,0,0]
lst_2 = [2,5,6]

lst_1_without_0 = []

for num in lst_1:
    if num != 0:
        lst_1_without_0.append(num)

merge_list = lst_1_without_0 + lst_2

for num_1 in range(len(merge_list)):
    for num_2 in range(num_1 + 1,len(merge_list)):
        if merge_list[num_1] > merge_list[num_2]:
            merge_list[num_1] , merge_list[num_2] = merge_list[num_2] , merge_list[num_1]

print(merge_list)
