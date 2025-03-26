from view import *

#Below function's are using to take input and validate input. 
class Utility:
    @staticmethod
    def validate_name(name):
        if name.isdigit():
            EmployeeDisplay.show_message("Please input Character!")
            return False
        else:
            return True
        
    @staticmethod
    def input_name():
        while True:
            name = EmployeeDisplay.get_input("Enter your Name:").strip()
            if name:
                if Utility.validate_name(name):
                    return name 
            else:
                EmployeeDisplay.show_message("Please input Character name cant be empty.")   

   
    
    @staticmethod
    def input_age():
        while True:  
                age = EmployeeDisplay.get_input("Enter your Age:").strip()
                if age:
                    if Utility.validate_age(age):
                        return age
                    EmployeeDisplay.show_message("Invalid input! Age must be a number and at least 18.")
                else:
                    EmployeeDisplay.show_message("Invalid input! Empty space.")         

    @staticmethod
    def validate_age(age):

        return age.isdigit() and int(age) >= 18

    @staticmethod
    def input_salary():
        while True:
                salary = EmployeeDisplay.get_input("Enter your Salary:").strip()
                if salary:
                    if Utility.validate_salary(salary):
                        return salary
                    EmployeeDisplay.show_message("Invalid input! salary must be numeric and greter then 0.")
                else:
                    EmployeeDisplay.show_message("Invalid input! Empty space.")

    @staticmethod       
    def validate_salary(salary):

        return salary.isdigit() and int(salary) > 0

    @staticmethod
    def input_password():
        while True:
                EmployeeDisplay.show_message("At least 8 characters long,\n Contains both uppercase and lowercase letters,\n Includes at least one number")
                
                password = EmployeeDisplay.get_input("Enter Password:").strip()
                
                if Utility.validate_password(password):
                    return password
                else:
                    EmployeeDisplay.show_message("Weak password! Enter at least 8 characters, including uppercase, lowercase, and digits.")

    @staticmethod
    def validate_password(password):
        has_valid_length  = len(password) >= 8
        has_lowercase  = False
        has_uppercase = False
        has_digit  = False

        for char in password:
            if 'A'<= char <= 'Z':
                has_uppercase = True
            if 'a'<= char <= 'z':
                has_lowercase  = True
            if '0' <= char <= '9':
                has_digit  = True

        return has_valid_length  and has_lowercase  and has_uppercase and has_digit 
            
    #Below function's are used to update the employee details and validate them.
    @staticmethod
    def update_salary():
        salary = EmployeeDisplay.get_input("Enter Salary:").strip()

        if salary:
            if Utility.validate_salary(salary):
                return int(salary)
            EmployeeDisplay.show_message("Invalid input! Salary must be a positive number.")
        
    @staticmethod
    def update_age():
        age = EmployeeDisplay.get_input("Enter age:").strip()
        
        if age:
            if Utility.validate_age(age):
                return int(age)
        
            
    @staticmethod
    def update_department():
        department = EmployeeDisplay.get_input("Enter Department:").strip()
        if department:
            return department

    @staticmethod
    def update_name():
        name = EmployeeDisplay.get_input("Enter Name:").strip()
        if name:
            if Utility.validate_name(name):
                return name
        
    @staticmethod
    def update_password():

        password = EmployeeDisplay.get_input("Enter Password:").strip()
        if password:
            if Utility.validate_password(password):
                return password
        