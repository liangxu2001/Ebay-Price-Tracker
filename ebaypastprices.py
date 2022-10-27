from numpy import product
import requests
from bs4 import BeautifulSoup
import pandas as pd 

url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=Sylveon+V+TG14+psa+10&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=Sylveon+V+TG14+psa&_osacat=0&LH_Complete=1&LH_Sold=1'

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

#Goes through the dictonary and removes any words from the title that we don't want
def requiredWords(list, keywords):
    newList = []
    for listing in list:
        title = listing['title']
        for word in keywords:
            if word in title:
                newList.append(listing)
    
    return newList



soup = get_data(url)
list = parse(soup)
keywords = ['PSA 10'] 
filteredList = requiredWords(list, keywords)
print('Filtered:', getAverage(filteredList))
print('No Filter:', getAverage(list))
