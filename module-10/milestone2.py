import mysql.connector
from datetime import datetime

# Not my actual password, change user and/or password to fit your user setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="your-password"
)
cursor = conn.cursor()

# Step 1: Drop and recreate the winery database
cursor.execute("DROP DATABASE IF EXISTS winery")
cursor.execute("CREATE DATABASE winery")
cursor.execute("USE winery")

# Step 2: Drop and recreate winery_user
cursor.execute("DROP USER IF EXISTS 'winery_user'@'localhost'")
cursor.execute("""
    CREATE USER 'winery_user'@'localhost'
    IDENTIFIED WITH mysql_native_password BY 'popcorn'
""")
cursor.execute("GRANT ALL PRIVILEGES ON winery.* TO 'winery_user'@'localhost'")

# Step 3: Drop tables in reverse dependency order
cursor.execute("DROP TABLE IF EXISTS timelog")
cursor.execute("DROP TABLE IF EXISTS employee")
cursor.execute("DROP TABLE IF EXISTS supply_delivery")
cursor.execute("DROP TABLE IF EXISTS inventory")
cursor.execute("DROP TABLE IF EXISTS supplier")
cursor.execute("DROP TABLE IF EXISTS `order`")
cursor.execute("DROP TABLE IF EXISTS wine_distribution")
cursor.execute("DROP TABLE IF EXISTS distributor")
cursor.execute("DROP TABLE IF EXISTS wine")

# Step 4: Create tables

cursor.execute("""
CREATE TABLE wine (
   wine_id     INT             NOT NULL        AUTO_INCREMENT,
   wine_name   VARCHAR(75)     NOT NULL,
   wine_type   VARCHAR(75)     NOT NULL,
   PRIMARY KEY(wine_id)
)
""")

cursor.execute("""
CREATE TABLE distributor (
   distributor_id   INT   NOT NULL   AUTO_INCREMENT,
   distributor_name   VARCHAR(75),
   contact   VARCHAR(20),
   PRIMARY KEY(distributor_id)
)
""")

cursor.execute("""
CREATE TABLE wine_distribution (
   distribution_id   INT 	NOT NULL AUTO_INCREMENT,
   distributor_id	INT,
   wine_id       	INT,
   quantity      	INT,
   order_date    	DATE,
   PRIMARY KEY(distribution_id),
   CONSTRAINT fk_distributor FOREIGN KEY(distributor_id)
   	REFERENCES distributor(distributor_id),
   CONSTRAINT fk_wine FOREIGN KEY(wine_id)
   	REFERENCES wine(wine_id)
)
""")

cursor.execute("""
CREATE TABLE `order` (
   order_id   	INT NOT NULL AUTO_INCREMENT,
   distributor_id INT,
   wine_id    	INT,
   quantity   	INT,
   order_date 	DATE,
   delivery_date    DATE,
   PRIMARY KEY(order_id),
   CONSTRAINT fk_order_distributor FOREIGN KEY(distributor_id)
   	REFERENCES distributor(distributor_id),
   CONSTRAINT fk_order_wine FOREIGN KEY(wine_id)
   	REFERENCES wine(wine_id)
)
""")

cursor.execute("""
CREATE TABLE supplier (
   supplier_id   INT   NOT NULL   AUTO_INCREMENT,
   item_name    VARCHAR(75),
   supply_type   VARCHAR(75),
   PRIMARY KEY(supplier_id)
)
""")

cursor.execute("""
CREATE TABLE inventory (
   inventory_id     INT             NOT NULL        AUTO_INCREMENT,
   supply_id    INT,
   item_name   VARCHAR(75)     NOT NULL,
   quantity INT,
   Last_updated DATE,
   PRIMARY KEY(inventory_id),
   CONSTRAINT fk_supplier FOREIGN KEY(supply_id) REFERENCES supplier(supplier_id)
)
""")

cursor.execute("""
CREATE TABLE supply_delivery (
   delivery_id   INT   NOT NULL    AUTO_INCREMENT,
   supplier_id   INT,
   expected_date DATE,
   actual_date   DATE,
   PRIMARY KEY(delivery_id),
   CONSTRAINT fk_supplydelivery FOREIGN KEY(supplier_id) REFERENCES supplier(supplier_id)
)
""")

cursor.execute("""
CREATE TABLE employee (
   employee_id   INT             NOT NULL        AUTO_INCREMENT,
   employee_name  VARCHAR(75)     NOT NULL,
   department   VARCHAR(75)     NOT NULL,
   PRIMARY KEY(employee_id)
)
""")

