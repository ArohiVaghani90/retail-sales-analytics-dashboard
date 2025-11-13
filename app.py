
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

@st.cache_data
def load_data():
    
    csv_path = Path("supermarket_sales.csv")
    if csv_path.exists():
        df = pd.read_csv(csv_path)
    else:
        eng = create_engine("sqlite:///retail_data.db")
        df = pd.read_sql("SELECT * FROM sales", eng)


    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    # Safety: if Total is str, coerce to float
    df["Total"] = pd.to_numeric(df["Total"], errors="coerce")
    return df.dropna(subset=["Date", "Total"])

df = load_data()


st.sidebar.header("Filters")
branches = st.sidebar.multiselect(
    "Branch", sorted(df["Branch"].dropna().unique()),
    default=sorted(df["Branch"].dropna().unique())
)
products = st.sidebar.multiselect(
    "Product line", sorted(df["Product line"].dropna().unique()),
    default=sorted(df["Product line"].dropna().unique())
)
min_date, max_date = df["Date"].min(), df["Date"].max()
date_range = st.sidebar.date_input(
    "Date range", (min_date, max_date), min_value=min_date, max_value=max_date
)

mask = (
    df["Branch"].isin(branches)
    & df["Product line"].isin(products)
    & (df["Date"].between(pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])))
)
filtered = df.loc[mask].copy()


total_revenue = float(filtered["Total"].sum())
avg_rating = float(filtered["Rating"].mean()) if "Rating" in filtered else np.nan
orders = int(len(filtered))

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Average Rating", f"{avg_rating:.2f}" if not np.isnan(avg_rating) else "—")
col3.metric("Orders", f"{orders:,}")

st.markdown("---")


st.subheader("Revenue by Branch")
fig1, ax1 = plt.subplots(figsize=(5,3))
(filtered.groupby("Branch")["Total"].sum()
         .reindex(sorted(filtered["Branch"].unique()))
         .plot(kind="bar", ax=ax1))
ax1.set_xlabel("Branch")
ax1.set_ylabel("Revenue")
st.pyplot(fig1)

st.subheader("Revenue by Product Line")
fig2, ax2 = plt.subplots(figsize=(6,3))
(filtered.groupby("Product line")["Total"].sum()
         .sort_values(ascending=False)
         .plot(kind="bar", ax=ax2))
ax2.set_xlabel("Product line")
ax2.set_ylabel("Revenue")
plt.setp(ax2.get_xticklabels(), rotation=30, ha="right")
st.pyplot(fig2)

st.subheader("Revenue Trend")
by_day = filtered.set_index("Date").resample("D")["Total"].sum()
fig3, ax3 = plt.subplots(figsize=(6,3))
by_day.plot(ax=ax3)
ax3.set_xlabel("Date")
ax3.set_ylabel("Revenue (per day)")
st.pyplot(fig3)

st.markdown("### Filtered Rows")
st.dataframe(filtered.head(100), use_container_width=True)

st.download_button(
    "Download filtered CSV",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales.csv",
    mime="text/csv",
)
import numpy as np
from datetime import timedelta

def daily_revenue(df_in):
    s = (df_in
         .dropna(subset=["Date", "Total"])
         .set_index("Date")
         .resample("D")["Total"]
         .sum()
         .asfreq("D")
         .fillna(0.0))
    return s

def moving_avg_forecast(series, days_ahead=14, window=3):
    
    s = series.copy()
    if len(s) == 0:
        return series, series, pd.Series([], dtype=float)

    smooth = s.rolling(window=window, min_periods=1).mean()

    
    x = np.arange(len(smooth))
    y = smooth.values
    a, b = np.polyfit(x, y, 1)  

 
    future_x = np.arange(len(smooth), len(smooth) + days_ahead)
    future_vals = a * future_x + b

    future_index = pd.date_range(s.index[-1] + timedelta(days=1), periods=days_ahead, freq="D")
    forecast = pd.Series(future_vals, index=future_index, name="forecast")

    return s, smooth, forecast
