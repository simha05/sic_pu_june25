import pandas as pd

class CarWashAnalyzer:
    def __init__(self, df):
        self.df = df

    def analyze_churn_rate(self):
        latest = self.df["Transaction Date & Time"].max()
        last_visits = self.df.groupby("Customer ID")["Transaction Date & Time"].max()
        churned = (latest - last_visits).dt.days > 60
        churn_rate = churned.mean()
        print(f"\nCustomer Churn Rate: {churn_rate:.2%}")
        churned.name = 'Churned'
        churned.to_csv("churn_data.csv")

    def recommend_service_packages(self):
        top_services = self.df["Service Type"].value_counts().head(3)
        print("\nRecommended Service Combos:")
        print(top_services)
        top_services.to_csv("recommended_packages.csv", header=["Count"])

    def analyze_seasonality(self):
        seasonality = self.df.groupby("Month")["Amount Paid"].sum()
        print("\nSeasonality Trends (Revenue by Month):")
        print(seasonality)
        seasonality.to_csv("seasonality.csv", header=["Revenue"])

    def track_carbon_footprint(self):
        emission_factor = 0.05  # kg CO2 per transaction
        self.df["CO2_Emitted"] = emission_factor
        footprint = self.df.groupby("Month")["CO2_Emitted"].sum()
        print("\nMonthly CO2 Emissions (kg):")
        print(footprint)
        footprint.to_csv("carbon_footprint.csv", header=["CO2_Emitted"])

    def identify_low_sales_month(self):
        monthly_sales = self.df.groupby("Month")["Amount Paid"].sum()
        low_month = monthly_sales.idxmin()
        print(f"\nLowest Sales Month: {low_month} – ₹{monthly_sales[low_month]:,.2f}")
        monthly_sales.to_csv("monthly_sales.csv", header=["Revenue"])

    def rank_services(self):
        ranking = self.df.groupby("Service Type").agg(
            Usage_Count=("Transaction ID", "count"),
            Total_Revenue=("Amount Paid", "sum")
        ).sort_values("Total_Revenue", ascending=False)
        print("\nService Ranking by Revenue and Usage:")
        print(ranking)
        ranking.to_csv("service_ranking.csv")
