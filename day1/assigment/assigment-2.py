"""
methord i want to use but user press enter after entring first number
num1,num2=input("enter two number with space:").split()
print(num1)
print(num2)
"""
num1=input("enter first number:")
num2=input("enter second number:")
#converting type
converted_num1=int(num1)
converted_num2=int(num2)

print(f"Sum of {converted_num1} and {converted_num2} is {converted_num1+converted_num2}")
print(f"Difference of {converted_num1} and {converted_num2} is {converted_num1-converted_num2}")
print(f"Product of {converted_num1} and {converted_num2} is {converted_num1*converted_num2}")
print(f"Division of {converted_num1} and {converted_num2} is {converted_num1//converted_num2}")

#converting in to float
float_num1=float(num1)
float_num2=float(num2)
print(f"Sum of {float_num1} and {float_num2} is {float_num1+float_num2}")
print(f"Difference of {float_num1} and {float_num2} is {float_num1-float_num2}")
print(f"Product of {float_num1} and {float_num2} is {float_num1*float_num2}")
print(f"Division of {float_num1} and {float_num2} is {float_num1/float_num2}")
