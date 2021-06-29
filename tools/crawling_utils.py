# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import os
import sys
import time
import arxiv
import difflib

import requests
import pdfplumber

import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver

from .io_utils import download_file_using_url
from .json_utils import read_json, write_json
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
            if '2021' in sub_pdf_url and 'CVPR' in sub_pdf_url:
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

    def parse_for_nips(self, soup, url, json_path):
        if os.path.isfile(json_path):
            data = read_json(json_path, encoding='utf-8')
            titles = [d['title'] for d in data]
        else:
            data = []
            titles = []

        papers = soup.select('ul > li')
        length = len(papers)

        last_title = ''

        for paper_index, paper in enumerate(papers):
            sys.stdout.write('\r[%04d/%04d] title=%s'%(paper_index + 1, length, last_title))
            sys.stdout.flush()

            sub_url = url + paper.find('a').get('href')
            if not 'hash' in sub_url:
                continue
            
            try:
                soup_per_paper = self.get_soup(sub_url)
            except AttributeError:
                print('# url : {}'.format(url))
                print('# href : {}'.format(paper.find('a').get('href')))
                print('# sub_url : {}'.format(sub_url))
                input()

            contents = soup_per_paper.find('div', {'class':'col'})

            try:
                title = contents.find('h4').text
            except AttributeError:
                # server error = 500
                # print()
                # print('# sub_url : {}'.format(sub_url))
                # input()
                continue
            
            if title in titles:
                continue

            last_title = title
            
            p_tags = contents.find_all('p')

            try:
                abstract = contents.find_all('p')[-1].text
            except IndexError:
                print('# title : {}'.format(title))
                print('# length of p_tags : {}'.format(len(p_tags)))
                print('# sub_url : {}'.format(sub_url))
                input()

            tags = contents.find('div').find_all('a')

            pdf_url = ''
            bib_url = ''

            for tag in tags:
                if 'Paper' in tag.text and pdf_url == '':
                    pdf_url = url + tag.get('href')

                if 'Bibtex' in tag.text and bib_url == '':
                    bib_url = url + tag.get('href')
            
            bibtex = self.get_string_from_url(bib_url)
            # bibtex = remove_wrong_keyword(bibtex)
            
            data.append({
                'title' : title,
                'abstract' : abstract,
                'bibtex' : bibtex,
                'pdf_url' : pdf_url
            })

            if paper_index % 10 == 0:
                write_json(json_path, data, encoding='utf-8')
            
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

    def parse_for_aaai(self, name, pdf_url, json_path):
        if os.path.isfile(json_path):
            data = read_json(json_path, encoding='utf-8')
            checked_data = [d['title'] for d in data]
        else:
            data = []
            checked_data = []

        pdf_path = f'./data/{name}.pdf'
        if not os.path.isfile(pdf_path):
            download_file_using_url(pdf_url, pdf_path)
        
        titles = []
        reader = pdfplumber.open(pdf_path)

        if 'AAAI2019' in pdf_path:
            hint_of_authors = '('
        elif 'AAAI2020' in pdf_path:
            hint_of_authors = '('
        elif 'AAAI2021' in pdf_path:
            hint_of_authors = ','

        length = len(reader.pages)
        total_lines = []

        for index_of_page, page in enumerate(reader.pages):
            sys.stdout.write('\r[%03d/%03d]'%(index_of_page + 1, length))
            sys.stdout.flush()

            text = page.extract_text()

            text = text.replace('\xa0', '')
            text = text.replace('\xad', '')
            
            lines = text.split('\n')
            total_lines += lines

        index = 0
        length = len(total_lines)

        while index < length:
            # print(index, length)

            line = total_lines[index]; index += 1; 
            if not ':' in line:
                continue
            
            try:
                page_index = int(line.split(':')[0])
            except ValueError:
                continue
            
            title = line.replace(f'{page_index}: ', '').replace('-', '')

            line = total_lines[index].replace('-', ''); index += 1
            if not hint_of_authors in line:
                try:
                    # ignore page index
                    int(line.replace(' ', ''))
                    type_of_line = 'page_index' 
                except ValueError:
                    pass    
                
                second_line = total_lines[index]; index += 1
                if len(second_line) > 5:
                    type_of_line = 'sub-title'
                else:
                    type_of_line = 'author'

                if type_of_line == 'sub-title':
                    title += line
                else:
                    # print(title, '"{}"'.format(line), '"{}"'.format(second_line))
                    # input()
                    pass

            titles.append(title)

        length = len(titles)

        for paper_index, title in enumerate(titles):
            sys.stdout.write('\r[%03d/%03d] = %s'%(paper_index + 1, length, title))
            sys.stdout.flush()

            if title in checked_data:
                continue

            low_title = title.lower()
            results = arxiv.Search(title, max_results=10).get()

            info = None

            try:
                for result in results:
                    searched_title = result.title.lower()
                    similarity = difflib.SequenceMatcher(None, low_title, searched_title).ratio()
                    
                    # print(similarity)
                    # print(low_title)
                    # print(searched_title)
                    # print()

                    if similarity >= 0.90:
                        info = result
                        break
            
            except arxiv.arxiv.UnexpectedEmptyPageError:
                pass
            
            if info is not None:
                single_data = {
                    'title' : title,
                    'abstract' : result.summary.replace('\n', ' '),
                    'bibtex' : '',
                    'pdf_url' : result.pdf_url,
                }
            else:
                single_data = {
                    'title' : title,
                    'abstract' : '',
                    'bibtex' : '',
                    'pdf_url' : '',
                }

            data.append(single_data)
            
            if paper_index % 10 == 0:
                write_json(json_path, data, encoding='utf-8')
            
            if self.debug:
                if len(data) >= 10:
                    break
        
        print()

        return data

    # - Announced paper list on cvf foundation.
    # def parse_for_cvpr2021(self, json_path):
    #     if os.path.isfile(json_path):
    #         data = read_json(json_path, encoding='utf-8')
    #     else:
    #         data = []

    #     titles = []

    #     for page_name in range(168, 180):
    #         # Load URL for all CVPR 2021 accepted papers.
    #         self.driver.get("http://cvpr2021.thecvf.com/node/{}".format(page_name)) #FIXME

    #         table =  self.driver.find_elements_by_tag_name("table") 
    #         print("length of table : ", len(table))

    #         for i in range(len(table)):
    #             tbody = table[i].find_elements_by_tag_name("tbody")
    #             trs = tbody[0].find_elements_by_tag_name("tr")
                
    #             for j in range(1, len(trs)):
    #                 tds = trs[j].find_elements_by_tag_name('td')
    #                 titles.append(tds[1].text)

    #     print("The number of total accepted paper titles : ", len(titles))

    #     length = len(titles)

    #     for paper_index, title in enumerate(titles):
    #         sys.stdout.write('\r[%03d/%03d] = %s'%(paper_index + 1, length, title))
    #         sys.stdout.flush()

    #         try:
    #             if data[paper_index]['pdf_url'] != '':
    #                 continue
    #         except IndexError:
    #             pass
            
    #         low_title = title.lower()
    #         results = arxiv.Search(title, max_results=10).get()

    #         info = None

    #         try:
    #             for i, result in enumerate(results):
    #                 # if i > 10:
    #                 #     break

    #                 searched_title = result.title.lower()
    #                 similarity = difflib.SequenceMatcher(None, low_title, searched_title).ratio()
                    
    #                 # print(similarity)
    #                 # print(low_title)
    #                 # print(searched_title)
    #                 # print()

    #                 if similarity >= 0.90:
    #                     info = result
    #                     break
            
    #         except arxiv.arxiv.UnexpectedEmptyPageError:
    #             pass
            
    #         if info is not None:
    #             single_data = {
    #                 'title' : title,
    #                 'abstract' : result.summary.replace('\n', ' '),
    #                 'bibtex' : '',
    #                 'pdf_url' : result.pdf_url,
    #             }
    #         else:
    #             single_data = {
    #                 'title' : title,
    #                 'abstract' : '',
    #                 'bibtex' : '',
    #                 'pdf_url' : '',
    #             }

    #         data.append(single_data)
            
    #         if paper_index % 10 == 0:
    #             write_json(json_path, data, encoding='utf-8')
            
    #         if self.debug:
    #             if len(data) >= 10:
    #                 break
        
    #     print()

    #     return data