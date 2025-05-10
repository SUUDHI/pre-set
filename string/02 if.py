suu = int(input("enter age:"))

def validate(x):
    if x >= 18:
        if x == 20:
            print("you are an adult")
    elif x < 18:
        print("you are a kid")
    
validate(suu)