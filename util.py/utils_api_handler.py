import pandas as pd
import os
import sys
from pathlib import Path

from utils_file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)
transactions = parse_transactions(read_sales_data('sales_data.txt'))


import requests # to make API requests

# GET ALL PRODUCTS 
response = requests.get('https://dummyjson.com/products') # make GET request to API endpoint
data = response.json()
# data['products'] contains list of all products
# data['total'] gives total count



# GET A SINGLE PRODUCT BY ID
# example pdt id 1:
response = requests.get('https://dummyjson.com/products/1')
product = response.json()
# Returns single product object
# product['id'], product['title'], product['price'], etc. can be accessed
# Example: print product title and price
print(f"Product: {product['title']}, Price: Rs {product['price']}")
# You can integrate this API data with your sales transactions as needed

# example pdt id 5:
response = requests.get('https://dummyjson.com/products/5')
product = response.json()
print(f"Product: {product['title']}, Price: Rs {product['price']}")

# GET SPECIFIC NUMBETR OF PRODUCTS

response = requests.get('https://dummyjson.com/products?limit=100')
data = response.json()
# data['products'] contains list of products limited to 100
# data['total'] gives total count
# Example: print total number of products fetched
print(f"Total Products Fetched: {len(data['products'])}")

# You can further process this data as per your requirements

# SEARCH PRODUCTS
response = requests.get('https://dummyjson.com/products/search?q=phone')

data = response.json()
# data['products'] contains list of products matching search query 'phone'  
# Example: print titles of matching products
for product in data['products']:
    print (f"""id: {product['id']}, Title: {product['title']},description : {product['description']},Price: Rs {product['price']}, 
        category: {product['category']}, brand: {product['brand']}, rating: {product['rating']}, stock: {product['stock']}""")
# You can modify the search query as needed
# You can integrate this search functionality into your application as required
# THIS CAN ALSO BE REPRESENTED AS: individual F single product object

    print (
        f"id: {product['id']}", 
        f"Title: {product['title']}",
        f"description : {product['description']}",
        f"Price: Rs {product['price']}", 
        f"category: {product['category']}", 
        f"brand: {product['brand']}", 
        f"rating: {product['rating']}", 
        f"stock: {product['stock']}"
        )
#   "id": 1,
#   "title": "iPhone 9",
#   "description": "An apple mobile...",
#   "price": 549,
#   "category": "smartphones",
#   "brand": "Apple",
#   "rating": 4.69,
#   "stock": 94


# CREATE FUNCTION - FETCH ALL PRODUCTS #

from urllib import response
import requests # to make API requests
import json # to handle JSON data

def fetch_all_products():
    url='https://dummyjson.com/products'
    response = requests.get(url)
    data = response.json()
    
    response = requests.get(url + '?limit=100') # GET request to fetch 100 products
    data = response.json()
    for product in data['products']:
        try:
            print(
            f"id: {product.get('id')}, "
            f"Title: {product.get('title')}, "
            f"description: {product.get('description')}, "
            f"Price: Rs {product.get('price')}, "
            f"category: {product.get('category')}, "
            f"brand: {product.get('brand', 'N/A')}, "
            f"rating: {product.get('rating')}, "
            f"stock: {product.get('stock')}"
            )
        except KeyError as e:
            print(f"Missing key {e} in product data: {product}")
        continue
    # data['total'] gives total count
    print(f"Total Products Fetched: {len(data['products'])}")
    return data['products']
    # return empty list if API fails
    if response.status_code != 200: # check for successful response
        print("Failed to fetch products from API.")
        return []
    else: # print status message (success/failure)
        print("Successfully fetched products from API.")
        return data['products']
print(fetch_all_products())
print("Status message: Successfully fetched products from API.")
print("Total Products Fetched: ", len(fetch_all_products()))

 

# CREATE PRODUCT MAPPING
def create_product_mapping(api_products):
    product_mapping = {}
    for product in api_products:
        try:
            product_id = product['id']
            product_mapping[product_id] = {
                'title': product['title'],
                'category': product['category'],
                'brand': product.get('brand', 'N/A'),
                'rating': product['rating']
            }
        except KeyError as e:
            print(f"Missing key {e} in product data: {product}")
            continue
    return product_mapping
print(create_product_mapping(fetch_all_products()))

    # Creates a mapping of product IDs to product info

    # Parameters: api_products from fetch_all_products()

    # Returns: dictionary mapping product IDs to info

    # Expected Output Format:
    # {
    #     1: {'title': 'iPhone 9', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.69},
    #     2: {'title': 'iPhone X', 'category': 'smartphones', 'brand': 'Apple', 'rating': 4.44},
    #     ...
    # }
    # """



# ENRICH SALES DATA (transactions) WITH API INFO #


def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for trx in transactions:
        try:
            # --- 1. Extract numeric product ID (P101 → 101) ---
            product_id_str = trx.get("ProductID", "")
            numeric_id = int(product_id_str.replace("P", ""))

            # --- 2. Check if API data exists ---
            api_data = product_mapping.get(numeric_id)

            if api_data:
                trx["API_Category"] = api_data.get("category")
                trx["API_Brand"] = api_data.get("brand")
                trx["API_Rating"] = api_data.get("rating")
                trx["API_Match"] = True
            else:
                trx["API_Category"] = None
                trx["API_Brand"] = None
                trx["API_Rating"] = None
                trx["API_Match"] = False

        except Exception:
            # --- 3. Graceful error handling ---
            trx["API_Category"] = None
            trx["API_Brand"] = None
            trx["API_Rating"] = None
            trx["API_Match"] = False

        enriched_transactions.append(trx)

    # --- 4. Write enriched data to file ---
    output_file = "enriched_sales_data.txt"

    header = [
        "TransactionID", "Date", "ProductID", "ProductName",
        "Quantity", "UnitPrice", "CustomerID", "Region",
        "API_Category", "API_Brand", "API_Rating", "API_Match"
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("|".join(header) + "\n")

        for trx in enriched_transactions:
            row = [
                str(trx.get(col, "")) for col in header
            ]
            f.write("|".join(row) + "\n")

    return enriched_transactions
print(enrich_sales_data(transactions, create_product_mapping(fetch_all_products())))
df = pd.DataFrame(enrich_sales_data(transactions, create_product_mapping(fetch_all_products())))
print(df)   

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    for trx in enriched_transactions:
        try:
            with open(filename, 'a', encoding='utf-8') as f:
                header = [
                    "TransactionID", "Date", "ProductID", "ProductName",
                    "Quantity", "UnitPrice", "CustomerID", "Region",
                    "API_Category", "API_Brand", "API_Rating", "API_Match"
                ]
                row = [str(trx.get(col, "")) for col in header] 
                f.write("|".join(row) + "\n")
        except Exception as e:
            print(f"Error writing transaction {trx.get('TransactionID', 'N/A')}: {e}")
            continue
    print("Enriched data saved to", filename)

    # Saves enriched transactions back to file

    # Expected File Format:
    # TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match
    # T001|2024-12-01|P101|Laptop|2|45000.0|C001|North|laptops|Apple|4.7|True
    # ...

    # Requirements:
    # - Create output file with all original + new fields
    # - Use pipe delimiter
    # - Handle None values appropriately
    # """



