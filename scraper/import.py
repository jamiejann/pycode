#from urllib2 import urlopen as uReq
import urllib2
import time
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#user_input = raw_input("What brand are you looking for? ")
#user_input = user_input.replace(' ', '-').lower()
#print(user_input)

url = 'http://www.grailed.com/shop/chrome-hearts'

#403 if no headers
hdr = { 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
         'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
         'Accept-Encoding': 'none',
         'Accept-Language': 'en-US,en;q=0.8',
         'Connection': 'keep-alive'}

options = Options()

options.add_argument("--headless")

driver = webdriver.Chrome('/mnt/c/Users/jami/Desktop/master/chromedriver.exe', options = options) 

driver.get(url)

#grailed needs time to populate items
time.sleep(3)

bs = soup(driver.page_source, 'html.parser')

#find containers
containers = bs.find_all("div", class_="feed-item")

filename = "products.csv"
f = open(filename, "w")

headers = "brand, original_price, new_price\n"
f.write(headers)

item_number=1
for container in containers:

    brand_container = container.find_all("h3", class_="listing-designer")
    brand = brand_container[0].text.strip()

    original_price_container = container.find_all("h3", class_="original-price")
    original_price = original_price_container[0].text.strip()

    if(container.find_all("h3", class_="new-price")):
        new_price_container = container.find_all("h3", class_="new-price")
        new_price = new_price_container[0].text.strip()

        print("item #: " + str(item_number) + "brand: " + brand + "  original price: " + str(original_price) +"  new price: " + str(new_price))

        f.write(brand + "," + original_price.replace(",", "") + "," + str(new_price) + "\n")

        del new_price

    else:
        print("item #: " + str(item_number) + "brand: " + brand + "  original price: " + str(original_price))
        f.write(brand + "," + str(original_price) + "," + str("-") + "\n")

    item_number = item_number + 1

    if item_number == 51: break

f.close()
        
    
