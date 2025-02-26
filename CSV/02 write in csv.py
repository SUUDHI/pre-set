import csv
f = open(r'C:\cprogramming\Git_demo\pre-set\b.csv', 'w')

w=csv.writer(f,delimiter=',')

data=[[1,2,3,4,5],
     [6,7,8,9,10],
     [11,12,13,14,15]]
w.writerows(data)
f.close()