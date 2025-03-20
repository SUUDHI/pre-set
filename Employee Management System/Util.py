from view import *

@staticmethod
def age_Validation():
    while True:  
            try:
                age = int(EmployeeDisplay.get_input("Enter your Age:"))
                if age < 18:
                    EmployeeDisplay.show_message("Age must be at least 18. Please enter a valid age.")
                    continue
                return age
            except ValueError:
                EmployeeDisplay.show_message("Invalid input. Please enter a numeric age.")
            
@staticmethod
def Input_salary():
    while True:
        try:
            salary = int(EmployeeDisplay.get_input("Enter your Salary:"))
            if salary <= 0:
                EmployeeDisplay.show_message("Salary must be a positive number or Grater then 0. Please try again.")
                continue
            return salary
        except ValueError:  
            EmployeeDisplay.show_message("Invalid input. Please enter a numeric salary value.")

@staticmethod
def Input_Password():
     while True:
            EmployeeDisplay.show_message("At least 8 characters long,\n Contains both uppercase and lowercase letters,\n Includes at least one number")
            password = EmployeeDisplay.get_input("Enter Password:")

            passwd_len = len(password) >= 8
            Lower_case_check = False
            Upper_case_check = False
            digit_check = False

            for char in password:
                if 'A'<= char <= 'Z':
                 Upper_case_check = True
                if 'a'<= char <= 'z':
                    Lower_case_check = True
                if '0' <= char <= '9':
                    digit_check = True

            if passwd_len and Lower_case_check and Upper_case_check and digit_check:
                return password
            else:
                EmployeeDisplay.show_message("Week, enter stronge password")
            