import pandas as pd
import matplotlib.pyplot as plt

# Load raw data
df = pd.read_csv("orders_raw.csv", low_memory=False)

print("Original shape:", df.shape)

# -----------------------------
# CLEANING IMPORTANT COLUMNS
# -----------------------------

# Extract amount
df['amount'] = pd.to_numeric(df['amount'], errors='coerce')

# Convert date (timestamp to readable)
df['date'] = pd.to_datetime(df['date'], unit='ms', errors='coerce')

# Extract month
df['month'] = df['date'].dt.month

# Keep only useful columns
clean_df = df[['amount', 'date', 'month']].dropna()

print("\nCleaned Data:")
print(clean_df.head())

# Save clean data
clean_df.to_csv("orders_clean.csv", index=False)

print("\n✅ Clean data saved!")

# -----------------------------
# ANALYSIS
# -----------------------------

# Monthly sales
monthly_sales = clean_df.groupby('month')['amount'].sum()

print("\nMonthly Sales:")
print(monthly_sales)

# -----------------------------
# VISUALIZATION
# -----------------------------

monthly_sales.plot(kind='bar')
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.show()

# -----------------------------
# TOP PRODUCTS ANALYSIS
# -----------------------------

import ast

product_list = []

# Loop through items column (if exists)
if 'items' in df.columns:
    for item in df['items'].dropna():
        try:
            # Convert string to list
            parsed = ast.literal_eval(item)

            for p in parsed:
                # Adjust key based on your structure
                if isinstance(p, dict) and 'name' in p:
                    product_list.append(p['name'])

        except:
            continue

# Count top products
if product_list:
    product_series = pd.Series(product_list)
    top_products = product_series.value_counts().head(5)

    print("\nTop Products:")
    print(top_products)

    # Plot
    top_products.plot(kind='bar')
    plt.title("Top 5 Products")
    plt.xlabel("Product")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
else:
    print("\n⚠️ No product data extracted (structure may differ)")