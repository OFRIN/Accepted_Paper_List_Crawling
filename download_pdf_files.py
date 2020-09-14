import os

from excel import XLSX_Reader 
from utils import download_file_from_url

save_dir = './papers/'
reader = XLSX_Reader('./data/Anomaly_Detection.xlsx', ['Title', 'Link'])

for name, pdf_link in reader.dataset:
    if ':' in name:
        name = name.replace(':', ';')

    path = save_dir + name + '.pdf'
    if not os.path.isfile(path):
        try:
            download_file_from_url(pdf_link, path)  
        except:
            print(name)

