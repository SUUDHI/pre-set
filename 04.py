# s = [0,1,0,2,1,0,1,2,0]
# output = [0, 0, 0, 0, 1, 1, 1, 2, 2]

input = [0,1,0,2,1,0,1,2,0]

for num_1 in range(len(input)):
    for num_2 in range(num_1 + 1,len(input)):
        if input[num_1] > input[num_2]:
            input[num_1] , input[num_2] = input[num_2] , input[num_1]

print(f"output: {input}")
