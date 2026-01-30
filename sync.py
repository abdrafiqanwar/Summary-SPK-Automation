from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
import pandas as pd
import os, gspread, warnings

warnings.filterwarnings("ignore", message="Workbook contains no default style*")

load_dotenv()

download_path = os.getenv("DOWNLOAD_PATH")
spreadsheet_id = os.getenv("SPREADSHEET_ID")

def sync_data():
    files = [
        os.path.join(download_path, f)
        for f in os.listdir(download_path)
        if f.endswith(".xls")
    ]

    if not files:
        print("File tidak ditemukan ⚠️")
        return
    
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_id)

    for file in files:
        file_name = os.path.basename(file)

        if file_name.startswith("SPK"):
            sheet_name = "SPK"
        elif file_name.startswith("DO"):
            sheet_name = "DO"

        df = pd.read_html(file)[0]
        df = df.fillna("")

        worksheet = spreadsheet.worksheet(sheet_name)
        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())

        resize_columns(spreadsheet, worksheet, df)


def resize_columns(spreadsheet, worksheet, df):
    sheet_id = worksheet.id
    col_count = len(df.columns)

    body = {
        "requests": [
            {
                "autoResizeDimensions": {
                    "dimensions": {
                        "sheetId": sheet_id,
                        "dimension": "COLUMNS",
                        "startIndex": 0,
                        "endIndex": col_count
                    }
                }
            }
        ]
    }

    spreadsheet.batch_update(body)
