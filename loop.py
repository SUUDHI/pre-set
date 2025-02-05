class table:
    def print_table(self,n):
        i=1
        while i<=10:
            print(f"{n} * {i} = {n*i}")
            i+=1

print("enter number:")
num=int(input())
print("")
t=table()
t.print_table(num)


        