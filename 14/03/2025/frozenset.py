#The frozenset() function returns an unchangeable frozenset object (which is like a set object, only unchangeable).

s = {1,2,3,4}
print(type(s))

frozenset1 = frozenset(s)
print(frozenset1)
print(type(frozenset1))