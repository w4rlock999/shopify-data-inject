#!/usr/bin/env python3

import pandas as pd
from datetime import datetime

def analyze_product_releases_detailed(csv_file_path):
    """
    Analyze which specific products were released each month.
    
    Args:
        csv_file_path (str): Path to the CSV file containing product data
        
    Returns:
        DataFrame: Detailed breakdown of products by month
    """
    
    # Read the CSV file
    print(f"Reading data from {csv_file_path}...")
    df = pd.read_csv(csv_file_path)
    
    # Convert release_date to datetime
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    # Get unique products per release date (to avoid counting variants multiple times)
    unique_products = df.drop_duplicates(subset=['title', 'release_date'])
    
    # Extract year-month from release date
    unique_products['release_month'] = unique_products['release_date'].dt.to_period('M')
    
    # Sort by release date for chronological order
    unique_products = unique_products.sort_values('release_date')
    
    return unique_products[['release_month', 'title', 'product_type', 'release_date']]

def create_detailed_report(product_details):
    """
    Create a detailed report showing which products were released each month.
    
    Args:
        product_details (DataFrame): Product details by month
    """
    print("\n" + "="*80)
    print("DETAILED PRODUCT RELEASES BY MONTH")
    print("="*80)
    
    # Group by month and display products
    for month in product_details['release_month'].unique():
        month_products = product_details[product_details['release_month'] == month]
        
        print(f"\n📅 {month} ({len(month_products)} products)")
        print("-" * 50)
        
        for idx, product in month_products.iterrows():
            print(f"  • {product['title']} ({product['product_type']}) - Released: {product['release_date'].strftime('%Y-%m-%d')}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL: {len(product_details)} unique products released")

def save_detailed_csv(product_details, output_file):
    """
    Save detailed product release information to CSV.
    
    Args:
        product_details (DataFrame): Product details by month
        output_file (str): Output file name
    """
    # Create a more detailed output
    output_df = product_details.copy()
    output_df['release_month'] = output_df['release_month'].astype(str)
    output_df['release_date'] = output_df['release_date'].dt.strftime('%Y-%m-%d')
    
    # Reorder columns for better readability
    output_df = output_df[['release_month', 'release_date', 'title', 'product_type']]
    
    output_df.to_csv(output_file, index=False)
    print(f"\nDetailed results saved to: {output_file}")

def create_monthly_summary(product_details):
    """
    Create a summary table by month with product lists.
    
    Args:
        product_details (DataFrame): Product details by month
        
    Returns:
        DataFrame: Monthly summary with product lists
    """
    monthly_summary = product_details.groupby('release_month').agg({
        'title': lambda x: ', '.join(x.tolist()),
        'release_date': 'first'
    }).reset_index()
    
    monthly_summary['product_count'] = product_details.groupby('release_month').size().values
    monthly_summary['release_month'] = monthly_summary['release_month'].astype(str)
    monthly_summary['release_date'] = monthly_summary['release_date'].dt.strftime('%Y-%m-%d')
    
    # Reorder columns
    monthly_summary = monthly_summary[['release_month', 'product_count', 'title', 'release_date']]
    monthly_summary.columns = ['Month', 'Product_Count', 'Products_Released', 'First_Release_Date']
    
    return monthly_summary

def main():
    """
    Main function to run the detailed product release analysis.
    """
    # Define the CSV file path
    csv_file = 'data/shopify_products_cleaned.csv'
    
    try:
        # Analyze the data
        product_details = analyze_product_releases_detailed(csv_file)
        
        # Print detailed report
        create_detailed_report(product_details)
        
        # Save detailed results to CSV
        detailed_output_file = 'detailed_product_releases_by_month.csv'
        save_detailed_csv(product_details, detailed_output_file)
        
        # Create and save monthly summary
        monthly_summary = create_monthly_summary(product_details)
        summary_output_file = 'monthly_product_summary.csv'
        monthly_summary.to_csv(summary_output_file, index=False)
        print(f"Monthly summary saved to: {summary_output_file}")
        
        # Display the summary table
        print(f"\n{'='*80}")
        print("MONTHLY SUMMARY TABLE")
        print("="*80)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', 60)
        print(monthly_summary.to_string(index=False))
        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{csv_file}'. Please make sure it exists in the correct location.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 