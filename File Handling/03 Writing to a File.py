#Writing to a File
f=open('sudhanshu.txt','w')#this will change the content of the file and write the new content
f.write('123,456,789,12,12,12,12')
f.write('\n')   
f.close()

f=open('sudhanshu.txt','r')
print(f.read())
f.close()

