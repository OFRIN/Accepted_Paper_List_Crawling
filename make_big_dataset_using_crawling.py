import os

from tools import io_utils
from tools import json_utils
from tools import crawling_utils

parser = io_utils.Parser()
parser.add('conference_names', 'CVPR2018', str)
parser.add('debug', True, bool)
args = parser.get_args()

crawler = crawling_utils.Crawler()
crawler.set_debug(args.debug)

data_dict = json_utils.read_json('./data/conference_info.json')

for name in args.conference_names.split(','):
    data_path = f'./data/{name}.json'
    if os.path.isfile(data_path):
        continue

    data = []
    """
    [
        {
            "title" : str,
            "abstract" : str,
            "pdf_url" : str,
            "bibtex" : str
        }
    ]
    """

    if crawler.debug:
        print('#' * 50)
        print(name)

    if data_dict[name]['type'] == 'cvf':
        main_url = data_dict[name]['url']
        days = data_dict[name]['days']
        
        if len(days) == 0:
            soup = crawler.get_soup(main_url + name)
            data += crawler.parse_for_cvf(soup, main_url)
        else:
            for day in days:
                soup = crawler.get_soup(main_url + name + '?day=' + day)
                data += crawler.parse_for_cvf(soup, main_url)

    elif data_dict[name]['type'] == 'eccv':
        main_url = data_dict[name]['url']

        soup = crawler.get_soup(main_url + 'papers.php')
        data += crawler.parse_for_eccv(soup, main_url)

    elif data_dict[name]['type'] == 'nips':
        pass

    elif data_dict[name]['type'] == 'aaai':
        pass
    
    # debug
    if crawler.debug:
        print(len(data))
        for _data in data[:5]:
            print('# Title : ' + _data['title'])
            print('# Abstract : ' + _data['abstract'])
            print('# PDF : ' + _data['pdf_url'])
            print('# Bibtex : ' + _data['bibtex'])
            print()
        input('#' * 50)

    json_utils.write_json(data_path, data, encoding='utf-8')