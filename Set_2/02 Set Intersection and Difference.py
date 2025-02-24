"""
You are given two sets of integers representing the favorite numbers of two friends.
Write a program to:
Find and print the common numbers they both like (Intersection).
Find and print numbers that are unique to the first friend (Difference).
Find and print numbers that are unique to the second friend (Difference).
"""
First_friend={12,17,18,20,22}
Second_friend={12,18,19,20,14}

print(First_friend.intersection(Second_friend))
print(First_friend.difference(Second_friend))
print(Second_friend.difference(First_friend))

