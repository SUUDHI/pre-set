#Count Down from a Given Number
number = int(input("enter number for count down: "))

for i in range(number,0,-1):
    print(i)
    if i == 1:
        print("LIFTOFF.....")
