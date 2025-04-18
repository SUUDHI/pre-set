lst = [4,1,2,3,4,5,1]

def duplicate(lst):
    unique = set()
    for i in range(len(lst)):
        for j in range(len(lst)):
            if i != j and lst[i] == lst[j]:
                unique.add(lst[j])
    print(unique)

duplicate(lst)
