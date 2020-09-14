# Copyright (C) 2020 * Ltd. All rights reserved.
# author : Sanghyeon Jo <josanghyeokn@gmail.com>

import os
import glob

from crawling import get_soup
from excel import XLSX_Writer
from utils import download_file_from_url, read_json

# 1. Load json files
json_paths = sorted(glob.glob('./data/*.json'))
for json_index, json_path in enumerate(json_paths):
    print('{:02d}. {}'.format(json_index + 1, os.path.basename(json_path)))

json_index = int(input('Select index => ')) - 1
data = read_json(json_paths[json_index])

excel_path = './results/{}.xlsx'.format(data['name'])
links = data['links']

# 2. Crawling and merge dataset
writer = XLSX_Writer(excel_path, ['Index', 'Name', 'URL'])

for link in links:
    soup = get_soup(link)
    papers = soup.select('dt > a')
    
    for paper in papers:
        pdf_url = 'https://openaccess.thecvf.com/' + paper.get('href')
        pdf_url = pdf_url.replace('.html', '.pdf')
        pdf_url = pdf_url.replace('/html/', '/papers/')
        
        writer([writer.row_index - 1, paper.text, pdf_url])

writer.close()

