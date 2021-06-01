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

def remove_wrong_keyword(data, front=True, back=True):
    lowered_data = data.lower()
    lowered_alphabet = 'abcdefghijknmlopqrstuvwxyz/.,;{}'

    start_index = 0
    end_index = len(data)

    cond_fn = lambda i: lowered_data[i] in lowered_alphabet

    if front:
        # find start index (->)
        for i in range(len(data) - 1):
            # If this is alphabet, loop statement is finished. 
            if cond_fn(i):
                break
            
            if not cond_fn(i) and cond_fn(i + 1):
                start_index = i + 1
                break
    
    if back:
        # find end index (<-)
        for i in range(len(data))[::-1]:
            if cond_fn(i):
                end_index = i + 1
                break
            
            elif cond_fn(i - 1) and not cond_fn(i):
                end_index = i
                break
    
    # print(start_index, end_index)
    return data[start_index:end_index]

conference = '2020'
main_url = 'https://iclr.cc/virtual_{}/'.format(conference)

# soup = get_soup(main_url + 'papers.html')
soup = get_soup(main_url + 'papers.html', 'selenium', delay=5)

cards = soup.find('div', {'class':"cards row"})
papers = cards.find_all('div', {'class':"myCard col-xs-6 col-md-4"})

print(len(papers))

for paper in papers:
    sub_url = main_url + paper.find('a').get('href')
    soup_per_paper = get_soup(sub_url)

    title = soup_per_paper.find('h2', {'class':'card-title main-title text-center'}).text
    abstract = soup_per_paper.find('div', {'id':'abstractExample'}).text[len('abstract:'):]
    pdf_url = soup_per_paper.select_one('body > div:nth-child(9) > div:nth-child(1) > div > div.text-center.p-3 > a:nth-child(2)').get('href')
    
    title = remove_wrong_keyword(title)
    abstract = remove_wrong_keyword(abstract)
    
    print()
    # print(sub_url)
    print('# Title : \"{}\"'.format(title))
    print('# Abstract : \"{}\"'.format(abstract))
    print(pdf_url)
    input()
