# Copyright (C) 2021 * Ltd. All rights reserved.
# author : Sanghyun Jo <josanghyeokn@gmail.com>

from fpdf import FPDF

from tools import io_utils
from tools.json_utils import read_json

parser = io_utils.Parser()
parser.add('essential_keywords', 'weakly', str)
parser.add('additional_keywords', '', str)

parser.add('years', '2021,2020,2019,2018,2017', str)

parser.add('pdf_path', '', str)
parser.add('font', 'Roboto', str)

args = parser.get_args()

class PDF(FPDF):
    def __init__(self, papers):
        super().__init__()

        self.paper_index = 0
        self.papers = papers

        self.font_name = 'Arial'

    def update_font(self, name):
        font_folder = f'./font/{name}/'

        font_dict = read_json(font_folder + 'summary.json')

        for key in font_dict.keys():
            self.add_font(name, key, font_folder + font_dict[key], uni=True)

        self.font_name = name

    def header(self):
        pass
        
    def footer(self):
        self.set_y(-15)

        self.set_font(self.font_name, 'I', 7)
        # self.set_font(self.font_name, '', 7)

        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def write_title(self):
        self.image(self.papers[self.paper_index]['logo'], x=10, y=8, h=20)
        self.ln(20)
        
        self.set_font(self.font_name, '', 10)
        self.set_fill_color(200, 220, 255)

        self.multi_cell(0, 8, self.papers[self.paper_index]['title'], fill=True)
        self.ln(4)
    
    def write_abstract(self):
        if self.papers[self.paper_index]['abstract'] != '':
            self.set_font(self.font_name, '', 8)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['abstract'])

            # Line break
            self.ln()

    def write_bibtex(self):
        if '{' in self.papers[self.paper_index]['bibtex']:
            self.set_font(self.font_name , '', 7)
            self.set_fill_color(200, 200, 200)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['bibtex'], fill=True)

            # Line break
            self.ln()

    def write_pdf_url(self):
        # Mention in italics
        self.set_font(self.font_name, 'I', 7)
        # self.set_font(self.font_name, '', 7)

        self.cell(0, 5, self.papers[self.paper_index]['pdf_url'])
        
        self.ln(4)

    def update(self):
        for paper in self.papers:
            # if self.paper_index % 2 == 0:
            self.add_page()

            self.write_title()
            self.write_abstract()
            self.write_bibtex()
            self.write_pdf_url()

            self.paper_index += 1
            # if self.paper_index >= 5:
            #     break

papers = []

years = args.years.split(',')

essential_keywords = args.essential_keywords.lower().split(',')
if args.additional_keywords != '':
    additional_keywords = args.additional_keywords.lower().split(',')
else:
    additional_keywords = None

print('# Essential Keywords :', essential_keywords)
print('# Addntional Keywords :', additional_keywords)

conference_names = [
    'CVPR2021', 'AAAI2021',             'WACV2021',             'ICLR2021',
    'CVPR2020', 'AAAI2020', 'NIPS2020', 'WACV2020',             'ICLR2020',  'ECCV2020',
    'CVPR2019', 'AAAI2019', 'NIPS2019',             'ICCV2019', 'ICLR2019',
    'CVPR2018',             'NIPS2018',                         'ICLR2018',  'ECCV2018',
    'CVPR2017',             'NIPS2017',             'ICCV2017', 
]

logo_dict = read_json('./data/logo_info.json')
count_dict = {name:0 for name in conference_names}

for name in conference_names:
    print(name)

    year = name[4:]
    if not year in years:
        continue

    for data in read_json('./data/conferences/{}.json'.format(name), encoding='utf-8'):
        # extract title and abstract
        title = data['title'].lower()
        abstract = data['abstract'].lower()

        # set the condition of essential keywords
        essential_count = 0
        for keyword in essential_keywords:
            if keyword in title or keyword in abstract:
                essential_count += 1

        essential_cond = essential_count >= len(essential_keywords)

        # set the condition of additional keywords
        if additional_keywords is not None:
            additional_count = 0
            for keyword in additional_keywords:
                if keyword in title or keyword in abstract:
                    additional_count += 1

            additional_cond = additional_count > 0
        else:
            additional_cond = True
        
        if essential_cond and additional_cond:
            count_dict[name] += 1
            data['logo'] = './resource/' + logo_dict[name]
            papers.append(data)

print('# Found papers : ({})'.format(len(papers)))
for name in conference_names:
    print(f'# {name} : {count_dict[name]}')
print()

if len(papers) > 0 and args.pdf_path != '':
    pdf = PDF(papers)
    pdf.update_font(args.font)
    pdf.update()
    pdf.output(args.pdf_path)

