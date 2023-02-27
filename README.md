# Shopify API -> SQLite Database
This program uses Python to pull year-to-date order data from Shopify's API and load it into a SQLite database. Providing an example of how users can freely load their ecommerce data into a database.

# Prerequisites and Dependencies 
To run this program the user will require a PC with the following programs, packages and accounts:
- Shopify developers account with permission to create a custom app
- Python installed with the following packages:
  - requests, json, sqlite3
- SQLite installed
- Command Prompt

Python Download Link: https://www.python.org/downloads/
SQLite Download Link: https://sqlitebrowser.org/dl/

Please note that this program will only work for API versions from 2023 onwards.

# Creating custom app in Shopify
Go to: 
https://{your-store-name}.myshopify.com/admin/settings/apps/development

Create an App

Review the configuration to allow API access to: read_inventory, read_orders.

Note down the API Access Token and API version (webhook version) keep these secure. 

# Running the Program

Save the file as a Python file and run the program in the command prompt. The program will prompt the user to enter their store name, access token and API version. 

The program works by pulling JSON data from an API, bypassing Shopifys pagnation by linking through headers to create a list of order data. It then connects to SQLite to create a database, creating a table within that database called "order_data". The program then uses a for loop to parse the information in the orders list and pull out the deisred information, committing it to the database. 

# Results, limitations and use cases

The result should be a table created with order, product and sales information from the beginning of the year stored in a database. This program is just an example of some of the data that you can pull using the Shopify API. With simple modifications you can amend the code to adjust the start-date range: 

      end_date = datetime.now().date()
      start_date = end_date - timedelta(days=2)

      url = f"https://{store_name}.myshopify.com/admin/api/{api_version}/orders.json?status=any&created_at_min={start_date}"
      
The above example changes the start date to 2 days ago. Once you ran the initial program to get YTD sales, you could set up a task scheduler to run this amended code daily to improve performance and automate uploads. 

You can also amend the data you wish to load into the database by printing out the JSON data and amending the for loop with the desired data.

Finally, you can amend the URL with the parameters found here: 
https://shopify.dev/docs/api/admin-rest/2022-10/resources/order#get-orders?status=any

Adjusting the parameters, you can filter certain feilds, date ranges, order status etc. 

I use this program as part of an automated stock-reorder model in conjustion with inventory data that I pull from Shopify and purchased stock that I pull from Unleashed (WMS) API. The sales data provided informs sales trends that can be used to inform stock re-orders.

You can also connect your database to Tableau to create live dashboards. 

I hope you find this example useful and that it provides a base for you to start utilising Shopify's API. 
