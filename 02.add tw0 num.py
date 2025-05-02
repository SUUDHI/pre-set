"""
Input: l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
"""

list_1 = [2,4,3]
list_2 =  [5,6,4]

def Add_lst(lst_1, lst_2):
    output = []

    for i in range(len(list_1)):
        for j in range(len(list_2)):
            k = list_1[i] + list_2[j]
            if k < 9:
                output.append(k)
            else:
                output.append(0)
            break

    return output

print(Add_lst(list_1, list_2))
