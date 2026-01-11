import os
import pandas as pd
from collections import defaultdict # for aggregating data  
from datetime import datetime
from utils_file_handler import (
    read_sales_data,
    parse_transactions,
    validate_and_filter
)
transactions = parse_transactions(read_sales_data('sales_data.txt'))
enriched_transactions = []  # Assume this is populated elsewhere

def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    with open(output_file, 'w', encoding='utf-8') as f:
        # --- 1. HEADER ---
        f.write("============================================\n")
        f.write("       SALES ANALYTICS REPORT\n")
        f.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"     Records Processed: {len(transactions)}\n")
        f.write("============================================\n\n")

        # --- 2. OVERALL SUMMARY ---
        f.write("OVERALL SUMMARY\n")
        f.write("--------------------------------------------\n")
        total_revenue = sum(trx['Quantity'] * trx['UnitPrice'] for trx in transactions)
        total_transactions = len(transactions)
        avg_order_value = total_revenue / total_transactions
        date_format = "%Y-%m-%d"
        dates = [datetime.strptime(trx['Date'], date_format) for trx in transactions]
        date_range = f"{min(dates).strftime(date_format)} to {max(dates).strftime(date_format)}"
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")
        # --- 3. REGION-WISE PERFORMANCE ---
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Region':<10} {'Sales':<15} {'% of Total':<12} {'Transactions':<12}\n")
        region_data = defaultdict(lambda: {'sales': 0, 'transactions': 0})
        for trx in transactions:
            region = trx['Region']
            amount = trx['Quantity'] * trx['UnitPrice']
            region_data[region]['sales'] += amount
            region_data[region]['transactions'] += 1
        for region, data in sorted(region_data.items(), key=lambda x: x[1]['sales'], reverse=True):
            sales = data['sales']
            percent_total = (sales / total_revenue * 100)
            transactions_count = data['transactions']
            f.write(f"{region:<10} ₹{sales:,.2f}   {percent_total:.2f}%     {transactions_count:<12}\n")
        f.write("\n")
        # --- 4. TOP 5 PRODUCTS ---
        f.write("TOP 5 PRODUCTS\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Rank':<6} {'Product Name':<25} {'Quantity Sold':<15} {'Revenue':<15}\n")
        product_data = defaultdict(lambda: {'quantity': 0, 'revenue': 0})
        for trx in transactions:
            product_name = trx['ProductName']
            quantity = trx['Quantity']
            amount = trx['Quantity'] * trx['UnitPrice']
            product_data[product_name]['quantity'] += quantity
            product_data[product_name]['revenue'] += amount
        top_products = sorted(product_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        for rank, (product, data) in enumerate(top_products, start=1):
            f.write(f"{rank:<6} {product:<25} {data['quantity']:<15} ₹{data['revenue']:,.2f}\n")
        f.write("\n")
        # --- 5. TOP 5 CUSTOMERS ---
        f.write("TOP 5 CUSTOMERS\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Order Count':<12}\n")
        customer_data = defaultdict(lambda: {'total_spent': 0, 'order_count': 0})
        for trx in transactions:
            customer_id = trx['CustomerID']
            amount = trx['Quantity'] * trx['UnitPrice']
            customer_data[customer_id]['total_spent'] += amount
            customer_data[customer_id]['order_count'] += 1
        top_customers = sorted(customer_data.items(), key=lambda x: x[1]['total_spent'], reverse=True)[:5]
        for rank, (customer, data) in enumerate(top_customers, start=1):
            f.write(f"{rank:<6} {customer:<15} ₹{data['total_spent']:,.2f}   {data['order_count']:<12}\n")
        f.write("\n")
        # --- 6. DAILY SALES TREND ---
        f.write("DAILY SALES TREND\n")
        f.write("--------------------------------------------\n")
        f.write(f"{'Date':<12} {'Revenue':<15} {'Transactions':<15} {'Unique Customers':<18}\n")
        daily_data = defaultdict(lambda: {'revenue': 0, 'transactions': 0, 'unique_customers': set()})
        for trx in transactions:
            date = datetime.strptime(trx['Date'], "%Y-%m-%d").date()
            amount = trx['Quantity'] * trx['UnitPrice']
            daily_data[date]['revenue'] += amount
            daily_data[date]['transactions'] += 1
            daily_data[date]['unique_customers'].add(trx['CustomerID'])
        for date, data in sorted(daily_data.items()):
            f.write(f"{date:<12} ₹{data['revenue']:,.2f}   {data['transactions']:<15} {len(data['unique_customers']):<18}\n")
        f.write("\n")
        # --- 7. PRODUCT PERFORMANCE ANALYSIS ---
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("--------------------------------------------\n")
        # Best selling day
        best_selling_day = max(daily_data.items(), key=lambda x: x[1
]['revenue'])[0]
        best_selling_day_revenue = daily_data[best_selling_day]['revenue']
        # Low performing products
        low_performing_products = [product for product, data
                                    in product_data.items() if data['revenue'] < 1000]
        # Average transaction value per region
        avg_transaction_value_per_region = {}
        for region, data in region_data.items():
            avg_value = data['sales'] / data['transactions'] if data['transactions'] > 0 else 0
            avg_transaction_value_per_region[region] = avg_value
        f.write(f"Best Selling Day: {best_selling_day} with Revenue ₹{best_selling_day_revenue:,.2f}\n")
        f.write("Low Performing Products:\n")
        for product in low_performing_products:
            f.write(f"- {product}\n")
        f.write("\n")
        f.write("Average Transaction Value per Region:\n")
        for region, avg_value in avg_transaction_value_per_region.items():
            f.write(f"- {region}: ₹{avg_value:,.2f}\n")
        f.write("\n")
        # --- 8. API ENRICHMENT SUMMARY ---
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------\n")
        total_enriched = sum(1 for trx in enriched_transactions if trx.get("API_Match"))
        success_rate = (total_enriched / len(enriched_transactions) * 100) if enriched_transactions else 0
        unenriched_products = [trx['ProductID'] for trx in enriched_transactions if not trx.get("API_Match")]
        f.write(f"Total Products Enriched: {total_enriched}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Products that couldn't be enriched:\n")
        for product in unenriched_products:
            f.write(f"- {product}\n")
    print("Sales report generated at", output_file)
    return None
print(generate_sales_report(transactions, enriched_transactions))



# def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
#     with open(output_file, 'w', encoding='utf-8') as f:
#         # --- 1. HEADER ---
#         f.write("============================================\n")
#         f.write("       SALES ANALYTICS REPORT\n")
#         f.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
#         f.write(f"     Records Processed: {len(transactions)}\n")
#         f.write("============================================\n\n")

#         # --- 2. OVERALL SUMMARY ---
#         f.write("OVERALL SUMMARY\n")
#         f.write("--------------------------------------------\n")
#         total_revenue = sum(trx['Quantity'] * trx['UnitPrice'] for trx in transactions)
#         total_transactions = len(transactions)
#         avg_order_value = total_revenue / total_transactions
#         date_format = "%Y-%m-%d"
#         dates = [datetime.strptime(trx['Date'], date_format) for trx in transactions]
#         date_range = f"{min(dates).strftime(date_format)} to {max(dates).strftime(date_format)}"
#         f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
#         f.write(f"Total Transactions:   {total_transactions}\n")
#         f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
#         f.write(f"Date Range:           {date_range}\n\n")

#         # --- 3. REGION-WISE PERFORMANCE ---

#         f.write("REGION-WISE PERFORMANCE\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"{'Region':<10} {'Sales':<15} {'% of Total':<12} {'Transactions':<12}\n")

#         for region, data in sorted(region_data.items(), key=lambda x: x[1]['sales'], reverse=True):
#             sales = data['sales']
#             percent_total = (sales / total_revenue * 100) if total_revenue else 0
#             transactions_count = data['transactions']
#             f.write(f"{region:<10} ₹{sales:,.2f}   {percent_total:.2f}%     {transactions_count:<12}\n")
#         f.write("\n")
#         # --- 4. TOP 5 PRODUCTS ---
#         f.write("TOP 5 PRODUCTS\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"{'Rank':<6} {'Product Name':<25} {'Quantity Sold':<15} {'Revenue':<15}\n")
#         for rank, (product, data) in enumerate(top_products, start=1):
#             f.write(f"{rank:<6} {product:<25} {data['quantity']:<15} ₹{data['revenue']:,.2f}\n")
#         f.write("\n")
#         # --- 5. TOP 5 CUSTOMERS ---
#         f.write("TOP 5 CUSTOMERS\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<15} {'Order Count':<12}\n")
#         for rank, (customer, data) in enumerate(top_customers, start=1):
#             f.write(f"{rank:<6} {customer:<15} ₹{data['total_spent']:,.2f}   {data['order_count']:<12}\n")
#         f.write("\n")
#         # --- 6. DAILY SALES TREND ---
#         f.write("DAILY SALES TREND\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"{'Date':<12} {'Revenue':<15} {'Transactions':<15} {'Unique Customers':<18}\n")
#         for date, data in sorted(daily_trends.items()):
#             f.write(f"{date:<12} ₹{data['revenue']:,.2f}   {data['transactions']:<15} {data['unique_customers']:<18}\n")
#         f.write("\n")
#         # --- 7. PRODUCT PERFORMANCE ANALYSIS ---
#         f.write("PRODUCT PERFORMANCE ANALYSIS\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"Best Selling Day: {best_selling_day} with Revenue ₹{best_selling_day_revenue:,.2f}\n")
#         f.write("Low Performing Products:\n")
#         for product in low_performing_products:
#             f.write(f"- {product}\n")
#         f.write("\n")
#         f.write("Average Transaction Value per Region:\n")
#         for region, avg_value in avg_transaction_value_per_region.items():
#             f.write(f"- {region}: ₹{avg_value:,.2f}\n")
#         f.write("\n")
#         # --- 8. API ENRICHMENT SUMMARY ---
#         f.write("API ENRICHMENT SUMMARY\n")
#         f.write("--------------------------------------------\n")
#         f.write(f"Total Products Enriched: {total_enriched}\n")
#         f.write(f"Success Rate: {success_rate:.2f}%\n")
#         f.write("Products that couldn't be enriched:\n")
#         for product in unenriched_products:
#             f.write(f"- {product}\n")
#     print("Sales report generated at", output_file)
#     return None
# print(generate_sales_report(transactions, enriched_transactions))
# # def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt


    
    # # Generates a comprehensive formatted text report


    # Report Must Include (in this order):

    # 1. HEADER
    #    - Report title
    #    - Generation date and time
    #    - Total records processed

    # 2. OVERALL SUMMARY
    #    - Total Revenue (formatted with commas)
    #    - Total Transactions
    #    - Average Order Value
    #    - Date Range of data

    # 3. REGION-WISE PERFORMANCE
    #    - Table showing each region with:
    #      * Total Sales Amount
    #      * Percentage of Total
    #      * Transaction Count
    #    - Sorted by sales amount descending

    # 4. TOP 5 PRODUCTS
    #    - Table with columns: Rank, Product Name, Quantity Sold, Revenue

    # 5. TOP 5 CUSTOMERS
    #    - Table with columns: Rank, Customer ID, Total Spent, Order Count

    # 6. DAILY SALES TREND
    #    - Table showing: Date, Revenue, Transactions, Unique Customers

    # 7. PRODUCT PERFORMANCE ANALYSIS
    #    - Best selling day
    #    - Low performing products (if any)
    #    - Average transaction value per region

    # 8. API ENRICHMENT SUMMARY
    #    - Total products enriched
    #    - Success rate percentage
    #    - List of products that couldn't be enriched

    # Expected Output Format (sample):
    # ============================================
    #        SALES ANALYTICS REPORT
    #      Generated: 2024-12-18 14:30:22
    #      Records Processed: 95
    # ============================================

    # OVERALL SUMMARY
    # --------------------------------------------
    # Total Revenue:        ₹15,45,000.00
    # Total Transactions:   95
    # Average Order Value:  ₹16,263.16
    # Date Range:           2024-12-01 to 2024-12-31

    # REGION-WISE PERFORMANCE
    # --------------------------------------------
    # Region    Sales         % of Total  Transactions
    # North     ₹4,50,000     29.13%      25
    # South     ₹3,80,000     24.60%      22
    # ...

    # (continue with all sections...)
    # """

