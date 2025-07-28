#!/usr/bin/env python3

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_product_releases(csv_file_path):
    """
    Analyze product releases by month from CSV data.
    
    Args:
        csv_file_path (str): Path to the CSV file containing product data
        
    Returns:
        dict: Dictionary with monthly release counts
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
    
    # Count products released per month
    monthly_releases = unique_products.groupby('release_month').size().reset_index(name='new_products_count')
    
    # Convert period back to string for better readability
    monthly_releases['release_month'] = monthly_releases['release_month'].astype(str)
    
    return monthly_releases, unique_products

def create_visualization(monthly_releases):
    """
    Create a bar chart visualization of monthly product releases.
    
    Args:
        monthly_releases (DataFrame): Monthly release data
    """
    plt.figure(figsize=(12, 6))
    
    # Create bar plot
    bars = plt.bar(monthly_releases['release_month'], monthly_releases['new_products_count'], 
                   color='skyblue', edgecolor='navy', alpha=0.7)
    
    # Customize the plot
    plt.title('New Products Released Per Month', fontsize=16, fontweight='bold', pad=20)
    plt.xlabel('Month', fontsize=12, fontweight='bold')
    plt.ylabel('Number of New Products', fontsize=12, fontweight='bold')
    plt.xticks(rotation=45)
    plt.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('product_releases_by_month.png', dpi=300, bbox_inches='tight')
    plt.show()

def print_detailed_report(monthly_releases, unique_products):
    """
    Print a detailed report of product releases.
    
    Args:
        monthly_releases (DataFrame): Monthly release data
        unique_products (DataFrame): Unique products data
    """
    print("\n" + "="*60)
    print("NEW PRODUCTS RELEASED PER MONTH - DETAILED REPORT")
    print("="*60)
    
    total_products = len(unique_products)
    print(f"\nTotal unique products in dataset: {total_products}")
    print(f"Date range: {unique_products['release_date'].min().strftime('%Y-%m-%d')} to {unique_products['release_date'].max().strftime('%Y-%m-%d')}")
    
    print(f"\n{'Month':<15} {'New Products':<15} {'Product Names'}")
    print("-" * 80)
    
    for _, row in monthly_releases.iterrows():
        month = row['release_month']
        count = row['new_products_count']
        
        # Get product names for this month
        month_products = unique_products[unique_products['release_month'].astype(str) == month]['title'].tolist()
        product_names = ', '.join(month_products)
        
        print(f"{month:<15} {count:<15} {product_names}")
    
    # Summary statistics
    print(f"\n{'SUMMARY STATISTICS'}")
    print("-" * 30)
    print(f"Average products per month: {monthly_releases['new_products_count'].mean():.1f}")
    print(f"Peak month: {monthly_releases.loc[monthly_releases['new_products_count'].idxmax(), 'release_month']} ({monthly_releases['new_products_count'].max()} products)")
    print(f"Lowest month: {monthly_releases.loc[monthly_releases['new_products_count'].idxmin(), 'release_month']} ({monthly_releases['new_products_count'].min()} products)")

def main():
    """
    Main function to run the product release analysis.
    """
    # Define the CSV file path
    csv_file = 'data/shopify_products_cleaned.csv'
    
    try:
        # Analyze the data
        monthly_releases, unique_products = analyze_product_releases(csv_file)
        
        # Print detailed report
        print_detailed_report(monthly_releases, unique_products)
        
        # Create visualization
        print(f"\nCreating visualization...")
        create_visualization(monthly_releases)
        
        # Save results to CSV
        output_file = 'monthly_product_releases.csv'
        monthly_releases.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find the file '{csv_file}'. Please make sure it exists in the correct location.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 