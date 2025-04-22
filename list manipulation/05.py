#Shift all zeroes to the end of the list
data = [1,2,0,4,6,0,8]

length = len(data)

for num in range(length):
    for j in range(num,length):
        if data[num] == 0:
         data[num], data[j] =  data[j], data[num]

print(data)

#using while loop

data2 = [1,0,4,0,5,6]

i = 0
while i < len(data2):
   j = 1
   while j < len(data2):
      if data2[i] == 0:
         data2[i], data2[j] =  data2[j], data2[i]
      
print(data2)
