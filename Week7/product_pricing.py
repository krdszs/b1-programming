import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_discount(category, tier):
    category_discounts = {
        "Electronics": 10,
        "Clothing": 15,
        "Books": 5,
        "Home": 12
    }
    tier_discounts = {
        "Premium": 5,
        "Standard": 0,
        "Budget": 2
    }

    category_discount = category_discounts.get(category, 0)
    tier_discount = tier_discounts.get(tier, 0)

    return category_discount + tier_discount

try:
    products = []
    total_discount = 0

    with open("products.txt") as sourcefile:
        for line_num, line in enumerate(sourcefile, 1):
            try:
                parts = line.strip().split(',')
                if len(parts) != 4:
                    logging.warning(f"Line {line_num}: Invalid format, skipping")
                    continue

                name, str_price, category, tier = parts
                base_price = float(str_price)

                discount_pct = calculate_discount(category, tier)
                discount_amt = base_price * (discount_pct / 100)
                final_price = base_price - discount_amt

                products.append({
                    'name': name,
                    'base_price': base_price,
                    'discount_pct': discount_pct,
                    'discount_amt': discount_amt,
                    'final_price': final_price
                })
                total_discount += discount_pct

            except ValueError as e:
                logging.error(f"Line {line_num}: Invalid price format - {e}")
                continue

    with open("pricing_report.txt", "w") as outfile:
        outfile.write("=" * 90 + "\n")
        outfile.write("PRICING REPORT\n")
        outfile.write("=" * 90 + "\n")
        outfile.write(f"{'Product Name':<30} {'Base Price':>12} {'Discount %':>12} {'Discount $':>12} {'Final Price':>12}\n")
        outfile.write("-" * 90 + "\n")

        for product in products:
            outfile.write(f"{product['name']:<30} "
            f"${product['base_price']:>11.2f} "
            f"{product['discount_pct']:>11.1f}% "
            f"${product['discount_amt']:>11.2f} "
            f"${product['final_price']:>11.2f}\n")

        outfile.write("=" * 90 + "\n")

    avg_discount = total_discount / len(products) if products else 0
    print("\nProcessing Complete!")
    print(f"Total products processed: {len(products)}")
    print(f"Average discount applied: {avg_discount:.2f}%")
    print(f"Report saved to: 'pricing_report.txt'")

    logging.info(f"Successfully processed {len(products)} products")

except FileNotFoundError:
    logging.error(f"Input file 'products.txt' not found")
    print(f"Error: Could not find 'products.txt'")

except PermissionError:
    logging.error(f"Permission denied writing to 'pricing_report.txt'")
    print(f"Error: Cannot write to 'pricing_report.txt'")
    
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    print(f"Error: {e}")