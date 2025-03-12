import json
import os

Path=(r"C:\cprogramming\Employee Management System\01\employees.json")

class EmployeeModle:
    @staticmethod
    def load_data():
        if not os.path.exists(Path):
            with open(Path, "w") as file:
                json.dump([], file)
        with open(Path, "r") as file:
            return json.load(file)
    
    @staticmethod
    def save_data(data):
        with open(Path,"w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def generate_emp_id():
        data=EmployeeModle.load_data()
        return 1001 if not data else max(emp ["emp_id"] for emp in data)+1
    
    def __init__(self,emp_id, name, age, department, salary, password):
        self.emp_id = emp_id
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        self.password = password
    
    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,    
            "age": self.age,
            "department": self.department,
            "salary": self.salary,
            "password": self.password
        }
    
class EmployeeView:
    @staticmethod
    def show_message(message):
        print(message)
    
    @staticmethod
    def get_input(prompt):
        return input(prompt)
    
    @staticmethod
    def show_employee_details(employee):
        print("Employee details")
        print(f"ID:{employee['emp_id']}")
        print(f"Name:{employee['name']}")
        print(f"Age:{employee['age']}")
        print(f"Department:{employee['department']}")
        print(f"Salary:{employee['salary']}")

class EmployeeController:
    def __init__(self):
        self.data = EmployeeModle.load_data()

    def register_employee(self):
        emp_id = EmployeeModle.generate_emp_id()
        name = EmployeeView.get_input("Enter your Name:")
        age = EmployeeView.get_input("Enter your Age:")
        department = EmployeeView.get_input("Enter your Department:")
        salary = EmployeeView.get_input("Enter your Salary:")
        password = EmployeeView.get_input("Enter A Strong Password:")

        new_employee = EmployeeModle(emp_id, name, age, department, salary, password)
        self.data.append(new_employee.to_dict())
        EmployeeModle.save_data(self.data)
        EmployeeView.show_message(f"Employee added,your Id is{emp_id}")

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
#main fun
def main():
    controller = EmployeeController()

    while True:
        EmployeeView.show_message("     WELCOME     ")
        EmployeeView.show_message("1.login")
        EmployeeView.show_message("2.Register")
        EmployeeView.show_message("3.Exit")

        choice = EmployeeView.get_input("Enter your choice:")

        if choice == "1":
            emp_id = int(EmployeeView.get_input("Enter Employee Id:"))
            password=EmployeeView.get_input("Enter your password:")
            employee = controller.authenticate_user(emp_id, password)

            if employee:
                EmployeeView.show_message("Login Successfully!")
                if emp_id == 1000:
                    while True:
                        EmployeeView.show_message("Welcome Admin")
                        EmployeeView.show_message("1.View all employee.")
                        EmployeeView.show_message("2.Remove a employee.")
                        EmployeeView.show_message("3.Logout.")

                        Admin_choice =EmployeeView.get_input("Enter Choice:")

                        if Admin_choice == "1":
                            controller.view_all_employee()
                        elif Admin_choice == "2":
                            emp_id = int(EmployeeView.get_input("Enter Employee ID to delete: "))
                            controller.delete_employee(emp_id)
                        elif Admin_choice == "3":
                            break
                
                else:
                    EmployeeView.show_message("Welcome Employee!")
                    EmployeeView.show_message("1.View Details.")
                    EmployeeView.show_message("2.Update Details.")
                    EmployeeView.show_message("3.Logout.")
                    Emp_choice = EmployeeView.get_input("Enter your Choice")

                    if Emp_choice == "1":
                        EmployeeView.show_employee_details(employee)

                    elif Emp_choice == "2":
                        controller.update_employee_details(employee)

                    elif Emp_choice == "3":
                        break

            else:
                EmployeeView.show_message("Invilid ID")
        elif choice == "2":
            controller.register_employee()
        
        elif choice == "3":
            EmployeeView.show_message("Exiting the system.")
            break
        else:
            EmployeeView.show_message("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
   
    
        

        