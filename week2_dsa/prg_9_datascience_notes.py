import pandas as pd

def read_csv_file():
    file_path = r"C:\Users\student\Downloads\Indian_Kids_Screen_Time.csv"


    df = pd.read_csv(file_path)

    print(df.count())
    print(df.head())
    print(df.tail())

def read_csv_file1():
    file_path = r"C:\Users\student\Downloads\Indian_Kids_Screen_Time.csv"
    df = pd.read_csv(file_path)
    for index, row in df.iterrows():
        print(row[0], '  ', row[1])

def read_csv_file2():
    file_path = r"C:\Users\student\Downloads\Indian_Kids_Screen_Time.csv"
    df = pd.read_csv(file_path)
    for row in df.iterrows():
        print(row[1][0], row[1][1])

read_csv_file()