cursor.execute("""
CREATE TABLE timelog (
   timelog_id	   INT  NOT NULL  AUTO_INCREMENT,
   employee_id     INT,
   clock_in  	   DATETIME,
   clock_out 	   DATETIME,
   entry_date      DATE,
   PRIMARY KEY(timelog_id),
   CONSTRAINT fk_timelog_employee FOREIGN KEY(employee_id)
   	REFERENCES employee(employee_id)
)
""")

# Step 5: Insert sample data

cursor.executemany("INSERT INTO wine (wine_name, wine_type) VALUES (%s, %s)", [
    ("Cabernet Sauvignon", "Red"),
    ("Chardonnay", "White"),
    ("Merlot", "Red"),
    ("Riesling", "White"),
    ("Pinot Noir", "Red"),
    ("Zinfandel", "Red")
])

cursor.executemany("INSERT INTO distributor (distributor_name, contact) VALUES (%s, %s)", [
    ("Vintage Vines", "555-1111"),
    ("Global Grapes", "555-2222"),
    ("Fine Wine Co.", "555-3333")
])

cursor.executemany("INSERT INTO supplier (item_name, supply_type) VALUES (%s, %s)", [
    ("Corks", "Packaging"),
    ("Wine Bottles", "Container"),
    ("Labels", "Packaging")
])

cursor.executemany("INSERT INTO employee (employee_name, department) VALUES (%s, %s)", [
    ("Alice Johnson", "Production"),
    ("Bob Smith", "Sales"),
    ("Carol White", "Warehouse"),
    ("Dave Black", "Logistics"),
    ("Emma Green", "Quality"),
    ("Frank Brown", "Management")
])

cursor.executemany("INSERT INTO wine_distribution (distributor_id, wine_id, quantity, order_date) VALUES (%s, %s, %s, %s)", [
    (1, 1, 100, "2024-01-15"),
    (2, 2, 150, "2024-02-20"),
    (3, 3, 120, "2024-03-05"),
    (1, 4, 180, "2024-04-01"),
    (2, 5, 140, "2024-04-25"),
    (3, 6, 160, "2024-05-10")
])

cursor.executemany("INSERT INTO `order` (distributor_id, wine_id, quantity, order_date, delivery_date) VALUES (%s, %s, %s, %s, %s)", [
    (1, 1, 100, "2024-01-15", "2024-01-20"),
    (2, 2, 150, "2024-02-20", "2024-02-25"),
    (3, 3, 120, "2024-03-05", "2024-03-10"),
    (1, 4, 180, "2024-04-01", "2024-04-06"),
    (2, 5, 140, "2024-04-25", "2024-04-30"),
    (3, 6, 160, "2024-05-10", "2024-05-15")
])

cursor.executemany("INSERT INTO inventory (supply_id, item_name, quantity, Last_updated) VALUES (%s, %s, %s, %s)", [
    (1, "Corks", 1000, "2024-01-01"),
    (2, "Wine Bottles", 2000, "2024-01-02"),
    (3, "Labels", 3000, "2024-01-03")
])

cursor.executemany("INSERT INTO supply_delivery (supplier_id, expected_date, actual_date) VALUES (%s, %s, %s)", [
    (1, "2024-02-01", "2024-02-02"),
    (2, "2024-03-01", "2024-03-02"),
    (3, "2024-04-01", "2024-04-03")
])

cursor.executemany(
    "INSERT INTO timelog (employee_id, clock_in, clock_out, entry_date) VALUES (%s, %s, %s, %s)", [
        (1, "2024-05-01 08:00:00", "2024-05-01 16:00:00", "2024-05-01"),
        (2, "2024-05-01 09:00:00", "2024-05-01 17:00:00", "2024-05-01"),
        (3, "2024-05-01 07:30:00", "2024-05-01 15:30:00", "2024-05-01"),
        (4, "2024-05-01 08:30:00", "2024-05-01 16:30:00", "2024-05-01"),
        (5, "2024-05-01 09:15:00", "2024-05-01 17:15:00", "2024-05-01"),
        (6, "2024-05-01 10:00:00", "2024-05-01 18:00:00", "2024-05-01")
])

conn.commit()

# Step 6: Display contents of all tables
tables = ["wine", "distributor", "wine_distribution", "`order`", "supplier", "inventory", "supply_delivery", "employee", "timelog"]

for table in tables:
    print(f"\n--- {table.upper()} ---")
    cursor.execute(f"SELECT * FROM {table}")
    for row in cursor.fetchall():
        print(row)

# === Cleanup ===
cursor.close()
conn.close()
