# A peak element is greater than its neighbors. Find one peak.

nums=[1,2,3,1]
#output = 3

for element in range(1, len(nums) -1):
    if nums[element - 1] < nums[element] and nums[element] > nums[element + 1]:
        print(nums[element])
        