import json
from tools import json_utils

dataset = json_utils.read_json('./data/ECCV.json', encoding='utf-8')

years = ['2018', '2020']
data_dict = {year:[] for year in years}

for data in dataset:
    for year in years:
        if year in data['pdf_url']:
            data_dict[year].append(data)

for year in years:
    print(year, len(data_dict[year]))
    json_utils.write_json(f'./data/ECCV{year}.json', data_dict[year], encoding='utf-8')