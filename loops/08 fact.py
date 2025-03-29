#Find the factorial of a number using a loop
def fact(x):
    fact = 1

    if x <= 1:
        return 1
    else:
        for i in range(1,x+1):
            fact = fact*i
        print(fact)

fact(5)
