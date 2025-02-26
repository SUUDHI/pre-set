import csv

f = open(r'C:\cprogramming\Git_demo\pre-set\NKE.csv', 'r')

ro=csv.reader(f,delimiter=',')
ld=list(ro)
print(ld)
print(ro)
for row in ld:
    print(row)
f.close()