from time import sleep
import requests
import cloudscraper
import re
from bs4 import BeautifulSoup
scraper = cloudscraper.create_scraper()

name = ["DX POOL - ST BOX","DX POOL - HS BOX","DX POOL - KD BOX"]
urls = ["https://www.dxpool.io/product/st-box/",\
        "https://www.dxpool.io/product/hs-box/",\
        "https://www.dxpool.io/product/goldshell-kd-box-hs-box-lb-box-bundles/"]
search_quiry = ["in stock","in stock","in stock"]
BOT_TOKEN = '5016485044:AAGIVrmZTrVwDAT3Hux9KyYl5lIZs2tFES4'
BOT_CHAT_ID = '1916973474'
TIME_TO_PAUSE = 10 #This is in seconds

def telegram_bot_sendtext(bot_message):
    
    bot_token = BOT_TOKEN
    bot_chatID = BOT_CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()
    
def get_stock_info():
    # soup = BeautifulSoup(html,"html.parser")
    # href_all = soup.find_all('a',href=True)
    # for link in soup.find_all('a', href=True):
    #     print(link.get('href'))

    index = 0
    # html = scraper.get(urls[index]).text
    # print(html) #Check html
    while index < len(name):
        html = scraper.get(urls[index]).text
        if search_quiry[index] in str(html):
            test = telegram_bot_sendtext("Item: " + name[index] + " | Link: " + urls[index] + " | In Stock: " + str(search_quiry[index] in str(html)))
        index += 1
        # else:
        #     test = telegram_bot_sendtext("Item: " + name + " | Link: " + url + " | In Stock: " + str(search_quiry in str(html)))

while True:
    get_stock_info()
    sleep(TIME_TO_PAUSE) 
