import requests
import json
import sqlite3

# Define the store name, access token, and API version
store_name = input("Enter Store Name: ")
access_token = input("Enter Access Token: ")
api_version = input("Enter API Version: ")

# Set API Header
headers = {"X-Shopify-Access-Token": access_token}

# Define the API endpoint URL with the beginning of the year as a filter
url = f"https://{store_name}.myshopify.com/admin/api/{api_version}/orders.json?status=any&created_at_min=2023-01-01"

# Create an empty list to hold the orders data
orders = []

# Make the API requests and follow the "Link" header to get all the results
while url:
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        #Converting the response to JSON
        data = response.json()
        orders += data["orders"]
        
        #Checking link header and following the link to get more results
        link_header = response.headers.get("Link")
        if not link_header:
            break

        next_link = None
        links = link_header.split(", ")
        for link in links:
            if "rel=\"next\"" in link:
                next_link = link.split("; ")[0][1:-1]
                url = next_link
                break

        if not next_link:
            break
    else:
        print("Request failed with status code", response.status_code)
        break
        
# Connecting to SQLite Database and creating cursor object
conn = sqlite3.connect("Ecommerce_Data.db")
cursor = conn.cursor()
print("Connected to Database")

# Creating the order_data table unless it already exists
cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_data (
        order_date_time TEXT,
        order_number INTEGER,
        product_title TEXT,
        sku TEXT,
        quantity INTEGER,
        gross_sales REAL,
        tax FLOAT,
        discount FLOAT,
        total_sales REAL
    )""")

# Iterate through the orders and line items, and insert the data into the "order_data" table
for order in orders:
    order_date_time = order["processed_at"]
    order_number = order["name"]
    for line_item in order["line_items"]:
        product_title = line_item["title"]
        sku = line_item["sku"]
        quantity = line_item["quantity"]
        gross_sales = line_item["pre_tax_price"]
        total_sales = line_item["price"]
        discount = line_item["total_discount"]
        for tax_lines in line_item:
            tax = line_item["tax_lines"][0]["price"] if "tax_lines" in line_item and line_item["tax_lines"] else 0
             # Check if the data already exists in the table
            cursor.execute("""
                SELECT * FROM order_data 
                WHERE product_title = ? 
                AND sku = ? 
                AND order_date_time = ? 
                ORDER BY order_number DESC LIMIT 1
                """, (product_title, sku, order_date_time))
        
            existing_row = cursor.fetchone()
        
            # Insert the data only if it does not already exist
            if not existing_row:
                cursor.execute("""
                INSERT INTO order_data (order_date_time, order_number, product_title, sku, quantity, gross_sales, tax, discount, total_sales)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (order_date_time, order_number, product_title, sku, quantity, gross_sales, tax, discount, total_sales))
        

# Commit the changes and close the connection
conn.commit()
print("Orders Committed")
conn.close()
print("Connection Closed")






    