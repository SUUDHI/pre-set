element = [10,22,33,1,32,45,77]

def largest(l1):
    max_num = 0
    for i in l1:
        if i > max_num:
            max_num = i
    return max_num

print(largest(element))