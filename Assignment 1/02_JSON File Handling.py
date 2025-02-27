import json

No_of_Employee = int(input("Enter Number of Employee you want to store data of: "))

#below code is performing write operation on the Emp-1.txt file
with open (r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.txt", "a") as file:
    for i in range(No_of_Employee):
        file.write(input("Enter Employee ID: ") +", ")
        file.write(input("Enter Employee Name: ") +", ")
        file.write(input("Enter Employee Age: ") +", ")
        file.write(input("Enter Employee Department: ")+"\n")

#below code is performing read operation on the Emp-1.txt file        
with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.txt", "r") as file:
    print(file.read())

#below code is performing search operation on the basis of Employee ID
with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.txt", "r") as file:
    search_id = input("Enter Employee ID to search: ")
    for line in file:
        if search_id in line:
            print(line)
            break
    else:
        print("Employee ID not found")



        