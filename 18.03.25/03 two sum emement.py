#TwoSum Elements
# Find the pair of two numbers whose sum is 7

lst = [1,2,3,4,5,6,7,8]
pair_lst = []
for i in lst:
    for j in lst:
        if j != i and j + i == 7:
            pair_lst.append((i,j))

print(pair_lst)  
        