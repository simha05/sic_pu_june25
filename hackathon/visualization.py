import pandas as pd
import matplotlib.pyplot as plt
import os

class CarWashVisualizer:
    def plot_churn_rate(self):
        data = pd.read_csv("churn_data.csv", index_col=0).squeeze()
        counts = data.value_counts()
        counts.index = ["Active", "Churned"]
        counts.plot(kind="pie", autopct='%1.1f%%', title="Customer Churn Rate")
        plt.ylabel('')
        plt.tight_layout()
        plt.show()

    def plot_service_recommendations(self):
        data = pd.read_csv("recommended_packages.csv", index_col=0).squeeze()
        data.plot(kind="bar", color="skyblue", title="Top Recommended Services")
        plt.xlabel("Service Type")
        plt.ylabel("Count")
        plt.tight_layout()
        plt.show()

    def plot_seasonality(self):
        data = pd.read_csv("seasonality.csv", index_col=0).squeeze()
        data.plot(kind="line", marker='o', title="Seasonality Trends")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_carbon_footprint(self):
        data = pd.read_csv("carbon_footprint.csv", index_col=0).squeeze()
        data.plot(kind="bar", color="olive", title="Monthly CO2 Emissions")
        plt.xlabel("Month")
        plt.ylabel("CO2 (kg)")
        plt.tight_layout()
        plt.show()

    def plot_low_sales_month(self):
        data = pd.read_csv("monthly_sales.csv", index_col=0).squeeze()
        low = data.idxmin()
        colors = ['red' if m == low else 'lightgrey' for m in data.index]
        data.plot(kind="bar", color=colors, title="Monthly Sales (Lowest Highlighted)")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        plt.tight_layout()
        plt.show()

    def plot_service_ranking(self):
        df = pd.read_csv("service_ranking.csv", index_col=0)
        df["Total_Revenue"].plot(kind="barh", color="seagreen", title="Top Services by Revenue")
        plt.xlabel("Revenue")
        plt.tight_layout()
        plt.show()

        df["Usage_Count"].plot(kind="barh", color="dodgerblue", title="Top Services by Usage")
        plt.xlabel("Usage Count")
        plt.tight_layout()
        plt.show()

    def show_all_plots(self):
        print("\nGenerating all available plots...")
        if os.path.exists("churn_data.csv"):
            self.plot_churn_rate()
        if os.path.exists("recommended_packages.csv"):
            self.plot_service_recommendations()
        if os.path.exists("seasonality.csv"):
            self.plot_seasonality()
        if os.path.exists("carbon_footprint.csv"):
            self.plot_carbon_footprint()
        if os.path.exists("monthly_sales.csv"):
            self.plot_low_sales_month()
        if os.path.exists("service_ranking.csv"):
            self.plot_service_ranking()
