import json
import os

Path=(r"C:\cprogramming\GIt_demo\pre-set\Employee Management System\employees.json")

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
