#from model import EmployeeRecord
from view import EmployeeDisplay
from constant import ADMIN_ID
from Util import *
from modle_01 import Employe_r

class EmployeeManager:
    def register_employee(self):
        name = name_input()
        age = age_Validation()
        department = EmployeeDisplay.get_input("Enter your Department:")
        salary = Input_salary()
        password = Input_password()

        connect = Employe_r.Connect_db()
        cursor = connect.cursor()

        new_emp_id = Employe_r.save_employee(name, age, department, salary, password)
        EmployeeDisplay.show_message(f"Employee added, your ID is {new_emp_id}")

    #admin only
    def view_all_employee(self):
        employees = Employe_r.Load_all_employee()
        for emp in employees:
            EmployeeDisplay.show_message(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Dept: {emp[3]}, Salary: {emp[4]}")
        
    def delete_employee(self,emp_id):
        if emp_id == ADMIN_ID:
            EmployeeDisplay.show_message("Admin can't be delete from database")
        else:
            connect = Employe_r.Connect_db()
            cursor = connect.cursor()
            cursor.execute("DELETE FROM Employee WHERE emp_id = ?",(emp_id,))  
            connect.commit()
            EmployeeDisplay.show_message("Employee deleted!")

   
    def update_employee_details(self, emp_id):
            connect = Employe_r.Connect_db()
            cursor = connect.cursor()

            new_name = Update_name()
            new_age = Update_age()
            new_department = Update_department()
            new_salary = Update_salary()
            new_password = Update_password()

            cursor.execute("""
                UPDATE Employee 
                SET 
                    name = COALESCE(?, name),
                    age = COALESCE(?, age),
                    department = COALESCE(?, department),
                    salary = COALESCE(?, salary),
                    password = COALESCE(?, password)
                WHERE emp_id = ?
            """, (new_name, new_age, new_department, new_salary, new_password, emp_id))
            connect.commit()
            connect.close()
            EmployeeDisplay.show_message("Details Updated!")
            return
