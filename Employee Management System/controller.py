from model import EmployeeRecord
from view import EmployeeDisplay
from constant import Admin_Id

class EmployeeManager:
    def __init__(self):
        self.data = EmployeeRecord.load_data()

    def register_employee(self):
        emp_id = EmployeeRecord.generate_emp_id()
        name = EmployeeDisplay.get_input("Enter your Name:")

       #using while true with exception handling for age
        while True:  
            try:
                age = int(EmployeeDisplay.get_input("Enter your Age:"))
                if age < 18:
                    EmployeeDisplay.show_message("Age must be at least 18. Please enter a valid age.")
                    continue
                break
            except ValueError:
                EmployeeDisplay.show_message("Invalid input. Please enter a numeric age.")

        department = EmployeeDisplay.get_input("Enter your Department:")

        #using while true with exception handling for Salary
        while True:
            try:
                salary = float(EmployeeDisplay.get_input("Enter your Salary:"))
                if salary <= 0:
                    EmployeeDisplay.show_message("Salary must be a positive number or Grater then 0. Please try again.")
                    continue
                break
            except ValueError:
                EmployeeDisplay.show_message("Invalid input. Please enter a numeric salary value.")
        
        while True:
            EmployeeDisplay.show_message("At least 8 characters long,\n Contains both uppercase and lowercase letters,\n Includes at least one number")
            password = EmployeeDisplay.get_input("Enter Password:")

            passwd_len = len(password) >= 8
            Lower_case_check = False
            Upper_case_check = False
            digit_check = False

            for char in password:
                if 'A'<= char <= 'Z':
                 Upper_case_check = True
                if 'a'<= char <= 'z':
                    Lower_case_check = True
                if '0' <= char <= '9':
                    digit_check = True

            if passwd_len and Lower_case_check and Upper_case_check and digit_check:
                break
            else:
                EmployeeDisplay.show_message("week enter stronge password")
        #convert user input to a dict, so 
        employee_data = {
                        "name": name,
                        "age": age,
                        "department": department,
                        "salary": salary,
                        "password": password
                        }

        new_employee = EmployeeRecord(**employee_data)
        self.data.append(new_employee.to_dict())
        EmployeeRecord.save_data(self.data)
        EmployeeDisplay.show_message(f"Employee added,your Id is {emp_id}")

    #admin only
    def view_all_employee(self):
        for emp in self.data:
            EmployeeDisplay.show_employee_details(emp)

    def delete_employee(self,emp_id):
        if emp_id == Admin_Id:
            EmployeeDisplay.show_message("Admin can't be delete from database")
            return
        new_data=[emp for emp in self.data if emp["emp_id"] != emp_id]

        if len(new_data) == len(self.data):
            EmployeeDisplay.show_message("Employee Id is not in database")
        else:
            EmployeeRecord.save_data(new_data)
            EmployeeDisplay.show_message("Employe deleted from database")
    
    def update_employee_details(self, employee):
        for emp in self.data:
            if emp["emp_id"] == employee["emp_id"]:
                name = EmployeeDisplay.get_input("Enter Name:").strip()
                if name:
                    emp["name"] = name

                age = EmployeeDisplay.get_input("Enter age:").strip()
                if age.isdigit() and int(age) >= 18:
                    emp["age"] = int(age)
                
                department = EmployeeDisplay.get_input("Enter Department:").strip()
                if department:
                    emp["department"] = department

                salary = EmployeeDisplay.get_input("Enter Salary:").strip()
                if salary.isdigit() and float(salary) > 0:
                    emp["salary"] = salary

                EmployeeRecord.save_data(self.data)
                EmployeeDisplay.show_message("Details Updated!")
                return
