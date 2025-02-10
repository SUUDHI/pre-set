"""
Triangle Type Checker 
   - Take three side lengths as input.  
   - Check and print whether they form:
     Equilateral Triangle (all sides equal),
     Isosceles Triangle (two sides equal),
     Scalene Triangle (all sides different),
     Invalid Triangle (sum of any two sides should be greater than the third side).
"""
side_1 = int(input("enter the first side: "))
side_2 = int(input("enter the second side: "))
side_3 = int(input("enter yhe third side: "))

if side_1 + side_2 <= side_3 and side_1 + side_3 <= side_2 and side_2 + side_3 <= side_1:
    print("Invalid Triangle")
    
elif side_1 == side_2 and side_2 == side_3:
    print("Equilateral Triangle")

elif side_1 == side_2 or side_2 == side_3 or side_1 == side_3:
    print("Isosceles Triangle")

elif side_1 != side_2 and side_2 != side_3:
    print("Scalene Triangle")