import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def walmart_rollbacks(store_code):
    '''
    Scrapes Walmart.com to find the different items on rollback and returns a tuple of the product name and price.
    Parameters:
    -----------------------------------------------
    store_code: integer of the location of walmart based on given zipcode.
    '''
    departments = ['furniture', 'hardware', 'fashion', 'electronics', 'toys', 'patio-garden']
    records = []
    for department in departments:
        url = 'https://www.walmart.com/store/'+ str(store_code) + '/' + department
        web_html = requests.get(url).text
        soup = BeautifulSoup(web_html, 'lxml')
    
        rollbacks = soup.find_all('div', class_ = 'rollback-result-wrapper')
        
        #print(department)
        
        for products in rollbacks:
            product_name = products.find('div', style = 'max-height:3em;overflow:hidden').text
            product_price = products.find('span', class_ = 'price-characteristic')
            if (products.find('span', class_ = 'price-characteristic')):
                #print(product_name)
                #print(product_price.text)
                records.append((product_name, product_price.text))
    return records
