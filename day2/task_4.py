"""
Task 4: Age Validator
Write a program that:
Takes user name and age as input.
Checks if the user is eligible to vote (18+ years old).
If age is negative or unrealistic (e.g., > 120), show an error.
Example Output:
Enter your name: John  
Enter your age: 17  
Sorry John, you are not eligible to vote."""
name = input("Enter your name: ")
age = int(input("Enter your ange: "))

if age >=121:
    print("enter valid age")
elif age <=0:
    print("age is negative")

elif age >= 18:
    print(f"congo,{name} you can vote your age is {age}")

else:
    print(f"Sorry {name}, you are not eligible to vote")