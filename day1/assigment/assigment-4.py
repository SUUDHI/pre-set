"""Temperature Converter
Take a temperature value as input.
Convert it from Celsius to Fahrenheit and Fahrenheit to Celsius.
Use the formulas:
°F = (°C × 9/5) + 32
°C = (°F − 32) × 5/9
Example Output:
Enter temperature in Celsius: 25
25°C is 77°F
Enter temperature in Fahrenheit: 98
98°F is 36.67°C

"""
temp1 = int(input("Enter temperature in Celsius:"))
c = temp1
k = (c *  9//5 ) + 32
print(c,"°is",k,"°")
temp2 = int(input("Enter temperature in Fahrenheit:"))
F = temp2
C = (F - 32 ) * 5//9
print(F,"°is",C,"°")
