"""
You are given a large integer represented as an integer array digits, 
where each digits[i] is the ith digit of the integer. 
The digits are ordered from most significant to least significant in left-to-right order. 
The large integer does not contain any leading 0's.

Increment the large integer by one and return the resulting array of digits.

 

Example 1:

Input: digits = [1,2,3]
Output: [1,2,4]
Explanation: The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].
Example 2:

Input: digits = [4,3,2,1]
Output: [4,3,2,2]
Explanation: The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].
Example 3:

Input: digits = [9]
Output: [1,0]
Explanation: The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0]."""


def add_one_to_digits(digits):
    digit_strings = []
    for digit in digits:
        digit = str(digit)
        digit_strings.append(digit)

    number_str = ''.join(digit_strings)

    incremented_number = int(number_str)
    incremented_number += 1

    result = list(str(incremented_number))

    output = []
    for digit in result:
        number_int= int(digit)
        output.append(number_int)
    
    return output

def add_one_to_digits_2(digits):

    numbers = int("".join([str(digit) for digit in digits])) + 1
    return [int (digit) for digit in str(numbers)]

digits = [9,9,0]
print(add_one_to_digits(digits))    
print(add_one_to_digits_2(digits))
