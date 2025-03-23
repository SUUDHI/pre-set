class EmployeeDisplay:
    @staticmethod
    def show_message(message):
        print(message)
    
    @staticmethod
    def get_input(prompt):
        return input(prompt)
    
    @staticmethod
    def show_employee_details(employee):
        if not employee:
            print("No employee details found.")
            return

        print("Employee details")
        print(f"ID: {employee[0]}")
        print(f"Name: {employee[1]}")
        print(f"Age: {employee[2]}")
        print(f"Department: {employee[3]}")
        print(f"Salary: {employee[4]}")
