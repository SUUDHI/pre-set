list1 = ["M", "na", "i", "Ke"] 
list2 = ["y", "me", "s", "lly", "aslamd"]
list3 = [i + j for i, j in zip(list1, list2)]
print(list3)

l3=[]
l3.append(list1[0]+list2[0])
l3.append(list1[1]+list2[1])
print(l3)

from itertools import zip_longest

result = [a + b if b else a for a, b in zip_longest(list1, list2, fillvalue="")]
print(result)
