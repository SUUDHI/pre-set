from view import EmployeeDisplay
from constant import ADMIN_ID
from Util import InputHandler, Update_details
from modle_01 import EmployeeRecord

class EmployeeManager:
    def register_employee(self):
        name = InputHandler.input_name()
        age = InputHandler.input_age()
        department = EmployeeDisplay.get_input("Enter your Department:")
        salary = InputHandler.input_salary()
        password = InputHandler.input_password()

        connect = EmployeeRecord.connect_db()
        cursor = connect.cursor()

        new_emp_id = EmployeeRecord.save_employee(name, age, department, salary, password)
        EmployeeDisplay.show_message(f"Employee added, your ID is {new_emp_id}")
   
    def update_employee_details(self, emp_id):
            connect = EmployeeRecord.connect_db()
            cursor = connect.cursor()

            new_name = Update_details.update_name()
            new_age = Update_details.update_age()
            new_department = Update_details.update_department()
            new_salary = Update_details.update_salary()
            new_password = Update_details.update_password()

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

class AdminManager:  
    def delete_employee(self,emp_id):
        if emp_id == ADMIN_ID:
            EmployeeDisplay.show_message("Admin can't be delete from database")
        else:
            connect = EmployeeRecord.connect_db()
            cursor = connect.cursor()
            cursor.execute("DELETE FROM Employee WHERE emp_id = ?",(emp_id,))  
            connect.commit()
            EmployeeDisplay.show_message("Employee deleted!")

    def view_all_employee(self):
        employees = EmployeeRecord.load_all_employee()
        for emp in employees:
            EmployeeDisplay.show_message(f"ID: {emp[0]}, Name: {emp[1]}, Age: {emp[2]}, Dept: {emp[3]}, Salary: {emp[4]}")
      