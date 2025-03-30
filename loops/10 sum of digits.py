#Find the sum of digits of a given number using a loop

def sumofdigit(number):
    sum = 0

    if number == 0:
        return 0
    elif 1 <= number <=9:
        return number
    else:
        while number > 0:
            num = number % 10
            number //= 10
            sum = sum + num

        return sum

print(sumofdigit(109))
