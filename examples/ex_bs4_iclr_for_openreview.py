import time

import requests
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

def get_soup(url, option='requests', delay=1):
    if option == 'requests':
        req = requests.get(url)
        page_source = req.text
    else:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')

        driver = webdriver.Chrome("./data/chromedriver", chrome_options=options)
        driver.get(url)
        
        time.sleep(delay)

        page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    return soup

def get_string_from_url(url):
    data = ''
    for line in urllib.request.urlopen(url):
        data += line.decode('utf-8')
    return data

conference = 'ICLR'
# conference = 'ICML' # ERROR
year = '2019'
# year = '2018'
url = 'https://{}.cc/Conferences/{}/Schedule?type=Poster'.format(conference.lower(), year)

soup = get_soup(url)
# soup = get_soup(main_url, 'selenium')

openreview_url = 'https://openreview.net'

papers = soup.find_all('div', {'class':"maincard narrower Poster"})

for paper in papers:
    title = paper.find('div', {'class':'maincardBody'}).text

    sub_url = paper.find('a', {'class':'btn btn-default btn-xs href_PDF'}).get('href')
    soup_per_paper = get_soup(sub_url, 'selenium', delay=2)

    abstract = soup_per_paper.find('span', {'class':'note_content_value'}).text
    pdf_url = openreview_url + soup_per_paper.find('a', {'class':'note_content_pdf'}).get('href')
    
    print()
    print('# Title : \"{}\"'.format(title))
    print('# Abstract : \"{}\"'.format(abstract))
    print('# PDF : \"{}\"'.format(pdf_url))
    input()
