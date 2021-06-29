# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import os
import sys

filepath = os.path.dirname(__file__)
filepath = os.path.abspath(filepath)

sys.path.append(os.path.dirname(filepath))

from tools import json_utils

dataset = json_utils.read_json('./data/conferences/ECCV.json', encoding='utf-8')

years = ['2018', '2020']
data_dict = {year:[] for year in years}

for data in dataset:
    for year in years:
        if year in data['pdf_url']:
            data_dict[year].append(data)

for year in years:
    print(year, len(data_dict[year]))
    json_utils.write_json(f'./data/conferences/ECCV{year}.json', data_dict[year], encoding='utf-8')