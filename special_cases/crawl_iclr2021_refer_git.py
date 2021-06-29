# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

import time

import requests
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

from tools import json_utils

driver = None

def get_soup(url, option='requests', delay=1):
    global driver 

    if option == 'requests':
        req = requests.get(url)
        page_source = req.text
    else:
        if driver is None:
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

def read_tsv(path):
    with open(path, 'r', encoding='utf-8') as f:
        dataset = []
        for line in f.readlines()[1:]:
            data = line.strip().split('\t')
            dataset.append(data)
    return dataset

def read_papers(paper_path, rating_path):
    papers = read_tsv(paper_path)

    paper_dict = {}
    for (id, title, link, _, abstract) in papers:
        # print(id, title, link)
        # input()

        paper_dict[id] = {
            'title' : title,
            'abstract' : abstract,
            'bibtex' : "",
            'pdf_url' : link
        }
    
    print('# Number of Papers : {}'.format(len(list(paper_dict.keys()))))

    for data in read_tsv(rating_path):
        id = data[0]
        decision = data[-1]
        
        if 'Accept' in decision:
            format = decision.replace('(', '').replace(')', '').replace('Accept ', '')
            paper_dict[id]['format'] = format
        else:
            del paper_dict[id]

    print('# Number of Accepted Papers : {}'.format(len(list(paper_dict.keys()))))

    return paper_dict

openreview_url = 'https://openreview.net'
paper_dict = read_papers('./data/iclr2021/paperlist.tsv', './data/iclr2021/ratings.tsv')

paper_ids = list(paper_dict.keys())
length = len(paper_ids)

data = []
data_path = f'./data/conferences/ICLR2021.json'

for i, paper_id in enumerate(paper_ids):
    sys.stdout.write('\r[{}/{}]'.format(i + 1, length))
    sys.stdout.flush()

    # if i > 10:
    #     break

    paper = paper_dict[paper_id]

    soup_per_paper = get_soup(paper['pdf_url'], 'selenium', delay=2)

    title = paper['title']
    abstract = paper['abstract']
    bibtex = paper['bibtex']
    format = paper['format']
    pdf_url = openreview_url + soup_per_paper.find('a', {'class':'note_content_pdf'}).get('href')
    
    # print()
    # print('# Title : \"{}\"'.format(title))
    # print('# Abstract : \"{}\"'.format(abstract))
    # print('# PDF : \"{}\"'.format(pdf_url))
    # print('# Format : \"{}\"'.format(format))
    # input()

    data.append({
        'title' : title,
        'abstract' : abstract,
        'bibtex' : bibtex,
        'pdf_url' : pdf_url,
        'format' : format,
    })

json_utils.write_json(data_path, data, encoding='utf-8')