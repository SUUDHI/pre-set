from controller import EmployeeController
from view import EmployeeView

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
                        EmployeeView.show_message("\nWelcome Admin")
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
