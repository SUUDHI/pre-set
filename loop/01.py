#Sum of Even Numbers in a Range

number = int(input("Enter number: "))

sum =0

for item in range(1,number):
    if item % 2 == 0:
        sum += item

print(sum)
