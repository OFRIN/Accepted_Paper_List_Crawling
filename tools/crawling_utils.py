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

            sub_pdf_url = soup_per_paper.select_one('#content > dl > dd > a').get('href')

            if '2021' in sub_pdf_url and 'WACV' in sub_pdf_url:
                sub_pdf_url = sub_pdf_url[1:]
            else:
                sub_pdf_url = sub_pdf_url[6:]

            pdf_url = url + sub_pdf_url
            
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
                if len(data) >= 3:
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

            try:
                sub_pdf_url = soup_per_paper.select_one('#content > dl > dd > a').get('href')
            except:
                self.set_selenium()

                soup_per_paper = self.get_soup(sub_url, delay=1)
                sub_pdf_url = soup_per_paper.select_one('#content > dl > dd > a').get('href')

                self.set_requests()

            if '2020' in sub_pdf_url:
                sub_pdf_url = sub_pdf_url[12:]
            else:
                sub_pdf_url = 'papers/eccv_2018/' + sub_pdf_url[6:]

            pdf_url = url + sub_pdf_url

            title = remove_wrong_keyword(title)
            abstract = remove_wrong_keyword(abstract)
            
            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })
            
            if self.debug:
                if len(data) >= 5:
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

            p_tags = contents.find_all('p')

            try:
                abstract = contents.find_all('p')[-1].text
            except IndexError:
                print('# title : {}'.format(title))
                print('# length of p_tags : {}'.format(len(p_tags)))
                print('# sub_url : {}'.format(sub_url))
                input()

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

    def parse_for_openreview(self, soup):
        data = []
        openreview_url = 'https://openreview.net'

        papers = soup.find_all('div', {'class':"maincard narrower Poster"})
        length = len(papers)

        self.set_selenium()

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d]'%(paper_index + 1, length))
            sys.stdout.flush()

            title = paper.find('div', {'class':'maincardBody'}).text

            sub_url = paper.find('a', {'class':'btn btn-default btn-xs href_PDF'}).get('href')
            soup_per_paper = self.get_soup(sub_url, delay=2)

            abstract = soup_per_paper.find('span', {'class':'note_content_value'}).text
            pdf_url = openreview_url + soup_per_paper.find('a', {'class':'note_content_pdf'}).get('href')

            bibtex = ''

            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })
            
            if self.debug:
                if len(data) >= 5:
                    break
        
        print()
        self.set_requests()

        return data

    def parse_for_virtual(self, soup, main_url):
        data = []

        cards = soup.find('div', {'class':"cards row"})
        papers = cards.find_all('div', {'class':"myCard col-xs-6 col-md-4"})

        length = len(papers)

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d]'%(paper_index + 1, length))
            sys.stdout.flush()

            sub_url = main_url + paper.find('a').get('href')
            soup_per_paper = self.get_soup(sub_url)

            title = soup_per_paper.find('h2', {'class':'card-title main-title text-center'}).text
            abstract = soup_per_paper.find('div', {'id':'abstractExample'}).text[len('abstract:'):]
            pdf_url = soup_per_paper.select_one('body > div:nth-child(9) > div:nth-child(1) > div > div.text-center.p-3 > a:nth-child(2)').get('href')
            
            title = remove_wrong_keyword(title)
            abstract = remove_wrong_keyword(abstract)
            bibtex = ''
            
            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })
            
            if self.debug:
                if len(data) >= 5:
                    break
        
        print()

        return data