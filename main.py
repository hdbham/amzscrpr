import requests
from bs4 import BeautifulSoup
import pandas as pd
from random import randint
from time import sleep
from lxml.html import fromstring

print("Please wait - Finding working proxy")
url = 'https://free-proxy-list.net/anonymous-proxy.html'
response = requests.get(url)
parser = fromstring(response.text)
proxies = []

for i in parser.xpath('//tbody/tr')[:20]:
    if i.xpath('.//td[7][contains(text(),"yes")]'):
        proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])

    try:
        t = requests.get("https://www.google.com/", proxies={"http": proxy, "https": proxy}, timeout=5)
        if t.status_code == requests.codes.ok:
            proxies.append(proxy)
    except:
        pass

proxy = proxies[randint(0, len(proxies)-1)]
print("Sucessful proxy " + proxy
)

headers = {
   'accept': '*/*',
   'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53',
   'Accept-Language': 'en-US,en;q=0.9,it;q=0.8,es;q=0.7',
   'referer': 'https://www.google.com/',
   'cookie': 'DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0'
}  

queryString = input('Please input Search Params: ')
search_query = queryString.replace(' ', '+')
print("Searching for " + queryString)
base_url = 'https://www.amazon.com/s?k={0}'.format(search_query)

maxRange = input("How many pages to scrape? ")
maxRange = int(maxRange)

Outeritems = []
for i in range(1, maxRange):
    print('Processing {0}...'.format(base_url + '&page={0}'.format(i)))
    response = requests.get(base_url + '&page={0}'.format(i), headers=headers, proxies={"http": proxy, "https": proxy})
  
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
  # print(results)

    #get urls from pages 
    for result in results:
        product_name = result.h2.text

        try:
            rating = result.find('i', {'class': 'a-icon'}).text
            rating_count = result.find_all('span', {'aria-label': True})[1].text
        except AttributeError:
            continue

        
        try:
            price1 = result.find('span', {'class': 'a-price-whole'}).text
            price2 = result.find('span', {'class': 'a-price-fraction'}).text
            price = float(price1 + price2)
            product_url = 'https://amazon.com' + result.h2.a['href']
            
            Outeritems.append([product_url])
        except AttributeError:
            continue
sleep(randint(8,20))
    
df = pd.DataFrame(items, columns=['product_url'])
df.to_csv('{0}.csv'.format(search_query), index=False
          
'''
innerItems = []

for index, row in enumerate(df):
    pageUrl = row. # is this the right way to inject url into request.get?
  
    response = requests.get(pageUrl, headers=headers, proxies={"http": proxy, "https": proxy})
  
    soup = BeautifulSoup(response.content, 'html.parser')
    results = soup.find_all('div', {'class': 's-result-item', 'data-component-type': 's-search-result'})
  # print(results)
  
    for result in results:
        product_name = result.h1.text
        try:
            description = result.find('span', {'class': 'a-section content'}).text
        except AttributeError:
            continue
        try:
            innerItems.append([product_name, description])
        except AttributeError:
            continue
    sleep(randint(1,20))
    
df = pd.DataFrame(items, columns=['product_name', 'description'])
df.to_csv('{0}.csv'.format(search_query), index=False)
'''
