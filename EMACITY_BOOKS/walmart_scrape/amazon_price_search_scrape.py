import csv
from bs4 import BeautifulSoup
import requests
from selenium import webdriver

def get_url(search_term):
    '''
    Creates correct format of url from a specific search term.
    Parameters:
    --------------------------------------------
    search_term: string of product that is wanted to be searched.
    '''
    template = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
    search_term = search_term.replace(' ', '+')
    return(template.format(search_term))

def extract_record(item):
    '''
    Extract and return data from a single record.
    Parameters:
    ---------------------------------------------
    item: one search result from the search term.
    '''
    
    #description and url
    atag = item.h2.a
    description = atag.text
    url = 'https://www.amazon.com' + atag.get('href')
    
    #Price
    try:
        price = item.find('span', class_ = 'a-price').find('span', class_ = 'a-offscreen').text
    except AttributeError:
        return
    
    #Tuple of description, url, and price
    results = (description, url, price)
    return results

def find_amazon_prices(search_term):
    '''
    Finds the prices of a search term and returns their description and price.
    Parameters:
    ---------------------------------------------
    search_term: string of product we will be searching the price for on amazon.
    '''
    
    #start the driver
    driver = webdriver.Firefox(executable_path=r'/Users/michael/Downloads/geckodriver')
    
    records = []
    url = get_url(search_term)
    
    #Get the information from each item in the search
    driver.get(url.format())
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    for item in results:
        record = extract_record(item)
        if record:
            records.append(record)
    driver.close()
    return records
    #save data to something, right now a csv