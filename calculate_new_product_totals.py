import json
import csv
from datetime import datetime

# Load the JSON data
with open('data/all_months_prod_list.json', 'r') as f:
    data = json.load(f)

# Load price data from the products CSV
price_lookup = {}
with open('data/shopify_products_cleaned_with_variant_ids.csv', 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        product_title = row['title']
        price = float(row['price'])
        # Use the first price we encounter for each product (they should all be the same)
        if product_title not in price_lookup:
            price_lookup[product_title] = price

# Define the new products with their release dates
new_products = [
    ("2024-01-01", "Wool Beanie"),
    ("2024-03-01", "Vintage Washed Tee"),
    ("2024-03-01", "Mini Sling Bag"),
    ("2024-03-01", "Unisex Thermal Long Sleeve Tee"),
    ("2024-05-10", "Minimalist Crewneck Sweatshirt"),
    ("2024-05-10", "Wide Leg Utility Pants"),
    ("2024-05-10", "Boxy Hoodie"),
    ("2024-05-10", "Graphic Print Tee"),
    ("2024-06-15", "Coach Jacket"),
    ("2024-06-15", "Relaxed Fit Cargo Shorts"),
    ("2024-06-15", "Loose Fit Tank Top"),
    ("2024-06-15", "5-Panel Street Cap"),
    ("2024-09-10", "Zip-Up Hoodie"),
    ("2024-09-10", "Slim Tapered Joggers"),
    ("2024-09-10", "Corduroy Bucket Hat"),
    ("2024-09-10", "Ribbed Crew Socks"),
    ("2024-11-20", "Quilted Bomber Jacket"),
    ("2024-11-20", "Streetwear Messenger Bag"),
    ("2024-11-20", "Patterned Dress Socks"),
    ("2025-02-10", "Thermal Hoodie")
]

# Calculate total sales for each product
results = []

for release_date, product_name in new_products:
    total_sold = 0
    
    # Go through each month in the data
    for month_data in data:
        month = month_data["month"]
        product_list = month_data["product_list"]
        
        # Find the product in this month's sales
        for product in product_list:
            if product["product_title"] == product_name:
                total_sold += product["quantity_sold"]
                break
    
    # Get the price for this product
    price = price_lookup.get(product_name, 0)
    
    results.append({
        "date_released": release_date,
        "product_name": product_name,
        "price": price,
        "total_sold_in_a_year": total_sold
    })

# Save to CSV
with open('new_product_totals.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['date_released', 'product_name', 'price', 'total_sold_in_a_year']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
    writer.writeheader()
    for result in results:
        writer.writerow(result)

print("Results saved to new_product_totals.csv")
print("\nSummary:")
for result in results:
    print(f"{result['product_name']}: ${result['price']:.2f} - {result['total_sold_in_a_year']} units sold") 