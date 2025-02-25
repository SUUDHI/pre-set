f=open('sudhanshu.txt','r')
content = f.read()
#print(content)
f.close()

#Reading a File in Binary Mode
g=open('sudhanshu.txt','rb')
content1 = g.read()
print(content1)
g.close()