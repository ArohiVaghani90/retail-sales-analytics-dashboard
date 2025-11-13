import pandas as pd


df = pd.read_csv("supermarket_sales.csv")


print(" Data loaded successfully!\n")
print(df.head())


print("\nBasic Stats:")
print(df.describe())

import seaborn as sns
import matplotlib.pyplot as plt

sns.barplot(x="Branch", y="Total", data=df, estimator=sum)
plt.title("Total Sales by Branch")
plt.show()



df = pd.read_csv("supermarket_sales.csv")


print("Data overview:\n")
print(df.info())


print("\n Missing values:\n", df.isnull().sum())


df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

print("\nCleaned Data Preview:\n", df.head())



total_revenue = df['Total'].sum()


avg_rating = df['Rating'].mean()


top_branch = df.groupby('Branch')['Total'].sum().idxmax()


top_product_line = df.groupby('Product line')['Total'].sum().idxmax()

print("\n Key Insights:")
print(f" Total Revenue: ${total_revenue:,.2f}")
print(f" Average Rating: {avg_rating:.2f}")
print(f" Top Branch: {top_branch}")
print(f" Best-Selling Product Line: {top_product_line}")

import matplotlib.pyplot as plt
import seaborn as sns




plt.figure(figsize=(6,4))
sns.barplot(x='Branch', y='Total', data=df, estimator=sum, palette='viridis')
plt.title('Total Sales by Branch')
plt.show()


plt.figure(figsize=(8,5))
sns.barplot(x='Product line', y='Total', data=df, estimator=sum, palette='coolwarm')
plt.title('Sales by Product Line')
plt.xticks(rotation=45)
plt.show()


plt.figure(figsize=(6,4))
sns.barplot(x='Branch', y='Rating', data=df, estimator='mean', palette='magma')
plt.title('Average Rating by Branch')
plt.show()

print("\n ANALYSIS COMPLETE!")
print("You just performed data cleaning, summarization, and visualization on retail sales data.")



from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///retail_data.db', echo=False)


df.to_sql('sales', con=engine, index=False, if_exists='replace')
print("\n💾 Saved dataframe to SQLite: retail_data.db (table: sales)")


with engine.connect() as conn:
   
    q1 = text("""
        SELECT Branch, ROUND(SUM(Total), 2) AS total_revenue
        FROM sales
        GROUP BY Branch
        ORDER BY total_revenue DESC;
    """)
    print("\n🏪 Total revenue by branch:")
    print(pd.read_sql(q1, conn))

    
    q2 = text("""
        SELECT [Product line] AS product_line, ROUND(SUM(Total), 2) AS revenue
        FROM sales
        GROUP BY [Product line]
        ORDER BY revenue DESC;
    """)
    print("\n🔥 Best-selling product lines:")
    print(pd.read_sql(q2, conn))

   
    q3 = text("""
        SELECT strftime('%Y-%m', DATE(Date)) AS year_month, ROUND(SUM(Total), 2) AS revenue
        FROM sales
        GROUP BY year_month
        ORDER BY year_month;
    """)
    print("\n📆 Monthly revenue trend:")
    print(pd.read_sql(q3, conn))

    
    q4 = text("""
        SELECT Branch, ROUND(AVG(Rating), 2) AS avg_rating
        FROM sales
        GROUP BY Branch
        ORDER BY avg_rating DESC;
    """)
    print("\n⭐ Average rating by branch:")
    print(pd.read_sql(q4, conn))
