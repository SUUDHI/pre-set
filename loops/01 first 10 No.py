# for i in range (1,11):
#     print(i)

for i in range(1, 11):
    if i % 3 == 0 and i % 2 == 0:
        continue
    if i % 4 == 0:
        pass
    if i % 5 == 0:
        break
    print(i)

#1,2,3,4