import sqlite3
from connect import * 
from view import EmployeeDisplay 

class Employe_r:
    def __init__(self, name, age, department, salary, password):
        self.emp_id = Employe_r.generate_emp_id()
        self.name = name
        self.age = age
        self.department = department
        self.salary = salary
        self.password = password


    @staticmethod
    def Connect_db():
        return sqlite3.connect("EMP.DB")

    @staticmethod
    def save_employee(name, age, department, salary, password):
        connect = Employe_r.Connect_db()
        cursor = connect.cursor()
        cursor.execute("""
                    INSERT INTO Employee(name, age, department, salary, password)
                    VALUES(?,?,?,?,?)
        """,(name, age, department, salary, password))

        new_emp_id = cursor.lastrowid

        connect.commit()
        connect.close()

        return new_emp_id
        #EmployeeDisplay.show_message("Employee add successfully!")

    @staticmethod
    def Load_all_employee():
        connect = Employe_r.Connect_db()
        cursor = connect.cursor()
        cursor.execute(" SELECT * FROM Employee")
        employees = cursor.fetchall()
        connect.close()  
        return employees

    @staticmethod
    def Authenticate_user(emp_id, password):
        connect = Employe_r.Connect_db()
        cursor = connect.cursor()
        cursor.execute("SELECT * FROM Employee WHERE emp_id = ? AND password = ?", (emp_id, password))
        user = cursor.fetchone()

        return user
    
    @staticmethod
    def generate_emp_id():
        #Fetch the next available employee ID, starting from 1001.
        connect = Employe_r.connect_db()
        cursor = connect.cursor()

        cursor.execute("SELECT MAX(emp_id) FROM Employee WHERE emp_id >= 1001")
        last_emp_id = cursor.fetchone()[0]

        connect.close()

        return 1001 if last_emp_id is None else last_emp_id + 1
