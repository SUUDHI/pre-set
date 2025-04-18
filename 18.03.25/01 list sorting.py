# sort a list without using inbuild function.

lst = [2,7,6,4]
print(lst)
for i in range(len(lst)):
    for j in range(i+1,len(lst)):
        if lst[i] > lst[j]:
            lst[i],lst[j]=lst[j],lst[i]
print(lst)
    