#Given a list of numbers from 1 to n with one number missing, write a function to find the missing number

lst = [1,2,3,4,5,7,8,9]

# normal approch 
a1 = []
for j in range(1,10):
     if j not in lst:
         a1.append(j)
print("Missing number is :",a1)

# when list is sorted 
r = lst[-1] #when list is sorted
a2 = list(range(1, r + 1))

for i in a2:
    if i not in lst:
        print("Missing number is:", i)

# when list is not sorted and only one number is missing
lst2 = [1,3,2,5,7,6]
a3 = []

for i in range(1,(len(lst2) + 2)):
    a3.append(i)

for i in a3:
    if i not in lst2:
        print("Missing number is:",i)
