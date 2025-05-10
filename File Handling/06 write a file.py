#Write a program that takes user input and saves it to a file named output.txt.

def write(x):
    with open("01_file.txt","w") as file:
        file.write(x)

s = input("")

write(s)

def count1(xx):
    count = 0
    with open ("01_file.txt") as file:
        reader = file.read()
        reader.split()
        print(len(reader))
count1(s)
        