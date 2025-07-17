import pandas as pd

def analyze_churn_rate(df):
    latest = df["Transaction Date & Time"].max()
    last_visits = df.groupby("Customer ID")["Transaction Date & Time"].max()
    churned = (latest - last_visits).dt.days > 60
    churn_rate = churned.mean()
    print(f"\n Customer Churn Rate: {churn_rate:.2%}")
    pd.Series(churned).to_csv("churn_data.csv")

def recommend_service_packages(df):
    top_services = df["Service Type"].value_counts().head(3)
    print("\n Recommend Combo Offers Based On These Services:")
    print(top_services)
    top_services.to_csv("recommended_packages.csv")

def analyze_seasonality(df):
    seasonality = df.groupby("Month")["Amount Paid"].sum()
    print("\n Seasonality Trends:")
    print(seasonality)
    seasonality.to_csv("seasonality.csv")

def track_carbon_footprint(df):
    emission_factor = 0.05  # kg CO2 per transaction (example)
    df["CO2_Emitted"] = 1 * emission_factor
    footprint = df.groupby("Month")["CO2_Emitted"].sum()
    print("\n Monthly CO2 Emissions (kg):")
    print(footprint)
    footprint.to_csv("carbon_footprint.csv")

def identify_low_sales_month(df):
    monthly_sales = df.groupby("Month")["Amount Paid"].sum()
    low_month = monthly_sales.idxmin()
    print(f"\n Low Sales Month: {low_month} – ₹{monthly_sales[low_month]:,.2f}")
    monthly_sales.to_csv("monthly_sales.csv")

def rank_services(df):
    ranking = df.groupby("Service Type").agg(
        Usage_Count=("Transaction ID", "count"),
        Total_Revenue=("Amount Paid", "sum")
    ).sort_values("Total_Revenue", ascending=False)
    print("\n Service Rankings:")
    print(ranking)
    ranking.to_csv("service_ranking.csv")
