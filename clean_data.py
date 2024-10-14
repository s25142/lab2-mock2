import numpy as np
import pandas as pd
import requests
import logging
from sklearn.preprocessing import StandardScaler

logging.basicConfig(
    filename='log.txt',  # Log file
    level=logging.INFO,
    filemode='w',# Set the logging level
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.getLogger().addHandler(logging.StreamHandler())

def standardize_data(df):

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def clean_data(file_name):
    df = pd.read_csv(file_name, sep=",")

    logging.info("Liczba wierszy przed czyszczeniem danych: %d", df.shape[0])
    before_cleaning_size = df.shape[0]

    df.replace('', np.nan, inplace=True)

    df['Plec'] = df['Plec'].astype('category')
    df['Wiek'] = pd.to_numeric(df['Wiek'], errors='coerce')
    df['Wyksztalcenie'] = df['Wyksztalcenie'].astype('category')
    df['srednie Zarobki'] = pd.to_numeric(df['srednie Zarobki'], errors='coerce')
    df['Czas Poczatkowy podrozy'] = pd.to_datetime(df['Czas Poczatkowy podrozy'], format='%H:%M', errors='coerce')
    df['Czas Koncowy Podrozy'] = pd.to_datetime(df['Czas Koncowy Podrozy'], format='%H:%M', errors='coerce')
    df['Cel Podrozy'] = df['Cel Podrozy'].astype('category')

    logging.info("Rozpoczecie czyszczenia danych...")

    #remove duplicates
    df.drop_duplicates(inplace=True)

    #cleaning empty rows - remove rows where is missing at least 3 columns
    df.dropna(inplace=True, thresh=4)


    before_filling_cells = df.isna().sum().sum()

    #fill empty cells earnings with mean
    median = df['srednie Zarobki'].median()
    df.fillna({'srednie Zarobki': median}, inplace=True)

    avg_age = df['Wiek'].mean()
    df.fillna({'Wiek': avg_age}, inplace=True)

    #fill categorical columns when empty
    categories_df = df['Plec'].dropna().unique()
    df.fillna({'Plec' : np.random.choice(categories_df)}, inplace=True)

    categories_df = df['Wyksztalcenie'].dropna().unique()
    df.fillna({'Wyksztalcenie' : np.random.choice(categories_df)}, inplace=True)

    categories_df = df['Cel Podrozy'].dropna().unique()
    df.fillna({'Cel Podrozy': np.random.choice(categories_df)}, inplace=True)

    after_filling_cells = df.isna().sum().sum()

    df.dropna(inplace=True, thresh=7)

    # standarize data
    logging.info("standaryzacja danych...")
    df = standardize_data(df)

    df = df.reset_index(drop=True)

    removed_rows = before_cleaning_size - df.shape[0]

    logging.info("Zakonczono obrobke danych")
    logging.info("Liczba uzupelnionych komorek: %d", (before_filling_cells-after_filling_cells))
    logging.info("Liczba usunietych wierszy: %d", removed_rows)
    logging.info("Ilosc wierszy po obrobce: %d", df.shape[0])
    return df

if __name__ == "__main__":

    cleaned_data = clean_data("data.csv")

    pd.set_option('display.max_rows', None)  # Show all rows
    pd.set_option('display.max_columns', None)  # Show all columns

    print(cleaned_data)

    # Reset display options to default (optional)
    pd.reset_option('display.max_rows')
    pd.reset_option('display.max_columns')


