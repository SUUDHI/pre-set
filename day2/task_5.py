num1 = input("enter a number: ")
#checking primr in below code
num = int(num1)
flag=0
Iteration=1
while Iteration<=num:
    if num % Iteration ==0:
        flag=flag+1
    Iteration=Iteration+1
if flag==2:
    print(f"{num} is an primr number.")
else:
    print(f"{num} is not an prime number.")

#below code is for sum of digits
sum=0
while num >0:
    dig = num % 10
    sum += dig
    num = num // 10
print(f"Sum of digits: {sum}")

#below code is for palindrome
num_copy=int(num1)
num_copy01=int(num1)
Reverse=0

while num_copy > 0:
    last = num_copy % 10
    Reverse=Reverse * 10 + last
    num_copy= num_copy //10

if num_copy01 == Reverse:
    print(f"{num1} is an palindrome.")
else:
    print(f"{num1} is not a palindrome.")
  