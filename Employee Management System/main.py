
from view import EmployeeDisplay
from modle_01 import EmployeeRecord
from controller import EmployeeManager , AdminManager 
from constant import ADMIN_ID , INVALID_CHOICE

def main():
    controller = EmployeeManager()
    admin_controller = AdminManager()

    while True:
        EmployeeDisplay.show_message("     WELCOME     ")
        EmployeeDisplay.show_message("1.login")
        EmployeeDisplay.show_message("2.Register")
        EmployeeDisplay.show_message("3.Exit")

        try:
            choice = int(EmployeeDisplay.get_input("Enter your choice:"))
            
        except ValueError:
            EmployeeDisplay.show_message(INVALID_CHOICE)
            continue

        if choice == 1:
            try:    
                emp_id = int(EmployeeDisplay.get_input("Enter Employee Id:"))
                password = EmployeeDisplay.get_input("Enter your password:")
                employee = EmployeeRecord.authenticate_user(emp_id, password)
            except ValueError:
                EmployeeDisplay.show_message("Enter ID or Password, It can't be empty. ")
                continue
            
            if employee:
                EmployeeDisplay.show_message("Login Successfully!")
                if emp_id == ADMIN_ID:
                    while True:
                        EmployeeDisplay.show_message("\nWelcome Admin")
                        EmployeeDisplay.show_message("1.View all employee.")
                        EmployeeDisplay.show_message("2.Remove a employee.")
                        EmployeeDisplay.show_message("3.Logout.")

                        try:
                            Admin_choice = int(EmployeeDisplay.get_input("Enter Choice:"))
                        except ValueError:
                            EmployeeDisplay.show_message(INVALID_CHOICE)
                            continue

                        if Admin_choice == 1:
                            admin_controller.view_all_employee()
                        elif Admin_choice == 2:
                            try:
                                emp_id = int(EmployeeDisplay.get_input("Enter Employee ID to delete: "))
                                admin_controller.delete_employee(emp_id)
                            except ValueError:
                                EmployeeDisplay.show_message("Invalid input! Employee ID must be a number.")
                        elif Admin_choice == 3:
                            break
                        else:
                            EmployeeDisplay.show_message(INVALID_CHOICE)
                
                else:
                    while True:
                        EmployeeDisplay.show_message("Welcome Employee!")
                        EmployeeDisplay.show_message("1.View Details.")
                        EmployeeDisplay.show_message("2.Update Details.")
                        EmployeeDisplay.show_message("3.Logout.")

                        try:
                            Emp_choice = int(
                                EmployeeDisplay.get_input("Enter your Choice:")
                                )
                        except ValueError:
                            EmployeeDisplay.show_message(INVALID_CHOICE) 
                            continue   
                        if Emp_choice == 1:
                            EmployeeDisplay.show_employee_details(employee)
                        elif Emp_choice == 2:
                            controller.update_employee_details(employee[0])
                        elif Emp_choice == 3:
                            break
                        else:
                            EmployeeDisplay.show_message(INVALID_CHOICE)

            else:
                EmployeeDisplay.show_message("Invilid ID Or Password")
        elif choice == 2:
            controller.register_employee()
        
        elif choice == 3:
            EmployeeDisplay.show_message("Exiting the system.")
            break
        else:
            EmployeeDisplay.show_message(INVALID_CHOICE)
        
if __name__ == "__main__":
    main()
