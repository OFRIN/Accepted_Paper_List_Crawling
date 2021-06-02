# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

import argparse
import urllib.request

def download_file_using_url(url, file_path):
    urllib.request.urlretrieve(url, file_path)

def boolean(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
    
class Parser:
    def __init__(self):
        self.parser = argparse.ArgumentParser()

    def add(self, tag, default, type):
        if type == bool:
            type = boolean
        
        self.parser.add_argument(f'--{tag}', default=default, type=type)

    def add_from_list(self, dataset):
        for data in dataset:
            self.add(*data)

    def add_from_dict(self, dataset):
        for tag in dataset.keys():
            default = dataset[tag]['default']
            type = dataset[tag]['type']

            self.add(tag, default, type)
    
    def get_args(self):
        return self.parser.parse_args()
