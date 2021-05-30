import requests
from bs4 import BeautifulSoup

def get_soup(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')
    return soup

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

main_url = 'https://www.ecva.net/'

soup = get_soup(main_url + 'papers.php')
papers = soup.find_all("dt", {"class":"ptitle"})

for paper in papers:
    sub_url = main_url + paper.find('a').get('href')
    soup_per_paper = get_soup(sub_url)

    title = soup_per_paper.find("div", {"id": "papertitle"}).text
    abstract = soup_per_paper.find("div", {"id": "abstract"}).text
    bibtex = None
    pdf_url = main_url + soup_per_paper.select_one('#content > dl > dd > a').get('href')[12:]

    title = remove_wrong_keyword(title)
    abstract = remove_wrong_keyword(abstract)
    
    print()
    print(sub_url)
    print(title)
    print(abstract)
    print(bibtex)
    print(pdf_url)
    input()
