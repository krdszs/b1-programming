expense_records = []
category_totals = {}
unique_categories = set()


num_expenses = int(input("How many expenses do your want to enter? "))
if num_expenses < 5 or num_expenses > 7:
    print("\nInvalid input. Enter a number between 5 and 7.")

else:
    print("=== PERSONAL EXPENSE TRACKER ===")
    for i in range(1, num_expenses + 1):
        category = str(input(f"\nEnter expense {i} category: "))
        amount = float(input(f"Enter expense {i} amount: $"))
        date = str(input(f"Enter expense {i} date (YYYY-MM-DD): "))
        
        details = (category, amount, date)
        expense_records.append(details)

    for date, amount, category  in expense_records:
        category_totals[category] = category_totals.get(category, 0) + amount
        unique_categories.add(category)
    
    all_amounts = [exp[1] for exp in expense_records]
    overall_stats = {}
    overall_stats["total_spent"] = sum(all_amounts)
    overall_stats["highest_exp"] = max(all_amounts)
    overall_stats["lowest_exp"] = min(all_amounts)
    overall_stats["avg_exp"] = overall_stats["total_spent"]/len(all_amounts)
    
    for date, amount, category in expense_records:
        if amount == overall_stats["highest_exp"]:      # Storing date and category of highest expense
            high_date = date
            high_category = category
        elif amount == overall_stats["lowest_exp"]:         # Storing date and category of lowest expense
            low_date = date
            low_category = category

    print("\n=== OVERALL SPENDING SUMMARY ===")
    print(f"Total Spending: ${overall_stats["total_spent"]:.2f}")
    print(f"Average Expense: ${overall_stats["avg_exp"]:.2f}")
    print(f"Highest Expense: ${overall_stats["highest_exp"]:.2f} (Category: {high_category}, Date: {high_date})")
    print(f"Lowest Expense: ${overall_stats["lowest_exp"]:.2f} (Category: {low_category}, Date: {low_date})")

    print("\n=== OVERALL SPENDING SUMMARY ===")
    print(unique_categories)
    print(f"Total unique categories: {len(unique_categories)}")

    print("\n=== OVERALL SPENDING SUMMARY ===")
    for category, amount in category_totals.items():
        print(f"{category}: ${amount:.2f}")
