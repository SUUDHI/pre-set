#Write a program to remove duplicates from a list

list1 = [1,1,2,3,3,4,5,5,6,7]
print(list1)

set1 = set(list1)

list2 = list(set1)
print(list2)

new = []
for item in list1:
    if item not in new:
        new.append(item)
    
print(new)
    