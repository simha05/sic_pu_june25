import pandas as pd
from analysis import (
    analyze_churn_rate,
    recommend_service_packages,
    analyze_seasonality,
    track_carbon_footprint,
    identify_low_sales_month,
    rank_services
)
from visualization import (
    plot_churn_rate,
    plot_service_recommendations,
    plot_seasonality,
    plot_carbon_footprint,
    plot_low_sales_month,
    plot_service_ranking
)

# Updated file path
DATA_PATH = r"C:\LEARNING\sic_pu_june25\hackathon\car_wash data set\car_wash_final_dataset_with_date (1).csv"

def preprocess_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Transaction Date & Time"])
    df['Month'] = df['Transaction Date & Time'].dt.month
    df['DayOfWeek'] = df['Transaction Date & Time'].dt.day_name()
    df['Hour'] = df['Transaction Date & Time'].dt.hour
    df['Time Slot'] = df['Hour'].apply(
        lambda h: "Night" if h < 6 else "Morning" if h < 12 else "Afternoon" if h < 18 else "Evening"
    )
    df.to_csv(DATA_PATH, index=False)
    return df

def main():
    print(" Preprocessing data...")
    df = preprocess_data()

    print(" Running analysis...")
    analyze_churn_rate(df)
    recommend_service_packages(df)
    analyze_seasonality(df)
    track_carbon_footprint(df)
    identify_low_sales_month(df)
    rank_services(df)

    print(" Generating visualizations...")
    plot_churn_rate()
    plot_service_recommendations()
    plot_seasonality()
    plot_carbon_footprint()
    plot_low_sales_month()
    plot_service_ranking()

    print(" All tasks completed.")

if __name__ == "__main__":
    main()
