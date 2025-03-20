import json
import os
from  constant import Admin_details , Admin_Id

Path=(r"C:\cprogramming\GIt_demo\pre-set\Employee Management System\employees.json")

class EmployeeRecord:
    @staticmethod
    def load_data():
        data = [Admin_details] # Initialize with admin

        # If file does not exist, create it with admin details
        if not os.path.exists(Path):
            with open(Path, "w") as file:
                json.dump([Admin_details], file, indent=4)
        else:
            # Load existing data
            with open(Path, "r") as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:  # Handling corrupted JSON
                    data = [Admin_details]  
                    EmployeeRecord.save_data(data)

        # Ensure Admin is always present
        if not any(emp["emp_id"] == Admin_Id for emp in data):
            data.append(Admin_details)
            EmployeeRecord.save_data(data)

        return data
         
    @staticmethod
    def save_data(data):
        with open(Path,"w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def generate_emp_id():
        data=EmployeeRecord.load_data()
        return 1001 if not data else max(emp ["emp_id"] for emp in data)+1
    
    @staticmethod
    def authenticate_user(emp_id, password):
        data = EmployeeRecord.load_data()
        for emp in data:
            if emp ["emp_id"] == emp_id and emp ["password"] == password:
                return emp
        return None
   
    def __init__(self, name, age, department, salary, password):
        self.emp_id = self.generate_emp_id()
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
