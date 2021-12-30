from os import scandir
from time import sleep
from bs4.element import PreformattedString
import requests
import cloudscraper
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
scraper = cloudscraper.create_scraper()

#name = ["SCAN-3060","SCAN-3060Ti","SCAN-3070","SCAN-3070Ti","SCAN-3080"] #Now name scraped from html
urls = ["https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3060-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/geforce-rtx-3060-ti-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3070-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/geforce-rtx-3070-ti-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3080-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/geforce-rtx-3080-ti-graphics-cards",\
        "https://www.scan.co.uk/shop/gaming/virtual-reality/nvidia-geforce-rtx-3090-graphics-cards"]
search_quiry = ["Add To Basket","Add To Basket","Add To Basket","Add To Basket","Add To Basket","Add To Basket",\
                "Add To Basket"]
notified = list()

BOT_TOKEN = '5016485044:AAGIVrmZTrVwDAT3Hux9KyYl5lIZs2tFES4'
BOT_CHAT_ID = '1916973474'
SEARCH_INTERVAL = 5 #in secs
RESET_NOTIFIED_INTERVAL = 86400 #in secs
NUMBER_OF_WEBSITES = len(urls)

def telegram_bot_sendtext(bot_message):
    
    bot_token = BOT_TOKEN
    bot_chatID = BOT_CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    return response.json()

'''this takes product tags and the get the contents inside the tags and scrapes the relevant data inside and send'''
def get_stock_info():

    for i in range(NUMBER_OF_WEBSITES):

        '''Scrape the webpage as txt format and parse it to html-readable format using soup'''
        html = scraper.get(urls[i]).text
        soup = BeautifulSoup(html,"html.parser")

        '''find_all contents within "li" tags with attribute class=... and ... then combine them into one list
            soup forms a list of all matching results using find_all method'''
        all_products = soup.find_all('li', attrs={'class':'featuredProduct product'}) + soup.find_all('li', attrs={'class':'product'})

        '''find out if the word is in each product content'''
        for product in all_products:
            if search_quiry[i] in str(product) and product not in notified:
                # print(product)
                name_values = re.findall(r'data-description="(.*?)"', str(product)) #A list of attrs values in ___=""
                price_values = re.findall(r'data-price="(.*?)"', str(product))
                have_not_found_name = True #Prevent multiple print of the same item
                for index in range(len(name_values)):
                    if "RTX" in name_values[index] and have_not_found_name:
                        test = telegram_bot_sendtext("Item: " + name_values[index] + " | Link: " + urls[index] + " | Price: " + str(price_values[index]) + " | In Stock: " + str(search_quiry[index] in str(product)))
                        # print(name_values[index])
                        # print(price_values[index])
                        have_not_found_name = False
            notified.append(product)

'''old_get_stock function simply checks if in-stock indicator is in the product page's html'''
def old_get_stock_info():
    
    # soup = BeautifulSoup(html,"html.parser")
    # href_all = soup.find_all('a',href=True)
    # for link in soup.find_all('a', href=True):
    #     print(link.get('href'))

    index = 0
    # html = scraper.get(urls[index]).text
    # print(html) #Check html
    while index < len(name):
        html = scraper.get(urls[index]).text
        soup = BeautifulSoup(html,"html.parser")
        for contents in soup.find_all('div', attrs={'class':'productsCont productList list'}):
            if (search_quiry[index] in str(contents)) and not_sent[index]:
                test = telegram_bot_sendtext("Item: " + name[index] + " | Link: " + urls[index] + " | In Stock: " + str(search_quiry[index] in str(html)))
                not_sent[index] = False #To send once 
        index += 1

        # else:
        #     test = telegram_bot_sendtext("Item: " + name + " | Link: " + url + " | In Stock: " + str(search_quiry in str(html)))

start = datetime.now()
while True:
    now = datetime.now()
    '''resetting the notified list every day'''
    if now >= start + timedelta(seconds=(RESET_NOTIFIED_INTERVAL)) and now <= RESET_NOTIFIED_INTERVAL + timedelta(seconds=5 + (SEARCH_INTERVAL + 1)):
        notified = []
        start = now

    get_stock_info()
    sleep(SEARCH_INTERVAL) 
