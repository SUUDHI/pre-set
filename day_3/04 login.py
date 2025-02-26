Indentation = "SK123@gmail.com"
Passwd = "SK@123"

Itraction=0
Attempt=2

while(Itraction<3):
    Indentation_1=input("Enter username: ")
    Passwd_2=input("Enter password:")
    if Indentation == Indentation_1 and Passwd == Passwd_2:
        print("Login Successful!")
        break
    else:
        if Attempt >=0:
            print(f"Incorrect credentials. {Attempt} attempts left.")
    Attempt=Attempt-1
    Itraction=Itraction+1
