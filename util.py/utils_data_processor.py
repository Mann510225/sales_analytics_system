import pandas as pd

from utils_file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)

# TOTAL REVENUE CALCULATION

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions.
    """
    total_revenue = 0.0

    for trx in transactions:
        try:
            total_revenue += trx['Quantity'] * trx['UnitPrice']
        except KeyError:
            continue

    return total_revenue


if __name__ == "__main__":

    # Read and parse sales data
    sales_data = read_sales_data('sales_data.txt')
    transactions = parse_transactions(sales_data)

    # Calculate total revenue
    total_revenue = calculate_total_revenue(transactions)
    print(f"Total Revenue: Rs {total_revenue:,.2f}")

    # Validate and filter
    summary = validate_and_filter(
        transactions,
        region='North',
        min_amount=100,
        max_amount=1000
    )
    print(summary)

    # REGIONWISE SALES ANALYSIS

def region_wise_sales(transactions):
    region_stats = {} # dictionary to hold region-wise stats
    grand_total_sales = 0.0 # total sales across all regions . why 0 ? = initial value

    for trx in transactions:
        if 'Region' not in trx:
            continue
        region = trx['Region'] # get region from transaction
        amount = trx['Quantity'] * trx['UnitPrice']
        grand_total_sales += amount # accumulate grand total sales (add amount over and over)
        if region not in region_stats: # if region not in region_stats dict , then initialize it
            region_stats[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }
        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
    for region, stats in region_stats.items(): # calculate percentage contribution of each region to grand total sales
        stats['percentage'] = (stats['total_sales'] / grand_total_sales * 100) if grand_total_sales > 0 else 0.0
    # Sort regions by total_sales in descending order
    sorted_region_stats = dict(sorted(region_stats.items(), key=lambda item: item[1]['total_sales'], reverse=True))
    return sorted_region_stats
region_analysis = region_wise_sales(transactions)
print(region_analysis)
df= pd.DataFrame(region_analysis).T  # Transpose to get regions as rows
print(df)
    
# TOP SELLING PRODUCTS

def top_selling_products(transactions, n=5):
    # """
    # Returns top N selling products based on total quantity sold.

    # Output format:
    # [
    #     ('Laptop', 25, 1125000.0),
    #     ('Mouse', 40, 80000.0)
    # ]
    # """

    product_stats = {} # 

    for trx in transactions:

        # Validate required fields - why ? to avoid KeyError like below 
        if 'ProductName' not in trx or 'Quantity' not in trx or 'UnitPrice' not in trx:  
            continue

        product = trx['ProductName'] # get product name from transaction
        quantity = trx['Quantity']
        revenue = quantity * trx['UnitPrice']

        # Initialize product if not present
        if product not in product_stats:
            product_stats[product] = {
                'TotalQuantity': 0,
                'TotalRevenue': 0.0
            }

        # Aggregate values
        product_stats[product]['TotalQuantity'] += quantity
        product_stats[product]['TotalRevenue'] += revenue

    # Sort by TotalQuantity (descending)
    sorted_products = sorted(
        [(p, v['TotalQuantity'], v['TotalRevenue']) for p, v in product_stats.items()], # tuple list of (ProductName, TotalQuantity, TotalRevenue)
        # p = ProductName , v = {'TotalQuantity': x, 'TotalRevenue': y}
        key=lambda x: x[1], # lambda x : x[1] means sort by second element of tuple which is TotalQuantity
        reverse=True
    )

    return sorted_products[:n]
print(top_selling_products(transactions, n=5))

df = pd.DataFrame(top_selling_products(transactions, n=5), columns=['ProductName', 'TotalQuantity', 'TotalRevenue'])
print(df)

# CUSTOMER PURCHASE ANALYSIS

