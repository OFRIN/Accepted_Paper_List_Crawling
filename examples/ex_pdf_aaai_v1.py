import sys
import arxiv
import difflib
import pdfplumber

import requests
from bs4 import BeautifulSoup

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup

def get_titles_for_aaai(pdf_path):
    titles = []
    reader = pdfplumber.open(pdf_path)

    length = len(reader.pages)

    for index_of_page, page in enumerate(reader.pages):
        sys.stdout.write('\r[%03d/%03d]'%(index_of_page + 1, length))
        sys.stdout.flush()

        text = page.extract_text()

        text = text.replace('\xa0', '')
        text = text.replace('\xad', '')

        papers = text.split('\n \n')

        for paper in papers:
            try:
                index = int(paper.split(':')[0])
            except ValueError:
                continue

            strings = paper.replace(f'{index}: ', '').split('\n')
            
            title = ''
            single_author = True

            for string in strings:
                if ',' in string:
                    single_author = False
                    break

                title += string

            if single_author:
                title = title.replace(strings[-1], '')

            title = title.replace('-', '')

            if title == '':
                print()
                print(title, strings)
                input()

            titles.append(title)

        # break
    print()

    return titles

# google 결과도 정확하지 않음. (PDF 있는 href 태그만 찾아도 어려움)

titles = get_titles_for_aaai('./data/AAAI2019.pdf')

error_count = 0
length = len(titles)

for index_of_title, title in enumerate(titles):
    sys.stdout.write('\r[%03d/%03d] = {}'%(index_of_title + 1, length))
    sys.stdout.flush()

    low_title = title.lower()
    results = arxiv.Search(title, max_results=5).get()

    info = None

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
    
    if info is not None:
        # print(result.title)
        # print(result.pdf_url)
        # print(result.summary.replace('\n', ''))
        # print()
        pass
    else:
        # print('ERROR : \"{}\"'.format(title))
        error_count += 1

        # input()

print(length, error_count)