class EmployeeDisplay:
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
