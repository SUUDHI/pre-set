import json

# File path
sales_data = r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\sales_data.csv"  

# Read the file manually
with open(sales_data, "r") as file:
    lines = file.readlines()

# Extract headers (first row) and clean them
headers = lines[0].strip().split(",")

# Process each row manually
data = []
for line in lines[1:]:  # Skip header row
    values = line.strip().split(",")  # Split values by comma
    row_dict = {headers[i]: values[i] for i in range(len(headers))}  # Map values to headers
    row_dict["Amount"] = float(row_dict["Amount"])  # Convert "Amount" to float for calculations
    data.append(row_dict)

# 1. Count total sales records
total_sales = len(data)

# 2. Calculate total revenue
total_revenue = sum(row["Amount"] for row in data)

# 3. Find Top 3 Highest Sales Transactions Without Using `sorted()`
def selection_sort(arr):
    """Sorts the list in descending order using Selection Sort."""
    n = len(arr)
    for i in range(n):
        max_idx = i
        for j in range(i + 1, n):
            if arr[j]["Amount"] > arr[max_idx]["Amount"]:
                max_idx = j
        # Swap elements
        arr[i], arr[max_idx] = arr[max_idx], arr[i]

# Sort data using Selection Sort
selection_sort(data)

# Get the top 3 highest sales
top_sales = data[:3]

# Display results
print("Total Sales Records:", total_sales)
print("Total Revenue:", total_revenue)
print("\nTop 3 Highest Sales Transactions:")
for sale in top_sales:
    print(sale)
