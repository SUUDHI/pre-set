num = int(input("Enter a number: "))

if num < 2:
    print("enter number is 1 or less then 1")
else:
    Iteration=1
    flag=0
    while Iteration<=num:
        if num % Iteration ==0:
            flag=flag+1
        Iteration=Iteration+1
    if flag ==2:
        print(f"{num} is a prime number.")
    else:
        print(f"{num} is nat a prime number.")
           