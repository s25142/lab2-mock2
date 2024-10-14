import requests
import pandas as pd

def get_google_sheet(sheet_id, api_key, range_name):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")


if __name__ == "__main__":
    import os

    API_KEY = 'AIzaSyAywyd3osBMY8L-b-Lr3mPLDfxwB-Zq9MA'
    SHEET_ID = '1k-NR4HvbcAH8EcS129RSS4N_xI4gSRHD1OrJQkLfoJs'
    RANGE_NAME = 'data_student_25142'

    #SHEET_ID = os.getenv("SHEET_ID")
    #RANGE_NAME = os.getenv("RANGE_NAME")
    #API_KEY = os.getenv("API_KEY")

    data = get_google_sheet(SHEET_ID, API_KEY, RANGE_NAME)
    values = data.get('values', [])
    df = pd.DataFrame(values[1:], columns=values[0])
    df.to_csv("data.csv", sep=',', encoding='utf-8', index=False, header=True)
    print(data)