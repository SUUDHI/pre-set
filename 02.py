#sort list 
#head = [4,2,1,3]
#Output: [1,2,3,4]

#head = [-1,5,3,4,0]
#Output: [-1,0,3,4,5]

def sorted_list(lst):
    for i in range(len(lst)):
        for j in range(len(lst)):
            if lst[i] != lst[j] and lst[i] < lst[j]:
                lst[i], lst[j] = lst[j], lst[i]
    
    return(lst)

head = [4,5,2,6]
print(sorted_list(head))

head1 = [-1,5,3,4,0]
result = sorted_list(head1)

print(result)
