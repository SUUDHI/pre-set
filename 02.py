"""
Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.

The overall run time complexity should be O(log (m+n)).

Example 1:

Input: nums1 = [1,3], nums2 = [2]
Output: 2.00000
Explanation: merged array = [1,2,3] and median is 2.
Example 2:

Input: nums1 = [1,2], nums2 = [3,4]
Output: 2.50000
Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5."""

def Median(nums1,nums2):
    nums1 = nums1 + nums2

    for num1 in range(len(nums1)):
        for num2 in range(num1, len(nums1)):
            if nums1[num1] > nums1[num2]:
                nums1[num1] , nums1[num2] = nums1[num2] , nums1[num1]
    return nums1[len(nums1)//2]
    return nums1

print(Median([1,2],[4,3]))
                