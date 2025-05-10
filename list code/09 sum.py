#Write a Python program to find the sum and average of elements in a list
l = [1,2,3,4]

length = len(l)
total = 0

for i in l:
    total += i
print("sum of listis:",total)

average = total // length
print("average of the element in list:"average)