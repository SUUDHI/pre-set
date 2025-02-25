list1 = ["Mike", "", "Emma", "Kelly", "", "Brad"]

#list1.remove("")
del list1[1]
del list1[3]
print(list1)

list2 = ["Mike", "", "Emma", "Kelly", "", "Brad","","sham"]

# remove None from list1 and convert result into list
res = list(filter(None,list2))
print(res)
