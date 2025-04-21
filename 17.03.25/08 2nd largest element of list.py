# Write a program to print second largest element from an array.

data = [10,22,33,22,15,66] 

unique_data = list(set(data))

def second_largest(list):
    for i in range(len(list)):
        for j in range(0, len(list)-i-1):
            if list[j] > list[j+1]:
                list[j], list[j+1] = list[j+1], list[j]

    return(list[-2])

print(second_largest(unique_data))
