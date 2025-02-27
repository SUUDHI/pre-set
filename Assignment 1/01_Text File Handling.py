No_of_Employee = int(input("Enter Number of Employee you want to store data of: "))

with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\employees.txt ", "a") as file:
    for i in range(No_of_Employee):
        file.write(input("Enter Employee ID: ") + ", ")
        file.write(input("Enter Employee Name: ") + ", ")
        file.write(input("Enter Employee Age: ") + ", ")
        file.write(input("Enter Employee Department: ") + "\n")

with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\employees.txt ", "r") as file:
    print(file.read())

with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\employees.txt ", "r") as file:
    search_id = input("Enter Employee ID to search: ")
    for line in file:
        if search_id in line:
            print(line)
            break
    else:
        print("Employee ID not found")
    