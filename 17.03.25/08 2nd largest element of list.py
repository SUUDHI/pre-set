# Write a program to print second largest element from an array.

def second_largest(arr):
    return sorted(set(arr))[-2]

list = [10,22,33,22,15,66] 
print(second_largest(list))