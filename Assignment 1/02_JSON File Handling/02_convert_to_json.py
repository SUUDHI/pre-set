import json

# List to store employee data
Emp_data = []

# Open and read the text file
with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.txt", "r") as file:
    for line in file:
        # Strip newline and split by ", "
        data = line.strip().split(", ")

        # Ensure the line has exactly 4 values (ID, Name, Age, Department)
        if len(data) == 4:
            emp_dict = {
                "ID": data[0],
                "Name": data[1],
                "Age": int(data[2]),  # Convert age to integer
                "Department": data[3]
            }
            Emp_data.append(emp_dict)

# Save data to a JSON file
with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.json", "w") as json_file:
    json.dump(Emp_data, json_file, indent=4)

print("Data successfully converted to JSON and saved as EMP-1.json!")
with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\EMP-1.json", "r") as json_file:
    print(json_file.read())
