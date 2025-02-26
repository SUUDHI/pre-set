def num(k):#print 3 variables directly
    a,b,c=k
    print(a)
    print(b)
    print(c)

def num2(z):#function that unpack a tuple with 3 element and return them
    a,b,c=z
    return a,b,c

l1=(22,33,44)
num(l1)

x,y,z=num2(l1)#stoer the return value in x,y,z
print(x,y,z)
