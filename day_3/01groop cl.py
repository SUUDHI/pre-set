# Define constants for better readability
CHILD_AGE_MIN = 0
CHILD_AGE_MAX = 12
TEEN_AGE_MIN = 13
TEEN_AGE_MAX = 19
ADULT_AGE_MIN = 20
ADULT_AGE_MAX = 59
SENIOR_AGE_MIN = 60
SENIOR_AGE_MAX = 120

# User Input
age = int(input("Enter your age: "))

# Age Classification
if age < 0:
    print("Age can't be negative.")
elif CHILD_AGE_MIN <= age <= CHILD_AGE_MAX:
    print("You are a child.")
elif TEEN_AGE_MIN <= age <= TEEN_AGE_MAX:
    print("You are a teenager.")
elif ADULT_AGE_MIN <= age <= ADULT_AGE_MAX:
    print("You are an adult.")
elif SENIOR_AGE_MIN <= age <= SENIOR_AGE_MAX:
    print("You are a senior citizen.")
else:
    print("Invalid age range.")  # Handles cases like age > 120
