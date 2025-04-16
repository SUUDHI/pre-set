d = {'a': 1, 'b': 2}
for k in list(d.keys()):
    d[k + '1'] = d.pop(k)
print(d)

"""
OUTPUT: {'a1': 1, 'b1': 2} we get this output because we are adding '1' in keys. pop removes 'a' from the dict and returns 1 
"""