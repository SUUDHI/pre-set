import csv
import json

data=[]

with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\sales_data.csv") as File:
    reader = csv.DictReader(File)
    for row in reader:
        data.append(row)

with open(r"C:\cprogramming\GIt_demo\pre-set\Sampal_Data\sales-data.json", "w") as File:
    json.dump(data, File, indent=4)

Total_Sales = len(data)
print("Total Sales: ", Total_Sales)
        
calculate_revenue = 0
for row in data:
    calculate_revenue += float(row["Amount"])
print("Total Ravenu: ", calculate_revenue)

sales_data = data
sorted_sales = sorted(sales_data, key=lambda x: float(x["Amount"]), reverse=True)
top_sales= sorted_sales[:3]
for sale in top_sales:
    print(sale)
          