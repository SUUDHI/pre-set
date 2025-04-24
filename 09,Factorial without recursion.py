# Factorial without recursion
number = int(input("Enter number: "))

fact = 1

for i in range(1, number + 1):
    fact *= i

print(fact)
