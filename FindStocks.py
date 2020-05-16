import html2text
import requests
import ReadSymbols
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


def getTextFromURL(url):
    # get the html from the url
    url = requests.get(url)
    htmltext = url.text

    # parse out the html to text and split by new lines
    h = html2text.HTML2Text()
    h.ignore_links = True
    text = h.handle(htmltext)
    text = text.splitlines()

    return text


# Setup for all urls
urlList = getURLs()
symbols = ReadSymbols.getSymbols()

# mentions will track the number of times a stock has been mentioned
mentions = {}
for sym in symbols:
    mentions[sym] = 0



urlNum = 0
for url in urlList:
    urlNum += 1
    print("URL " + str(urlNum) + "/" + str(len(urlList)))
    foundOnSite = []
    
    try:
        text = getTextFromURL(url)
    except:
        print("FAILED URL : " + url)
        continue

    # print(url) # DEBUG CODE
    for line in text:
        if(line.find('(') != -1):
            for sym in symbols:
                if(sym in foundOnSite):
                    continue

                if(line.find("("+sym+")") != -1 or line.find(":"+sym+")") != -1):
                    # print(sym + " : " + line) # DEBUG CODE
                    mentions[sym] += 1
                    foundOnSite.append(sym)

print()
print("STOCK MENTIONS")
for key in mentions.keys():
    if(mentions[key] > 0):
        print(key + " : " + str(mentions[key]))