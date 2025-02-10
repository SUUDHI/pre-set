id = "SK"
passwd = "SK@123"

i=0
k=2

while(i<3):
    id1=input("Enter username: ")
    passwd2=input("Enter password:")
    if id == id1 and passwd == passwd2:
        print("Login Successful!")
        break
    else:
        if k >=0:
            print(f"Incorrect credentials. {k} attempts left.")
    k=k-1
    i=i+1
