First_friend={12,17,18,}
Second_friend={12,18,16}
common_numbers=[]#for storing common numbers
unique_First=[]#for storing unique numbers of first friend
unique_Second=[]#for storing unique numbers of second friend

#loop for finding common numbers
for i in First_friend:
    if i in Second_friend:
        common_numbers.append(i)
print(common_numbers)

#loop for finding unique numbers of first friend
for i in First_friend:
    if i not in Second_friend:
        unique_First.append(i)
print(unique_First)

#loop for finding unique numbers of second friend
for i in Second_friend:
    if i not in First_friend:
        unique_Second.append(i)
print(unique_Second)
