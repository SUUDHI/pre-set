#A year is a leap year if it is divisible by 4, but not by 100 unless it is also divisible by 400. 

year =  int(input("Enter a year:"))

def isleap(x):
    if x % 4 == 0 or x % 400 == 0 and x % 100 == 0:
        print("is a leeap year")
    else:
        print("not a leap year")

isleap(year)  