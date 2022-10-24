from numpy import product
import requests
from bs4 import BeautifulSoup
import pandas as pd 

url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=iphone+11+64gb&_sacat=0&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&rt=nc&Storage%2520Capacity=64%2520GB&_dcat=9355'

#Create a function that will parse the URL and requests the data from page and makes soup variable so we can pocess. 
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

def parse(soup):
    productsList = []
    results = soup.find_all('div', {'class', 's-item__info clearfix'})
    for item in results:

        title = item.find('div', {'class', 's-item__title'}).text
        link = item.find('a', {'class', 's-item__link'})['href']
        rawSoldPrice = item.find('span', {'class', 's-item__price'}).text.replace('$', '').replace(',','').split()

        #If the listing has two prices, include both of them
        if len(rawSoldPrice) == 2:
            product2 = {
                'title': title,
                'soldprice': float(rawSoldPrice[2]),
                'link': link,
            }
            productsList.append(product2)

        #Add the price to the list
        product1 = {
            'title': title,
            'soldprice': float(rawSoldPrice[0]),
            'link': link,
        }
        productsList.append(product1)
    return productsList

def getAverage(list):
    sum = 0
    for data in list:
        sum += data["soldprice"]
    return sum / len(list)

soup = get_data(url)
list = parse(soup)
print(getAverage(list))
