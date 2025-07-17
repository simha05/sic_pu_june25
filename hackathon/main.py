import pandas as pd
from analysis import CarWashAnalyzer
from visualization import CarWashVisualizer

# Dataset path
DATA_PATH = r"C:\LEARNING\sic_pu_june25\hackathon\car_wash data set\car_wash_final_dataset_with_date (1).csv"

class CarWashApp:
    def __init__(self):
        self.df = None
        self.analyzer = None
        self.visualizer = CarWashVisualizer()

    def preprocess_data(self):
        print("\nPreprocessing data...")
        self.df = pd.read_csv(DATA_PATH, parse_dates=["Transaction Date & Time"])
        self.df['Month'] = self.df['Transaction Date & Time'].dt.month_name()
        self.df['DayOfWeek'] = self.df['Transaction Date & Time'].dt.day_name()
        self.df['Hour'] = self.df['Transaction Date & Time'].dt.hour
        self.df['Time Slot'] = self.df['Hour'].apply(
            lambda h: "Night" if h < 6 else "Morning" if h < 12 else "Afternoon" if h < 18 else "Evening"
        )
        self.df.to_csv(DATA_PATH, index=False)
        self.analyzer = CarWashAnalyzer(self.df)
        print("Preprocessing complete.")

    def show_menu(self):
        while True:
            print("\n--- Car Wash Analysis Menu ---")
            print("1. Analyze Customer Churn")
            print("2. Recommend Service Packages")
            print("3. Analyze Seasonality")
            print("4. Track Carbon Footprint")
            print("5. Identify Low-Sales Month")
            print("6. Rank Services")
            print("7. Show All Visualizations")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.analyzer.analyze_churn_rate()
            elif choice == "2":
                self.analyzer.recommend_service_packages()
            elif choice == "3":
                self.analyzer.analyze_seasonality()
            elif choice == "4":
                self.analyzer.track_carbon_footprint()
            elif choice == "5":
                self.analyzer.identify_low_sales_month()
            elif choice == "6":
                self.analyzer.rank_services()
            elif choice == "7":
                self.visualizer.show_all_plots()
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    app = CarWashApp()
    app.preprocess_data()
    app.show_menu()
