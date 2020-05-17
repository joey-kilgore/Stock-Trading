import gspread
from oauth2client.service_account import ServiceAccountCredentials

def getURLs():
    # https://www.youtube.com/watch?v=vISRn5qFrkM
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Stocks URLs').sheet1
    urls = sheet.col_values(1)
    return urls