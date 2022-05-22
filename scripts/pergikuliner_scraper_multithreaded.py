import numpy as np
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor

def driver_setup():
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)

    return driver

def restdata_fetcher(url, driver):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source)

    itemdict = {'itemprop': 'openingHours', 'class': 'promotional-text', 'href' : re.compile('tel:')}
    resultbucket = []
    for k, v in itemdict.items():
        tag = soup.find(attrs={k: v})
        if tag is not None:
            result = tag.get_text() 
        else:
            result = None
        resultbucket.append(result)
        
    ratings = ','.join([i.getText().strip() for i in soup.find_all(class_='rate-box-bottom')])
    resultbucket.append(ratings)

    return pd.Series(resultbucket)

def review_fetcher(url, driver):
    #check if all the reviews are opened
    driver.get(url)
    show_next_review = driver.find_element(By.ID, "next_review")
    while show_next_review:
        show_next_review.click()
    #then loop through all of them

"""

"""

def crawler(lst, driver):
    resultcontainer=[]
    for pageindex in lst:
        l = f'https://pergikuliner.com/restaurants?page={pageindex}'
        driver.get(l)
        soup = BeautifulSoup(driver.page_source)
        links = soup.find_all(href=re.compile('restaurants'))
        for i, n in zip(range(1, len(links), 2), range(1,1500)):
            # print(f'fetching links, {pageindex}th page, {i}/12', end='\r')
            urltest = re.search('/.*/.*/.*(?=")', str(links[i]))
            if urltest is None:
                pass
            else:
                urlext = urltest.group()
                print(f'\rretrieving: {urlext}', end='')
                resultcontainer.append(restdata_fetcher(f'https://pergikuliner.com{urlext}', driver))
    return resultcontainer

#build as many drivers as there are threads, so each thread gets own driver
drivers = [driver_setup() for _ in range(4)]

#split pages into evenly sized chunks
#then feed each chunks to its own threads
chunks = np.array_split(np.arange(1,126), 4)

with ThreadPoolExecutor(max_workers=4) as executor:
    bucket = executor.map(crawler, chunks, drivers)
    results = [item for block in bucket for item in block]

[driver.quit() for driver in drivers]

df = pd.concat(results, axis=1).T