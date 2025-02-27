Valid_age = 121
Negative_age = 0
Voting_age = 18

Name = input("Enter your name: ")
Age = int(input("Enter your ange: "))

if Age >=Valid_age:
    print("enter valid age")
elif Age <=Negative_age:
    print("age is negative")
elif Age >= Voting_age:
    print(f"congo,{Name} you can vote your age is {Age}")
else:
    print(f"Sorry {Name}, you are not eligible to vote")
    