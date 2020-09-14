# Copyright (C) 2020 * Ltd. All rights reserved.
# author : Sanghyeon Jo <josanghyeokn@gmail.com>

import json
import urllib

def download_file_from_url(url, save_path):
    urllib.request.urlretrieve(url, save_path) 

def read_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data