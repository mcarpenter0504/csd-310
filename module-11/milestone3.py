import mysql.connector
from datetime import datetime, timedelta

# === Helper: Print tables with centered columns ===
def print_centered_table(headers, rows, width=20):
    # Center and print header row
    header_row = " | ".join(str(h).center(width) for h in headers)
    print(header_row)
    print("-" * len(header_row))

    # Center and print each row
    for row in rows:
        print(" | ".join(str(cell).center(width) for cell in row))

# === Connect to the winery database ===
conn = mysql.connector.connect(
    #REPLACE WITH DOTENV FILE
    host="localhost",
    user="root",
    #Change to your password or .env credentials
    password="Spring2025#",
    database="winery"
)
cursor = conn.cursor()

# === REPORT 1: Supplier Delivery Timeliness ===
print("\n=== REPORT 1: Supplier Delivery Timeliness ===\n")

query1 = """
SELECT 
    supplier.item_name,
    MONTH(supply_delivery.expected_date) AS month,
    YEAR(supply_delivery.expected_date) AS year,
    DATEDIFF(supply_delivery.actual_date, supply_delivery.expected_date) AS delay_days
FROM 
    supply_delivery
JOIN 
    supplier ON supply_delivery.supplier_id = supplier.supplier_id
ORDER BY 
    year, month, supplier.item_name;
"""

cursor.execute(query1)
rows1 = cursor.fetchall()

if not rows1:
    print("No delivery data found.\n")
else:
    print_centered_table(
        ["Item Name", "Month", "Year", "Delay Days"],
        rows1
    )

# === REPORT 2: Wine Distribution Summary ===
print("\n=== REPORT 2: Wine Distribution Summary ===\n")

query2 = """
SELECT 
    wine.wine_name,
    distributor.distributor_name,
    SUM(wine_distribution.quantity) AS total_quantity
FROM 
    wine_distribution
JOIN 
    wine ON wine_distribution.wine_id = wine.wine_id
JOIN 
    distributor ON wine_distribution.distributor_id = distributor.distributor_id
GROUP BY 
    wine.wine_name, distributor.distributor_name
ORDER BY 
    total_quantity ASC;
"""

cursor.execute(query2)
rows2 = cursor.fetchall()

if not rows2:
    print("No wine distribution data found.\n")
else:
    print_centered_table(
        ["Wine Name", "Distributor", "Total Quantity"],
        rows2
    )


# === REPORT 3: Employee Work Hours (Last 4 Quarters) ===
print("\n=== REPORT 3: Employee Work Hours (Last 4 Quarters) ===\n")

# Get date one year ago from today
one_year_ago = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

query3 = """
SELECT 
    employee.employee_name,
    QUARTER(timelog.entry_date) AS quarter,
    YEAR(timelog.entry_date) AS year,
    ROUND(SUM(TIMESTAMPDIFF(MINUTE, timelog.clock_in, timelog.clock_out) / 60), 2) AS total_hours
FROM 
    timelog
JOIN 
    employee ON timelog.employee_id = employee.employee_id
WHERE 
    timelog.entry_date >= %s
GROUP BY 
    employee.employee_name, year, quarter
ORDER BY 
    employee.employee_name, year, quarter;
"""

cursor.execute(query3, (one_year_ago,))
rows3 = cursor.fetchall()

if not rows3:
    print("No employee time log data found.\n")
else:
    print_centered_table(
        ["Employee", "Quarter", "Year", "Total Hours"],
        rows3
    )

# === Cleanup ===
cursor.close()
conn.close()
