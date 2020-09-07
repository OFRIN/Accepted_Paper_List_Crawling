
import os
import urllib
import requests

from bs4 import BeautifulSoup

def csv_print(data_list, log_path = './log.csv'):
    string = ''
    for data in data_list:
        if type(data) != type(str):
            data = str(data)
        string += (data + ',')
    
    if log_path is not None:
        f = open(log_path, 'a+')
        f.write(string + '\n')
        f.close()

def download_file_from_url(url, save_path):
    urllib.request.urlretrieve(url, save_path) 

main_url = 'https://openaccess.thecvf.com/'

conference_url = input('# Conference URL ? ')
conference_name = conference_url.replace(main_url, '')[:8]

csv_path = conference_name + '.csv'
if not os.path.isfile(csv_path):
    csv_print(['Name', 'URL'], csv_path)

req = requests.get(conference_url)

html = req.text
soup = BeautifulSoup(html, 'html.parser')

soup.get_pretty

papers = soup.select(
    'dt > a'
)

for index, paper in enumerate(papers):
    pdf_url = main_url + paper.get('href')
    pdf_url = pdf_url.replace('.html', '.pdf')
    pdf_url = pdf_url.replace('/html/', '/papers/')

    csv_print([paper.text, pdf_url], csv_path)
    
    # pdf_path = save_dir + os.path.basename(pdf_url)
    # download_file_from_url(pdf_url, pdf_path)
