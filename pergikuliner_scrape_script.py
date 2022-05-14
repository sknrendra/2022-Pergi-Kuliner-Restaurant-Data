import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import re

def selenium_getsource(link):
    browser = webdriver.Chrome(executable_path="/usr/local/bin/chromedriver")
    browser.get(link)
    source = browser.page_source
    browser.close()
    return source

def retrieve_pergikuliner(url):
    soup = BeautifulSoup(selenium_getsource(url))
    restaurant = pd.Series([])
    #imprecise
    restaurant[0] = soup.h1.get_text()
    restaurant[1] = soup.find(attrs={'class':'info-list'}).li.get_text()
    restaurant[2] = soup(attrs={'class': 'left'})[1].get_text()
    restaurant[3] = soup.link.get('href')
    restaurant[4] = soup.find(class_='info-list').find_all('li')[-1].get_text()
    #check multi-valued attributes
    restaurant[5] = re.search('(?<=content=).+?"', str(soup.find(itemprop='paymentAccepted'))).group()
    #precise
    promo = soup.find(attrs={'class': 'promotional-text'})
    restaurant[6] = str(promo.get_text) if promo is not None else None
    restaurant[7] = soup.find(string=re.compile('Rp. .* '))
    schedule = soup.find(attrs={'itemprop': 'openingHours'})
    restaurant[8] = str(schedule.get_text) if schedule is not None else None
    restaurant[9] = ','.join([result.get_text() for result in soup(class_='checked')])
    restaurant[10] = ','.join([result.get_text() for result in soup(class_='unchecked')])
    restaurant[11] = soup.find(href=re.compile("tel.*")).get_text()
    restaurant[12] = soup.find(itemprop='ratingValue').get_text()
    restaurant[13] = ','.join([i.getText().strip() for i in soup.find_all(class_='rate-box-bottom')])
    return restaurant

restaurants_compiled = []

for pageindex in range(1, 126):
    soup = BeautifulSoup(selenium_getsource(f'https://pergikuliner.com/restaurants?page={pageindex}'))
    links = soup.find_all(href=re.compile('restaurants'))
    for i in range(1, len(links), 2):
        urltest = re.search('/.*/.*/.*(?=")', str(links[i]))
        if urltest is None:
            pass
        else:
            urlext = urltest.group()
            restaurants_compiled.append(retrieve_pergikuliner(f'https://pergikuliner.com{urlext}'))

restaurants_dataset = pd.concat(restaurants_compiled, axis=1).T
restaurants_dataset.to_csv('pergikuliner_restaurants_dataset.csv', index=False)
