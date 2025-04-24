number = int(input("Enter NUmber: "))

previous = 0
current = 1
next = current  
count = 1

while count <= number:
    print(next, end=" ")
    count += 1
    previous, current = current, next
    next = previous + current
print()
