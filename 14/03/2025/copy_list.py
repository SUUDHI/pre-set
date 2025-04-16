#the list and copy list have difrent id if we change in one list it dont reflect on copy list, it known as cloneing.
list = [1, 2, 3, 4, 5]
print(id(list))

copy_list = list [:]
print(copy_list)
print(id(copy_list))

#using .copy()
copy2_list = list.copy()
print(copy2_list)
print(id(copy2_list))

#aliasing a list, refrese to make a complete same copy of list with same id.

x = ['a','b','c']
y = x #this is aliasing of list

print(id(x))
print(id(y))