#Using with Statement
#with statement is used for resource management. 
#It ensures that file is properly closed after its suite finishes, even if an exception is raised.
# with open() as method automatically handles closing the file once the block of code is exited, even if an error occurs.
# This reduces the risk of file corruption and resource leakage.

with open('sudhanshu.txt','r') as f:
    a=f.read()
    print(a)
print(f.closed) #True
#The file is closed automatically after the with statement block is executed.