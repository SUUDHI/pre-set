# Check Common Member Between Two Lists


data_1 = [1,2,5,3,4]

data_2 = [5,6,7,8,1]

common_num = []

for num_1 in data_1:
    for num_2 in data_2:
        if num_1 == num_2:
            common_num.append(num_1)

print(common_num)

