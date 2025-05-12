def PlusOne(digits):
    plus = []
    for i in digits:
        i = str(i)
        plus.append(i)

    k = ''.join(plus)

    k = int(k)
    k += 1

    result = list(str(k))

    last = []
    for i in result:
        g= int(i)
        last.append(g)
    
    return last

def PlusOne2(digits):
    plusone = int("".join([str(d) for d in digits])) + 1
    return [int (d) for d in str(plusone)]

digits = [9,9,0]
print(PlusOne(digits))    
print(PlusOne2(digits))
