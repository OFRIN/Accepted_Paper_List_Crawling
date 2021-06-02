import os
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

    # show page
    # for line in lines:
    #     print(line)
    # print()
    # input()
    
    print(index, length)

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
            type_of_line = 'unknown'

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
                print(title, '"{}"'.format(line), '"{}"'.format(second_line))
                input()

            # ignore single author
        
        titles.append(title)

        # for making strategy to extract the title of paper without authors
        # input(title); continue

        # try:
        #     index = int(paper.split(':')[0])
        # except ValueError:
        #     continue
        
        # strings = paper.replace(f'{index}: ', '').split('\n')
        
        # title = ''
        # single_author = True

        # for string in strings:
        #     if ',' in string:
        #         single_author = False
        #         break

        #     title += string

        # if single_author:
        #     title = title.replace(strings[-1], '')

        # title = title.replace('-', '')

        # if title == '':
        #     print()
        #     print(title, strings)
        #     input()

        # titles.append(title)

    return titles

# google 결과도 정확하지 않음. (PDF 있는 href 태그만 찾아도 어려움)

date = 'AAAI2020'
txt_path = f'./examples/{date}.txt'

# if not os.path.isfile(txt_path):
#     titles = get_titles_for_aaai(f'./data/{date}.pdf')

#     with open(txt_path, 'w', encoding='utf-8') as f:
#         for title in titles:
#             f.write(title + '\n')
# else:
#     with open(txt_path, 'r', encoding='utf-8') as f:
#         titles = [title.strip() for title in f.readlines()]

titles = get_titles_for_aaai(f'./data/{date}.pdf')

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
        print(result.title)
        print(result.pdf_url)
        print(result.summary.replace('\n', ''))
        print()
    else:
        # print('ERROR : \"{}\"'.format(title))
        error_count += 1

        # input()

print(length, error_count)