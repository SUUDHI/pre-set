#Python counter and dictionary intersection example (Make a string using deletion and rearrangement)

s1 = 'ABHISHEKsinGH'
s2 = 'gfhfBHkooIHnfndSHEKsiAnG'
#Output : Possible

s1 = s1.upper()
s2 = s2.upper()

dict_1 = {}
dict_2 = {}

for char in s1:
    if char in dict_1:
        dict_1[char] += 1
    else:
        dict_1[char] = 1

#print(dict_1)

for char in s2:
    if char in dict_2:
        dict_2[char] += 1
    else:
        dict_2[char] = 1

#print(dict_2)

is_possible = True
for char in dict_1:
    if char not in dict_2 or dict_2[char] < dict_1[char]:
        is_possible = False
        break

if is_possible:
    print("posible")
else:
    print("not possible")