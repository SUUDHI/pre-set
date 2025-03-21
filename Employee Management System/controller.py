from model import EmployeeRecord
from view import EmployeeDisplay
from constant import ADMIN_ID
from Util import *

class EmployeeManager:
    def __init__(self):
        self.data = EmployeeRecord.load_data()

    def register_employee(self):
        name = EmployeeDisplay.get_input("Enter your Name:")
        age = age_Validation()
        department = EmployeeDisplay.get_input("Enter your Department:")
        salary = Input_salary()
        password = Input_password()
        new_employee = EmployeeRecord(name,age,department,salary,password)
        self.data.append(new_employee.to_dict())
        EmployeeRecord.save_data(self.data)
        EmployeeDisplay.show_message(f"Employee added,your Id is {new_employee.emp_id} ")

    #admin only
    def view_all_employee(self):
        for emp in self.data:
            EmployeeDisplay.show_employee_details(emp)

    def delete_employee(self,emp_id):
        if emp_id == ADMIN_ID:
            EmployeeDisplay.show_message("Admin can't be delete from database")
        else:
            for emp in self.data: 
                if emp["emp_id"] == emp_id:
                    self.data.remove(emp) 
                    EmployeeRecord.save_data(self.data)
                    EmployeeDisplay.show_message("Employee deleted from database.") 
                    
            EmployeeDisplay.show_message("Employee ID not found in database.")
   
    def update_employee_details(self, employee):
        for emp in self.data:
            if emp["emp_id"] == employee["emp_id"]:
                name= Update_name()
                emp["name"] = name
                
                age = Update_age()
                emp["age"] = age

                department = Update_department()
                emp["department"] = department

                new_salary = Update_salary()
                if new_salary is not None:  
                    emp["salary"] = new_salary 

                EmployeeRecord.save_data(self.data)
                EmployeeDisplay.show_message("Details Updated!")
                return
