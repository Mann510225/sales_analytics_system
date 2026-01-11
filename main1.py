
# FLOW: main execution function


def filter_data():
    print("Filtering data based on user input...")

def main():
    available_regions = ["North", "South", "East", "West"]
    transaction_amount_range = "₹1,000 – ₹5,00,000"
    
    for workflow_step in range(1, 13):
        try:
            # print welcom message
            print(f"[{workflow_step}/12] Executing step {workflow_step}...")
            if workflow_step == 1:
                print("WELCOME TO THE SALES ANALYTICS SYSTEM")
            # read sales data file
            elif workflow_step == 2:
                print("Reading sales data file...")
                # parse and clean transactions
            elif workflow_step == 3:
                print("Parsing and cleaning data...")
            # display filter options to user
            elif workflow_step == 4:
                print("Displaying filter options...")
                if available_regions:
                    print(f"Available regions: {', '.join(available_regions)}")
                if transaction_amount_range:
                    print(f"Transaction amount range: {transaction_amount_range}")
                user_input = input("Do you want to filter data? (y/n): ")
                if user_input.lower() == "y":
                    filter_data()
            # validate transactions
            elif workflow_step == 5:
                print("Validating transactions...")
            # display validation summary
            elif workflow_step == 6:
                print("Displaying validation summary...")
            # perform all data analyses
            elif workflow_step == 7:
                print("Performing data analyses...")
            # fetch products from API
            elif workflow_step == 8:
                print("Fetching products from API...")
            # enrich sales data with API info
            elif workflow_step == 9:
                print("Enriching sales data...")
            # save enriched data to file
            elif workflow_step == 10:
                print("Saving enriched data...")
            # generate comprehensive report
            elif workflow_step == 11:
                print("Generating report...")
            # print success message with file locations
            elif workflow_step == 12:
                print("Process complete!")
        except Exception as e:
            print(f"An error occurred at step {workflow_step}: {str(e)}")
            break
    print("========================================")
    

if __name__ == "__main__":
    main()





    # """
    # Main execution function

    # Workflow:
    # 1. Print welcome message
    # 2. Read sales data file (handle encoding)
    # 3. Parse and clean transactions
    # 4. Display filter options to user
    #    - Show available regions
    #    - Show transaction amount range
    #    - Ask if user wants to filter (y/n)
    # 5. If yes, ask for filter criteria and apply
    # 6. Validate transactions
    # 7. Display validation summary
    # 8. Perform all data analyses (call all functions from Part 2)
    # 9. Fetch products from API
    # 10. Enrich sales data with API info
    # 11. Save enriched data to file
    # 12. Generate comprehensive report
    # 13. Print success message with file locations

    # Error Handling:
    # - Wrap entire process in try-except
    # - Display user-friendly error messages
    # - Don't let program crash on errors

    # Expected Console Output:
    # ========================================
    # SALES ANALYTICS SYSTEM
    # ========================================

    # [1/10] Reading sales data...
    # ✓ Successfully read 95 transactions

    # [2/10] Parsing and cleaning data...
    # ✓ Parsed 95 records

    # [3/10] Filter Options Available:
    # Regions: North, South, East, West
    # Amount Range: ₹500 - ₹90,000

    # Do you want to filter data? (y/n): n

    # [4/10] Validating transactions...
    # ✓ Valid: 92 | Invalid: 3

    # [5/10] Analyzing sales data...
    # ✓ Analysis complete

    # [6/10] Fetching product data from API...
    # ✓ Fetched 30 products

    # [7/10] Enriching sales data...
    # ✓ Enriched 85/92 transactions (92.4%)

    # [8/10] Saving enriched data...
    # ✓ Saved to: data/enriched_sales_data.txt

    # [9/10] Generating report...
    # ✓ Report saved to: output/sales_report.txt

    # [10/10] Process Complete!
    # ========================================
    # """
