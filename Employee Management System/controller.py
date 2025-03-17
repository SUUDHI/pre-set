from model import EmployeeModle
from view import EmployeeView

class EmployeeController:
    def __init__(self):
        self.data = EmployeeModle.load_data()

    def register_employee(self):
        emp_id = EmployeeModle.generate_emp_id()
        name = EmployeeView.get_input("Enter your Name:")

       #using while true with exception handling for age
        while True:  
            try:
                age = int(EmployeeView.get_input("Enter your Age:"))
                if age < 18:
                    raise ValueError("Age must be greater than or equal to 18.")
                break
            except ValueError as e:
                EmployeeView.show_message(f"Invalid input: {e}. Please enter a valid age.")

        department = EmployeeView.get_input("Enter your Department:")

        #using while true with exception handling for Salary
        while True:
            try:
                salary = float(EmployeeView.get_input("Enter your Salary:"))
                if salary <= 0:
                    raise ValueError("Salary must be a positive number.")
                break
            except ValueError as e:
                EmployeeView.show_message(f"Invalid input: {e}. Please enter a valid salary.")

        password = EmployeeView.get_input("Enter A Strong Password:")

        new_employee = EmployeeModle(emp_id, name, age, department, salary, password)
        self.data.append(new_employee.to_dict())
        EmployeeModle.save_data(self.data)
        EmployeeView.show_message(f"Employee added,your Id is {emp_id}")

    def authenticate_user(self, emp_id, password):
        for emp in self.data:
            if emp ["emp_id"] == emp_id and emp ["password"] == password:
                return emp
        return None
    
    #admin only
    def view_all_employee(self):
        for emp in self.data:
            EmployeeView.show_employee_details(emp)

    def delete_employee(self,emp_id):
        if emp_id == 1000:
            EmployeeView.show_message("Admin can't be delete from database")
            return
        new_data=[emp for emp in self.data if emp["emp_id"] != emp_id]

        if len(new_data) == len(self.data):
            EmployeeView.show_message("Employee Id is not in database")
        else:
            EmployeeModle.save_data(new_data)
            EmployeeView.show_message("Employe deleted from database")
    
    def update_employee_details(self, employee):
        for emp in self.data:
            if emp["emp_id"] == employee["emp_id"]:
                emp["name"] = EmployeeView.get_input("Enter your name:") or emp['name']
                emp["age"] = EmployeeView.get_input("Enter your agr:") or emp["age"]
                emp["department"] = EmployeeView.get_input("Enter your department") or emp["department"]
                emp["salary"] = EmployeeView.get_input("Enter your salary:") or emp["salary"]
                EmployeeModle.save_data(self.data)
                EmployeeView.show_message("Details Updated!")
                return
