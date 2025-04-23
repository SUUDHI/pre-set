#Reverse a list without using .reverse()

data = [1,2,3,4,5]
a = []

data2 = data[::-1]
print(data2)

for i in range(len(data)-1,-1,-1):
    print(data[i],end = " ")
