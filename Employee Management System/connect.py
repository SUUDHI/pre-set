import sqlite3

def connect_db():
    return sqlite3.connect("Emp.DB")

def initialize_database():
    connect = connect_db()
    cursor = connect.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER CHECK(age >= 18),
            department TEXT,
            salary REAL CHECK(salary > 0),
            password TEXT NOT NULL
        )
    """)
    #checking admin
    cursor.execute("SELECT * FROM Employee WHERE emp_id = 1000")
    admin = cursor.fetchone()

    if not admin:
        cursor.execute("""
            INSERT INTO Employee (emp_id, name, age, department, salary, password)
            VALUES (1000, 'Admin', 35, 'Management', 100000, 'Admin1234')
        """)
        connect.commit()

    connect.close()

#
initialize_database()


