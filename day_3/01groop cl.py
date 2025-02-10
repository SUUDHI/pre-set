"""
Questions on Conditional Statements (if-else)  
1. Age Group Classifier  
   - Take a person's age as input.  
   - Print the corresponding category: Child (0-12 years), Teenager (13-19 years), 
   Adult (20-59 years), Senior Citizen (60+ years).  

   Example Output:  
   Enter your age: 25  
   You are an Adult."""
age = int(input("enter your age: "))

if age ==0 and age <=12:
    print("you are a chile")

elif age >=13 and age <=19:
    print("Teenager")

elif age >=20 and age <=59:
    print("adult")

elif age >=60 and age <=120:
    print("Senior Citizen")

elif age <0:
    print("age cant be negetive")



