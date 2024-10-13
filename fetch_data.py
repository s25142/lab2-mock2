import requests


def get_google_sheet(sheet_id, api_key, range_name):
    url = f'https://sheets.googleapis.com/v4/spreadsheets/{sheet_id}/values/{range_name}?key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching data: {response.status_code}, {response.text}")


if __name__ == "__main__":
    import os

    SHEET_ID = os.getenv("SHEET_ID")
    RANGE_NAME = os.getenv("RANGE_NAME")
    API_KEY = os.getenv("API_KEY")

    data = get_google_sheet(SHEET_ID, API_KEY, RANGE_NAME)
    print(data)