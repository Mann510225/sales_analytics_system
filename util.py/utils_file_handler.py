
import os
import sys
from pathlib import Path
from urllib import response
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import re
from io import StringIO # treats strings like file)
pd.set_option('display.max_columns', None) # to display all columns in pandas DF

# We can read the file using pd.read_csv if file source is trusted and we know encoding be used is for UTF 8 (inbuilt in pandas).
# But, if the source is not trusted  and we do not know the encoding option whether to use (UTF 8 or  'latin-1' or  'cp1252') and also need to clean the data
# we need to go with basic def fn loop with encoding command 
# READ SALES DATA WITH ENCODING HANDLING

sales_data = pd.read_csv(r'sales_data.txt', delimiter='|', header=0,)
print(sales_data)
sales_data.info()

    # """
    # Reads sales data from file handling encoding issues

    # Returns: list of raw lines (strings)

    # Expected Output Format:
    # ['T001|2024-12-01|P101|Laptop|2|45000|C001|North', ...]

    # Requirements:
    # - Use 'with' statement
    # - Handle different encodings (try 'utf-8', 'latin-1', 'cp1252')
    # - Handle FileNotFoundError with appropriate error message
    # - Skip the header row
    # - Remove empty lines
    # """

# READ SALES DATA WITH ENCODING HANDLING
filename = 'sales_data.txt'
def read_sales_data(filename):
    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    raw_lines = []

    for encoding in encodings_to_try:
        try:
            # Open file safely using with statement
            with open(filename, mode='r', encoding=encoding) as file:

                lines = file.readlines()

                # Skip header row and clean remaining lines
                for line in lines[1:]:  # skip header
                    line = line.strip() # Skip empty lines
                    if not line:
                        continue

                    raw_lines.append(line) # Append cleaned line to raw_lines

            # If file read successfully, stop trying other encodings
            break

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []
    return raw_lines

print(read_sales_data(filename))

df=pd.read_csv('sales_data.txt', delimiter='|', header=0)
print(df)
df.__len__()


# PARSE & CLEAN DATA #

    # """
    # Parses raw lines into clean list of dictionaries

    # Returns: list of dictionaries with keys:
    # ['TransactionID', 'Date', 'ProductID', 'ProductName',
    #  'Quantity', 'UnitPrice', 'CustomerID', 'Region']

    # Expected Output Format:
    # [
    #     {
    #         'TransactionID': 'T001',
    #         'Date': '2024-12-01',
    #         'ProductID': 'P101',
    #         'ProductName': 'Laptop',
    #         'Quantity': 2,           # int type
    #         'UnitPrice': 45000.0,    # float type
    #         'CustomerID': 'C001',
    #         'Region': 'North'
    #     },
    #     ...
    # ]

    # Requirements:
    # - Split by pipe delimiter '|'
    # - Handle commas within ProductName (remove or replace)
    # - Remove commas from numeric fields and convert to proper types
    # - Convert Quantity to int
    # - Convert UnitPrice to float
    # - Skip rows with incorrect number of fields
    # """


# DATA PARSING 

raw_lines=read_sales_data('sales_data.txt')
def parse_transactions(raw_lines):
    clean_transactions = []  # final output list

    for line in raw_lines:

        # Remove leading/trailing spaces and newline characters
        line = line.strip()

        # Skip empty lines
        if not line:
            continue

        # Split line by pipe delimiter
        parts = line.split('|')

        # Skip rows with incorrect number of fields
        if len(parts) != 8:
            continue

        try:
            # Assign fields to meaningful variable names
            txn_id, date, product_id, product_name, quantity, unit_price, customer_id, region = parts

            # Clean product name (remove commas)
            product_name = product_name.replace(',', '').strip()

            # Remove commas from numeric fields
            quantity = quantity.replace(',', '').strip()
            unit_price = unit_price.replace(',', '').strip()

            # Convert data types
            quantity = int(quantity)
            unit_price = float(unit_price)

            # Create clean transaction dictionary
            transaction = {
                'TransactionID': txn_id.strip(),
                'Date': date.strip(),
                'ProductID': product_id.strip(),
                'ProductName': product_name,
                'Quantity': quantity,
                'UnitPrice': unit_price,
                'CustomerID': customer_id.strip(),
                'Region': region.strip()
            }

            # Add to final list
            clean_transactions.append(transaction)

        except ValueError:
            # Skip rows with invalid numeric conversion
            continue

    return clean_transactions
print(parse_transactions(raw_lines))


# DATA VALIDATION & FILTER ING
    # """
    # Validates transactions and applies optional filters

    # Parameters:
    # - transactions: list of transaction dictionaries
    # - region: filter by specific region (optional)
    # - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    # - max_amount: maximum transaction amount (optional)

    # Returns: tuple (valid_transactions, invalid_count, filter_summary)

    # Expected Output Format:
    # (
    #     [list of valid filtered transactions],
    #     5,  # count of invalid transactions
    #     {
    #         'total_input': 100,
    #         'invalid': 5,
    #         'filtered_by_region': 20,
    #         'filtered_by_amount': 10,
    #         'final_count': 65
    #     }
    # )

    # Validation Rules:
    # - Quantity must be > 0
    # - UnitPrice must be > 0
    # - All required fields must be present
    # - TransactionID must start with 'T'
    # - ProductID must start with 'P'
    # - CustomerID must start with 'C'

    # Filter Display:
    # - Print available regions to user before filtering
    # - Print transaction amount range (min/max) to user
    # - Show count of records after each filter applied
    # """

transactions = parse_transactions(raw_lines)

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    valid = []   # region , min & max based on filter criteria as given above
    invalid_count = 0 

    for trx in transactions: # as per validation rules & requirements 
        try:
            if trx['Quantity'] <= 0 or trx['UnitPrice'] <= 0:
                invalid_count += 1 # Invalid if quantity or unit price is non-positive otherwise continue
                continue

            if not (
                trx['TransactionID'].startswith('T') and
                trx['ProductID'].startswith('P') and
                trx['CustomerID'].startswith('C')
            ):
                invalid_count += 1 # Invalid if IDs do not start with expected letters, otherwise continue
                continue

            amount = trx['Quantity'] * trx['UnitPrice']  # Calculate the transaction amount

            if region and trx['Region'] != region: # Filter by region if specified
                continue
            if min_amount and amount < min_amount: 
                continue
            if max_amount and amount > max_amount:
                continue

            valid.append(trx) # Valid transaction after all checks . 
                                # why append here - because it passed all validation and filtering criteria

        except KeyError:  # Missing expected fields
            invalid_count += 1



# Add more detailed summary information
    Summary = {
        'total_input': len(transactions),
        'valid': len(valid),
        'invalid': invalid_count,
        'filtered_by_amount': len(transactions) - invalid_count - len(valid), 
}
    return Summary

# Better debugging output - why? To understand the distribution of valid, invalid, and filtered transactions
print(f"Transactions: {len(transactions)} total")


# Fix the None value
Summary = validate_and_filter(
    transactions, 
    region=None,  # Changed from 'None' string
    min_amount=100, 
    max_amount=1000
)
print(validate_and_filter(transactions, region=None, min_amount=100, max_amount=1000))
print(transactions)
print(Summary)

df = pd.DataFrame(transactions)
print(df)

