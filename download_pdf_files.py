import os

from excel import XLSX_Reader 
from utils import download_file_from_url

# excel_path = './data/Anomaly_Detection.xlsx'
# excel_elements = ['Title', 'Link']

# root_dir = './papers/'
# save_dir = './papers/' + os.path.basename(excel_path).replace('.xlsx', '')

# reader = XLSX_Reader(excel_path, excel_elements)

# for name, pdf_link in reader.dataset:
#     if ':' in name:
#         name = name.replace(':', ';')

#     path = save_dir + name + '.pdf'

#     if not os.path.isfile(path):
#         try:
#             download_file_from_url(pdf_link, path)  
#         except:
#             print(name)

excel_path = './data/CVPR2020.xlsx'
excel_elements = ['Index', 'Name', 'Link']

root_dir = './papers/'
save_dir = './papers/' + os.path.basename(excel_path).replace('.xlsx', '') + '/'

if not os.path.isdir(save_dir):
    os.makedirs(save_dir)

reader = XLSX_Reader(excel_path, excel_elements)

for index, name, pdf_link in reader.dataset:
    if ':' in name:
        name = name.replace(':', ';')
    
    if '?' in name:
        name = name.replace('?', '')

    if '/' in name:
        name = name.replace('/', ' ')

    if '!' in name:
        name = name.replace('!', '')

    if '\"' in name:
        name = name.replace('\"', '')

    if ' ' in name:
        name = name.replace(' ', '_')

    path = save_dir + '{:04d}_'.format(index) + name.replace(' ', '_') + '.pdf'
    if os.path.isfile(path):
        continue
    
    if not os.path.isfile(path):
        try:
            download_file_from_url(pdf_link, path)  
        except:
            print(name)