def customer_analysis(transactions):
    customer_stats = {}
    for trx in transactions:
        customer_id = trx['CustomerID']
        amount = trx['Quantity'] * trx['UnitPrice']
        product_name = trx['ProductName']

        if customer_id not in customer_stats:
            customer_stats[customer_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_stats[customer_id]['total_spent'] += amount
        customer_stats[customer_id]['purchase_count'] += 1
        customer_stats[customer_id]['products_bought'].add(product_name)
    # Finalize average order value and convert products_bought to list
    for customer_id, stats in customer_stats.items():
        stats['avg_order_value'] = stats['total_spent'] / stats['purchase_count'] if stats['purchase_count'] > 0 else 0.0
        stats['products_bought'] = list(stats['products_bought'])
    # Sort by total_spent descending
    sorted_customer_stats = dict(sorted(customer_stats.items(), key=lambda item: item[1]['total_spent'], reverse=True))
    return sorted_customer_stats
print(customer_analysis(transactions))
df = pd.DataFrame(customer_analysis(transactions)).T
print(df)

  
    # """
    # Analyzes customer purchase patterns

    # Returns: dictionary of customer statistics

    # Expected Output Format:
    # {
    #     'C001': {
    #         'total_spent': 95000.0,
    #         'purchase_count': 3,
    #         'avg_order_value': 31666.67,
    #         'products_bought': ['Laptop', 'Mouse', 'Keyboard']
    #     },
    #     'C002': {...},
    #     ...
    # }

    # Requirements:
    # - Calculate total amount spent per customer
    # - Count number of purchases
    # - Calculate average order value
    # - List unique products bought
    # - Sort by total_spent descending
    # """

# Daily sales trend analysis

def daily_sales_trend(transactions):
    daily_stats = {}
    for trx in transactions:
        date = trx['Date']
        amount = trx['Quantity'] * trx['UnitPrice']
        customer_id = trx['CustomerID']

        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'unique_customers': set()
            }

        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['unique_customers'].add(customer_id)
    # Finalize unique_customers count
    for date, stats in daily_stats.items():
        stats['unique_customers'] = len(stats['unique_customers'])
    # Sort by date
    sorted_daily_stats = dict(sorted(daily_stats.items()))
    return sorted_daily_stats
print(daily_sales_trend(transactions))
df = pd.DataFrame(daily_sales_trend(transactions)).T
print(df)
    # """
    # Analyzes sales trends by date

    # Returns: dictionary sorted by date

    # Expected Output Format:
    # {
    #     '2024-12-01': {
    #         'revenue': 125000.0,
    #         'transaction_count': 8,
    #         'unique_customers': 6
    #     },
    #     '2024-12-02': {...},
    #     ...
    # }

    # Requirements:
    # - Group by date
    # - Calculate daily revenue
    # - Count daily transactions
    # - Count unique customers per day
    # - Sort chronologically
    # """

# PEAK SALES DAY

def find_peak_sales_day(transactions):

    daily_stats = daily_sales_trend(transactions)
    peak_day = None
    max_revenue = 0.0
    transaction_count = 0
    for date, stats in daily_stats.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_day = date
            transaction_count = stats['transaction_count']
    return (peak_day, max_revenue, transaction_count)
print(find_peak_sales_day(transactions))
    # """
    # Identifies the date with highest revenue

    # Returns: tuple (date, revenue, transaction_count)

    # Expected Output Format:
    # ('2024-12-15', 185000.0, 12)
    # """

# LOW PERFORMING PRODUCTS
def low_performing_products(transactions, threshold=10):
    product_stats = {}
    for trx in transactions:
        product = trx['ProductName']
        quantity = trx['Quantity']
        revenue = quantity * trx['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'TotalQuantity': 0,
                'TotalRevenue': 0.0
            }

        product_stats[product]['TotalQuantity'] += quantity
        product_stats[product]['TotalRevenue'] += revenue
    low_performers = [
        (product, stats['TotalQuantity'], stats['TotalRevenue'])
        for product, stats in product_stats.items()
        if stats['TotalQuantity'] < threshold
    ]
    low_performers.sort(key=lambda x: x[1])  # Sort by TotalQuantity ascending
    return low_performers
print(low_performing_products(transactions))

    # """
    # Identifies products with low sales

    # Returns: list of tuples

    # Expected Output Format:
    # [
    #     ('Webcam', 4, 12000.0),  # (ProductName, TotalQuantity, TotalRevenue)
    #     ('Headphones', 7, 10500.0),
    #     ...
    # ]

    # Requirements:
    # - Find products with total quantity < threshold
    # - Include total quantity and revenue
    # - Sort by TotalQuantity ascending
    # """

df = pd.DataFrame(low_performing_products(transactions), columns=['ProductName', 'TotalQuantity', 'TotalRevenue'])
print(df)

