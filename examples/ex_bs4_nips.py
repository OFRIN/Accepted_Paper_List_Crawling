import urllib.request

import requests
from bs4 import BeautifulSoup

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
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

main_url = 'https://papers.nips.cc'
conference = '2019'

soup = get_soup(main_url + '/paper/' + conference)
papers = soup.select(
    'ul > li'
)

for paper in papers:
    sub_url = main_url + paper.find('a').get('href')
    if not 'hash' in sub_url:
        continue
    
    soup_per_paper = get_soup(sub_url)

    contents = soup_per_paper.find('div', {'class':'col'})

    title = contents.find('h4').text
    abstract = contents.find_all('p')[3].text

    tags = contents.find('div').find_all('a')

    bib_url = main_url + tags[1].get('href')
    bibtex = get_string_from_url(bib_url)

    for tag in tags[2:]:
        if 'Paper' in tag.text:
            pdf_url = main_url + tag.get('href')
            break

    bibtex = remove_wrong_keyword(bibtex)
    
    print()
    print(sub_url)
    print(title)
    print(abstract)
    print(bibtex)
    print(pdf_url)
    input()
