import pandas as pd

# Load dataset
df = pd.read_csv("supermarket_sales.csv")

# Show first few rows
print(" Data loaded successfully!\n")
print(df.head())

# Quick summary
print("\nBasic Stats:")
print(df.describe())

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(x="Branch", y="Total", data=df, estimator=sum)
plt.title("Total Sales by Branch")
plt.show()
# --- STEP 1: DATA CLEANING ---

# Load data
df = pd.read_csv("supermarket_sales.csv")

# Check info
print("Data overview:\n")
print(df.info())

# Check for missing values
print("\n Missing values:\n", df.isnull().sum())

# Convert date column to datetime type
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

# Check the first few cleaned rows
print("\nCleaned Data Preview:\n", df.head())
# --- STEP 2: SUMMARY STATS AND INSIGHTS ---

# 1. Total revenue
total_revenue = df['Total'].sum()

# 2. Average customer rating
avg_rating = df['Rating'].mean()

# 3. Top-selling branch
top_branch = df.groupby('Branch')['Total'].sum().idxmax()

# 4. Top product line by sales
top_product_line = df.groupby('Product line')['Total'].sum().idxmax()

print("\n Key Insights:")
print(f" Total Revenue: ${total_revenue:,.2f}")
print(f" Average Rating: {avg_rating:.2f}")
print(f" Top Branch: {top_branch}")
print(f" Best-Selling Product Line: {top_product_line}")

import matplotlib.pyplot as plt
import seaborn as sns



# Sales by Branch
plt.figure(figsize=(6,4))
sns.barplot(x='Branch', y='Total', data=df, estimator=sum, palette='viridis')
plt.title('Total Sales by Branch')
plt.show()

# Sales by Product Line
plt.figure(figsize=(8,5))
sns.barplot(x='Product line', y='Total', data=df, estimator=sum, palette='coolwarm')
plt.title('Sales by Product Line')
plt.xticks(rotation=45)
plt.show()

# Average Rating per Branch
plt.figure(figsize=(6,4))
sns.barplot(x='Branch', y='Rating', data=df, estimator='mean', palette='magma')
plt.title('Average Rating by Branch')
plt.show()

print("\n ANALYSIS COMPLETE!")
print("You just performed data cleaning, summarization, and visualization on retail sales data.")

# --- STEP 4: SAVE TO SQLITE + RUN SQL QUERIES ---

from sqlalchemy import create_engine, text

# Create (or open) a local SQLite database file
engine = create_engine('sqlite:///retail_data.db', echo=False)

# Save dataframe as a table named "sales"
df.to_sql('sales', con=engine, index=False, if_exists='replace')
print("\n💾 Saved dataframe to SQLite: retail_data.db (table: sales)")

# Run example SQL queries
with engine.connect() as conn:
    # 1️⃣ Total revenue by branch
    q1 = text("""
        SELECT Branch, ROUND(SUM(Total), 2) AS total_revenue
        FROM sales
        GROUP BY Branch
        ORDER BY total_revenue DESC;
    """)
    print("\n🏪 Total revenue by branch:")
    print(pd.read_sql(q1, conn))

    # 2️⃣ Best-selling product line
    q2 = text("""
        SELECT [Product line] AS product_line, ROUND(SUM(Total), 2) AS revenue
        FROM sales
        GROUP BY [Product line]
        ORDER BY revenue DESC;
    """)
    print("\n🔥 Best-selling product lines:")
    print(pd.read_sql(q2, conn))

    # 3️⃣ Monthly revenue trend
    q3 = text("""
        SELECT strftime('%Y-%m', DATE(Date)) AS year_month, ROUND(SUM(Total), 2) AS revenue
        FROM sales
        GROUP BY year_month
        ORDER BY year_month;
    """)
    print("\n📆 Monthly revenue trend:")
    print(pd.read_sql(q3, conn))

    # 4️⃣ Average rating per branch
    q4 = text("""
        SELECT Branch, ROUND(AVG(Rating), 2) AS avg_rating
        FROM sales
        GROUP BY Branch
        ORDER BY avg_rating DESC;
    """)
    print("\n⭐ Average rating by branch:")
    print(pd.read_sql(q4, conn))
