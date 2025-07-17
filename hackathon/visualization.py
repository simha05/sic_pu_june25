import pandas as pd
import matplotlib.pyplot as plt

def plot_churn_rate():
    churned = pd.read_csv("churn_data.csv", index_col=0).squeeze()
    churn_counts = churned.value_counts()
    churn_counts.index = ["Active", "Churned"]
    churn_counts.plot(kind='pie', autopct='%1.1f%%', title="Customer Churn Rate")
    plt.ylabel('')
    plt.tight_layout()
    plt.show()

def plot_service_recommendations():
    services = pd.read_csv("recommended_packages.csv", index_col=0).squeeze()
    services.plot(kind='bar', color='skyblue', title="Top Recommended Services")
    plt.xlabel("Service Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.show()

def plot_seasonality():
    seasonality = pd.read_csv("seasonality.csv", index_col=0).squeeze()
    seasonality.plot(kind='line', marker='o', title="Seasonality Trends")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_carbon_footprint():
    footprint = pd.read_csv("carbon_footprint.csv", index_col=0).squeeze()
    footprint.plot(kind='bar', color='olive', title="Monthly Carbon Footprint (kg CO2)")
    plt.xlabel("Month")
    plt.ylabel("CO2 Emissions (kg)")
    plt.tight_layout()
    plt.show()

def plot_low_sales_month():
    sales = pd.read_csv("monthly_sales.csv", index_col=0).squeeze()
    low = sales.idxmin()
    colors = ['red' if m == low else 'lightgrey' for m in sales.index]
    sales.plot(kind='bar', color=colors, title="Low-Sales Month Highlighted")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.tight_layout()
    plt.show()

def plot_service_ranking():
    ranking = pd.read_csv("service_ranking.csv", index_col=0)
    ranking["Total_Revenue"].plot(kind='barh', color='seagreen', title="Top Services by Revenue")
    plt.xlabel("Revenue")
    plt.tight_layout()
    plt.show()

    ranking["Usage_Count"].plot(kind='barh', color='dodgerblue', title="Top Services by Usage Count")
    plt.xlabel("Usage Count")
    plt.tight_layout()
    plt.show()
