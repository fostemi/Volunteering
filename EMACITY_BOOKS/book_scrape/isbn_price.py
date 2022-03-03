from selectorlib import Extractor
import requests 
import json 
from time import sleep


# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_results.yml')

def scrape(url):  

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    #print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create 
    return e.extract(r.text)

def get_price(isbn):
    
    price_list = []
    
    with open('search_results_output.jsonl','w') as outfile:
        search = isbn
        #print(search)
        data = scrape('https://www.amazon.com/s?k=' + search + '&i=stripbooks&ref=nb_sb_noss') 
        #data = scrape('https://www.amazon.com/s?k=1577314808&i=stripbooks&ref=nb_sb_noss')
        if data:
            for product in data['products']:
                #product['search_url'] = url
                #print("Saving Product: %s"%product['title'])
                json.dump(product,outfile)
                outfile.write("\n")
                
    
    with open('search_results_output.jsonl','r') as filelist:
        for product in filelist.read().splitlines():
            price_idx = product.find("price")
            price = product[price_idx+10:price_idx+14]
            price_list.append(price)
            
    price_1 = float(price_list[0])
    #print(price_1)
    return(price_1)

if __name__ == '__main__':
	print(get_price("9781577314806"))

    
