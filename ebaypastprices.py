from numpy import product
import requests
from bs4 import BeautifulSoup
import pandas as pd 
from ProcessData import *

"""
Everything in this file is meant to go to eBay and grab data from listings
Once we grab all of the listings, we will place them into a list with the following: 

'title': 
'soldprice': 
'link': 
'date': 

"""

#PSA 10 Link
#url = 'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=Sylveon+V+TG14+psa+10&_sacat=0&LH_TitleDesc=0&rt=nc&_odkw=Sylveon+V+TG14+psa&_osacat=0&LH_Complete=1&LH_Sold=1'
#Only TG14 Link
url = 'https://www.ebay.com/sch/i.html?_from=R40&_nkw=charizard+upc&_sacat=2536&rt=nc&LH_Sold=1&LH_Complete=1&_ipg=240'
#Create a function that will parse the URL and requests the data from page and makes soup variable so we can pocess. 
def get_data(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return parse(soup)

def parse(soup):
    productsList = []
    results = soup.find_all('div', {'class', 's-item__info clearfix'})
    for item in results:

        #Elements that every listing have
        title = item.find('div', {'class', 's-item__title'}).text
        link = item.find('a', {'class', 's-item__link'})['href']
        rawSoldPrice = item.find('span', {'class', 's-item__price'}).text.replace('$', '').replace(',','').replace(' estimate', '').split()


        date = item.find_all('div', {'class', 's-item__title--tag'})
        if len(date) > 0:
            rawDate = date[0].text.replace('Sold ', '').replace('Item', '')
            print(rawDate)

        #Calculate and prase the shipping from the listing 
        ship = item.find_all('span', {'class', 's-item__shipping'})
        shippingCost = 0
        if len(ship) > 0:
            rawShip = ship[0].text
            if 'Free' in rawShip:
                shippingCost = 0
            else:
                shippingCost = rawShip.replace('+$', '').replace(' shipping', '').replace(', ', '').replace(' estimate', '')
        

        #If the listing has two prices, include both of them
        if len(rawSoldPrice) == 2:
            product2 = {
                'title': title,
                'soldprice': float(rawSoldPrice[2]) + float(shippingCost),
                'link': link,
                'date': date
            }
            productsList.append(product2)

        #Add the price to the list
        product1 = {
            'title': title,
            'soldprice': float(rawSoldPrice[0]) + float(shippingCost),
            'link': link,
            'date': date
        }
        productsList.append(product1)
    return productsList

list = get_data(url)

keywords = ['PSA', 'BGS', 'graded'] 
filteredList = excludeWords(list, keywords)
saveList(filteredList)
print('Filtered:', getAverage(filteredList), ' sample size:', len(filteredList))
print('No Filter:', getAverage(list), ' sample size:', len(list))
