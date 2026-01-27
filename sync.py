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
    else:
        latest_file = max(files, key=os.path.getctime)
        file_name = os.path.basename(latest_file)

        df = pd.read_html(latest_file)
        df = df[0]

        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
        client = gspread.authorize(creds)

        spreadsheet = client.open_by_key(spreadsheet_id)
        
        if file_name.startswith("SPK"):
            worksheet = spreadsheet.worksheet("SPK")
        elif file_name.startswith("DO"):
            worksheet = spreadsheet.worksheet("DO")
        
        df = df.fillna("")

        worksheet.clear()
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
