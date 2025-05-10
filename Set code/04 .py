#Update the first set with items that don’t exist in the second set
set1 = {10, 20, 30, 40, 50}
set2 = {30, 40, 50, 60, 70}

set1.difference_update(set2)
print(set1)
