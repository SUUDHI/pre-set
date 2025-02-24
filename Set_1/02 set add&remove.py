"""Create a set containing five unique numbers. Perform the following operations:
Add a new number to the set.
Try adding a duplicate number and observe what happens.
Remove a specific number from the set.
Check whether a given number is present in the set or not."""
set1={1,2,3,4,5}
set1.add(6)
print(set1)
set1.add(6)#nothing is happen set ignore the duplicate without giving error

set1.remove(3)
print(set1)
