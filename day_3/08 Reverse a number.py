num = int(input("Enter a number: "))

reversed_num = 0

while num > 0:
      dig = num % 10
      reversed_num = reversed_num * 10 + dig
      num = num // 10

print("Reversed number:", reversed_num)