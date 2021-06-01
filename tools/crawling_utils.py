# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import sys
import time

import requests
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

from .text_utils import remove_wrong_keyword

class Crawler:
    def __init__(self):
        self.debug = True
        self.driver = self.make_webdriver('./data/chromedriver')

        self.set_requests()

    def set_debug(self, status):
        self.debug = status

    def make_webdriver(self, chrome_path):
        options = webdriver.ChromeOptions()

        # options.add_argument('headless')
        # options.add_argument('window-size=1920x1080')
        # options.add_argument("disable-gpu")

        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')

        return webdriver.Chrome(chrome_path, chrome_options=options)

    def set_requests(self):
        self.option = 'requests'

    def set_selenium(self):
        self.option = 'selenium'

    def get_soup(self, url, delay=1):
        if self.option == 'requests':
            req = requests.get(url)
            page_source = req.text

        elif self.option == 'selenium':
            self.driver.get(url)
            time.sleep(delay)
            page_source = self.driver.page_source

        else:
            page_source = None

        if page_source is not None:
            soup = BeautifulSoup(page_source, 'html.parser')
        else:
            soup = None

        return soup

    def get_string_from_url(self, url):
        data = ''
        for line in urllib.request.urlopen(url):
            data += line.decode('utf-8')
        return data

    def parse_for_cvf(self, soup, url):
        data = []

        papers = soup.select('dt > a')
        length = len(papers)

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d]'%(paper_index + 1, length))
            sys.stdout.flush()

            sub_url = url + paper.get('href')
            soup_per_paper = self.get_soup(sub_url)
            
            title = soup_per_paper.find("div", {"id": "papertitle"}).text
            abstract = soup_per_paper.find("div", {"id": "abstract"}).text
            bibtex = soup_per_paper.find("div", {"class": "bibref"}).text
            pdf_url = url + soup_per_paper.select_one('#content > dl > dd > a').get('href')[6:]
            
            title = remove_wrong_keyword(title)
            abstract = remove_wrong_keyword(abstract)
            bibtex = remove_wrong_keyword(bibtex)

            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })

            if self.debug:
                if len(data) >= 10:
                    break
        
        print()

        return data

    def parse_for_eccv(self, soup, url):
        data = []

        papers = soup.find_all("dt", {"class":"ptitle"})
        length = len(papers)

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d]'%(paper_index + 1, length))
            sys.stdout.flush()

            sub_url = url + paper.find('a').get('href')
            soup_per_paper = self.get_soup(sub_url)

            title = soup_per_paper.find("div", {"id": "papertitle"}).text
            abstract = soup_per_paper.find("div", {"id": "abstract"}).text
            bibtex = ''
            pdf_url = url + soup_per_paper.select_one('#content > dl > dd > a').get('href')[12:]

            title = remove_wrong_keyword(title)
            abstract = remove_wrong_keyword(abstract)
            
            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })
            
            if self.debug:
                if len(data) >= 10:
                    break
        
        print()

        return data

    def parse_for_nips(self, soup, url):
        data = []

        papers = soup.select('ul > li')
        length = len(papers)

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d]'%(paper_index + 1, length))
            sys.stdout.flush()

            sub_url = url + paper.find('a').get('href')
            if not 'hash' in sub_url:
                continue

            soup_per_paper = self.get_soup(sub_url)

            contents = soup_per_paper.find('div', {'class':'col'})

            title = contents.find('h4').text
            abstract = contents.find_all('p')[3].text

            tags = contents.find('div').find_all('a')

            bib_url = url + tags[1].get('href')
            bibtex = self.get_string_from_url(bib_url)

            pdf_url = ''
            for tag in tags[2:]:
                if 'Paper' in tag.text:
                    pdf_url = url + tag.get('href')
                    break

            bibtex = remove_wrong_keyword(bibtex)
            
            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })
            
            if self.debug:
                if len(data) >= 10:
                    break
        
        print()

        return data