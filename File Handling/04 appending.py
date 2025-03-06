#Writing to a File in Append Mode
f=open('sudhanshu.txt','a')#this will append the content of the file and write the new content
f.write('this will append on the sudhnashu. txt file at the end of the file it dont change the content of the file')
f.write('\n')
f.close()
f=open('sudhanshu.txt','r')
print(f.read())
f.close()