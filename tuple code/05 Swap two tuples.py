tuple1 = (11, 22)
tuple2 = (99, 88)

#my aproch
temp=tuple1
tuple1=tuple2
tuple2=temp
print(tuple1)
print(tuple2)

t1 = (110, 220)
t2 = (990, 880)

t1,t2 = t2,t1
print(t1)
print(t2)
