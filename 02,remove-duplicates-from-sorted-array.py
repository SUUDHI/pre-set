arry = [1,1,2,3,3,4,5,6,6,7]

def remove_duplicate(nums):
    non_duplicate = []
    count = 0

    for item in arry:
        if item not in non_duplicate:
            non_duplicate.append(item)
            count += 1

    return count,non_duplicate
print(remove_duplicate(arry))

def rem_dev(nums):
    count = 1
    
    for item in range(1,len(nums)):
        if nums[item] != nums[item - 1]:
            nums[count] = nums[item]
            count += 1
    return count

print(rem_dev(arry))

