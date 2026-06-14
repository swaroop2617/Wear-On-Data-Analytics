import pandas as pd
import matplotlib.pyplot as plt
import ast
import os

# Create charts folder
if not os.path.exists("charts"):
    os.makedirs("charts")

# Load data
df = pd.read_csv("orders_raw.csv", low_memory=False)

print("Original shape:", df.shape)

# -----------------------------
# CLEANING
# -----------------------------

df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
df['date'] = pd.to_datetime(df['date'], unit='ms', errors='coerce')

clean_df = df[['amount', 'date']].dropna()
clean_df['month'] = clean_df['date'].dt.month

print("\nCleaned Data:")
print(clean_df.head())

clean_df.to_csv("orders_clean.csv", index=False)

# -----------------------------
# MONTHLY SALES
# -----------------------------

monthly_sales = clean_df.groupby('month')['amount'].sum()

print("\nMonthly Sales:")
print(monthly_sales)

plt.figure()
monthly_sales.plot(kind='bar')
plt.title("Monthly Sales")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.tight_layout()
plt.tight_layout()
plt.savefig("charts/monthly_sales.png")
plt.close()

# -----------------------------
# DAILY SALES TREND
# -----------------------------

daily_sales = clean_df.groupby(clean_df['date'].dt.date)['amount'].sum()

plt.figure()
daily_sales.plot(kind='line')
plt.title("Daily Sales Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/daily_sales.png")
plt.show()

# -----------------------------
# PAYMENT METHOD ANALYSIS
# -----------------------------

if 'paymentMethod' in df.columns:
    payment_counts = df['paymentMethod'].value_counts()

    print("\nPayment Method Distribution:")
    print(payment_counts)

    plt.figure()
    payment_counts.plot(kind='pie', autopct='%1.1f%%')
    plt.title("Payment Method Distribution")
    plt.ylabel("")
    plt.savefig("charts/payment_methods.png")
    plt.show()

# -----------------------------
# ORDER STATUS ANALYSIS
# -----------------------------

if 'status' in df.columns:
    status_counts = df['status'].value_counts()

    print("\nOrder Status Distribution:")
    print(status_counts)

    plt.figure()
    status_counts.plot(kind='bar')
    plt.title("Order Status Distribution")
    plt.xlabel("Status")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("charts/order_status.png")
    plt.show()

# -----------------------------
# AVERAGE ORDER VALUE
# -----------------------------

avg_order_value = clean_df['amount'].mean()
print("\nAverage Order Value:", avg_order_value)

# -----------------------------
# TOP PRODUCTS
# -----------------------------

product_list = []

if 'items' in df.columns:
    for item in df['items'].dropna():
        try:
            parsed = ast.literal_eval(item)
            for p in parsed:
                if isinstance(p, dict) and 'name' in p:
                    product_list.append(p['name'])
        except:
            continue

if product_list:
    product_series = pd.Series(product_list)
    top_products = product_series.value_counts().head(5)

    print("\nTop Products:")
    print(top_products)

    plt.figure()
    top_products.plot(kind='bar')
    plt.title("Top 5 Products")
    plt.xlabel("Product")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("charts/top_products.png")
    plt.show()
else:
    print("\nNo product data extracted")

# -----------------------------
# KEY BUSINESS METRICS
# -----------------------------

total_revenue = clean_df['amount'].sum()
total_orders = len(clean_df)
avg_order_value = clean_df['amount'].mean()

print("\nKey Metrics:")
print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Average Order Value:", avg_order_value)
