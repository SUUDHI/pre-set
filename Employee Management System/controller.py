from model import EmployeeRecord
from view import EmployeeDisplay
from constant import Admin_Id
from Util import *

class EmployeeManager:
    def __init__(self):
        self.data = EmployeeRecord.load_data()

    def register_employee(self):
        name = EmployeeDisplay.get_input("Enter your Name:")
        age= age_Validation()
        department = EmployeeDisplay.get_input("Enter your Department:")
        salary = Input_salary()
        password = Input_Password()
        new_employee = EmployeeRecord(name,age,department,salary,password)
        self.data.append(new_employee.to_dict())
        EmployeeRecord.save_data(self.data)
        EmployeeDisplay.show_message(f"Employee added,your Id is {new_employee.emp_id} ")

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
                if salary.isdigit() and int(salary) > 0:
                    emp["salary"] = salary

                EmployeeRecord.save_data(self.data)
                EmployeeDisplay.show_message("Details Updated!")
                return
