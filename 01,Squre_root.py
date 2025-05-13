"""
Given a non-negative integer x, return the square root of x rounded down to the nearest integer. 
The returned integer should be non-negative as well.

You must not use any built-in exponent function or operator.

For example, do not use pow(x, 0.5) in c++ or x ** 0.5 in python.
 

Example 1:

Input: x = 4
Output: 2
Explanation: The square root of 4 is 2, so we return 2.
Example 2:

Input: x = 8
Output: 2
Explanation: The square root of 8 is 2.82842..., and since we round it down to the nearest integer, 2 is returned."""

def SqureRoot(num):
    for number in range(num):
        if number * number == num:
            return number
        elif number * number > num:
            return number-1
        
print(SqureRoot(8)) 

def SqureRoot_2(num):
    left = 0
    right = num
    result = 0

    while left <= right:
        mid = left + ((right - left) // 2)
        if mid **2 > num:
            right = mid-1
        elif mid ** 2 < num:
            left = mid + 1
            result = mid
        else:
            return mid
    
    return result

print(SqureRoot_2(8))
print(SqureRoot_2(4))