# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import requests
from bs4 import BeautifulSoup

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup

def get_papers_for_CVF(url):
    soup = get_soup(url)
    papers = soup.select(
        'dt > a'
    )
    
    for paper in papers[:5]:
        pdf_url = main_url + paper.get('href')
        pdf_url = pdf_url.replace('.html', '.pdf')
        pdf_url = pdf_url.replace('/html/', '/papers/')
        
        print(paper.text)
        print(pdf_url)

        print()