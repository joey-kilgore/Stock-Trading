import html2text
import requests
import ReadSymbols
import Spreadsheet
import MathAnalysis
import time

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

def getMentionedStocks():
    # Setup for all urls
    urlList = Spreadsheet.getURLs()
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

    # get the stocks that were mentioned more than once and sort them accordingly
    highMentions = []
    for key in mentions.keys():
        if(mentions[key] > 0):
            # print(key + " : " + str(mentions[key])) # DEBUG CODE
            highMentions.append((key, mentions[key]))
    
    highMentions = sorted(highMentions, key= lambda x: x[1], reverse=True)

    print()
    print("NUMBER OF STOCKS FOUND : " + str(len(highMentions)))
    return highMentions
    

if(__name__ == "__main__"):
    mentionTuples = getMentionedStocks()

    for mention in mentionTuples:
       try:
            score = MathAnalysis.scoreStock(mention[0])
            print(mention[0] + " mentioned : " + str(mention[1]) + " times scored : " + str(score))
        except:
            print(mention[0] + " failed to access")
        time.sleep(60) # sleep between each stock to not overload alpha vantage