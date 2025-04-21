numbers = [10,22,33,1,32,45,77]

def largest(numbers_list):
    max_num = float('-inf')
    
    for number in numbers_list:
        if number > max_num:
            max_num = number
    return max_num

print(largest(numbers))
