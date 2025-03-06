import json

# File paths
Sample_data = r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\sales_data.csv"
sample_json = r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\sales_data.json"

# Read the CSV file manually
with open(Sample_data, "r") as file:
    lines = file.readlines()

# Extract headers (first row)
headers = lines[0].strip().split(",")

# Process CSV rows into a list of dictionaries
data = []
for line in lines[1:]:  # Skip the header row
    values = line.strip().split(",")
    row_dict = {headers[i]: values[i] for i in range(len(headers))}
    row_dict["Amount"] = float(row_dict["Amount"])  # Convert "Amount" to float
    data.append(row_dict)

# Save data to JSON file
with open(sample_json, "w") as json_file:
    json.dump(data, json_file, indent=4)

# Display the JSON file content
with open(sample_json, "r") as json_file:
    json_content = json.load(json_file)

# Print JSON content
print(json.dumps(json_content, indent=4))
