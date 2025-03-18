from controller import EmployeeManager
from view import EmployeeDisplay
from model import EmployeeRecord
from constant import Admin_Id


#main fun
def main():
    controller = EmployeeManager()

    while True:
        EmployeeDisplay.show_message("     WELCOME     ")
        EmployeeDisplay.show_message("1.login")
        EmployeeDisplay.show_message("2.Register")
        EmployeeDisplay.show_message("3.Exit")

        choice = EmployeeDisplay.get_input("Enter your choice:")

        if choice == "1":
            emp_id = int(EmployeeDisplay.get_input("Enter Employee Id:"))
            password=EmployeeDisplay.get_input("Enter your password:")
            employee = EmployeeRecord.authenticate_user(emp_id, password)

            if employee:
                EmployeeDisplay.show_message("Login Successfully!")
                if emp_id == Admin_Id:
                    while True:
                        EmployeeDisplay.show_message("\nWelcome Admin")
                        EmployeeDisplay.show_message("1.View all employee.")
                        EmployeeDisplay.show_message("2.Remove a employee.")
                        EmployeeDisplay.show_message("3.Logout.")

                        Admin_choice =EmployeeDisplay.get_input("Enter Choice:")

                        if Admin_choice == "1":
                            controller.view_all_employee()
                        elif Admin_choice == "2":
                            emp_id = int(EmployeeDisplay.get_input("Enter Employee ID to delete: "))
                            controller.delete_employee(emp_id)
                        elif Admin_choice == "3":
                            break
                
                else:
                    while True:
                        EmployeeDisplay.show_message("Welcome Employee!")
                        EmployeeDisplay.show_message("1.View Details.")
                        EmployeeDisplay.show_message("2.Update Details.")
                        EmployeeDisplay.show_message("3.Logout.")
                        
                        Emp_choice = EmployeeDisplay.get_input("Enter your Choice")

                        if Emp_choice == "1":
                            EmployeeDisplay.show_employee_details(employee)
                        elif Emp_choice == "2":
                            controller.update_employee_details(employee)
                        elif Emp_choice == "3":
                            break

            else:
                EmployeeDisplay.show_message("Invilid ID")
        elif choice == "2":
            controller.register_employee()
        
        elif choice == "3":
            EmployeeDisplay.show_message("Exiting the system.")
            break
        else:
            EmployeeDisplay.show_message("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
