import glob
from fpdf import FPDF

from tools import io_utils
from tools.json_utils import read_json

parser = io_utils.Parser()
parser.add('keywords', 'weakly,localization,segmentation,detection,panoptic', str)
parser.add('pdf_path', './data/WLSD.pdf', str)
parser.add('num_match', 2, int)
parser.add('font', 'DejaVuSans', str)
args = parser.get_args()

class PDF(FPDF):
    def __init__(self, papers):
        super().__init__()

        self.paper_index = 0
        self.papers = papers

        self.font_name = 'Arial'

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)

        # self.set_font(self.font_name, 'I', 8)
        self.set_font(self.font_name, '', 8)

        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def write_title(self):
        self.set_font(self.font_name, '', 12)
        self.set_fill_color(200, 220, 255)

        self.cell(0, 6, self.papers[self.paper_index]['title'], 0, 1, 'L', 1)
        self.ln(4)
    
    def write_abstract(self):
        if self.papers[self.paper_index]['abstract'] != '':
            self.set_font(self.font_name, '', 10)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['abstract'])

            # Line break
            self.ln()

    def write_bibtex(self):
        if '{' in self.papers[self.paper_index]['bibtex']:
            self.set_font(self.font_name , '', 8)
            self.set_fill_color(200, 200, 200)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['bibtex'], fill=1)

            # Line break
            self.ln()

    def write_pdf_url(self):
        # Mention in italics
        # self.set_font(self.font_name, 'I', 8)
        self.set_font(self.font_name, '', 8)
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
keywords = args.keywords.lower().split(',')

for name in [
    'CVPR2021', 'AAAI2021',             'WACV2021', 
    'CVPR2020', 'AAAI2020', 'NIPS2020', 'WACV2020',              'ECCV',
    'CVPR2019', 'AAAI2019', 'NIPS2019', 'ICCV2019', 'ICLR2019',
    'CVPR2018', 'AAAI2018', 'NIPS2018',             'ICLR2018']:

    if 'AAAI' in name:
        continue

    for data in read_json('./data/{}.json'.format(name), encoding='utf-8'):
        title = data['title'].lower()
        abstract = data['abstract'].lower()

        cond_title = sum([keyword in title for keyword in keywords])
        cond_abstract = sum([keyword in data['abstract'] for keyword in keywords])

        # print(title, cond_title, cond_abstract)

        if (cond_title + cond_abstract) >= args.num_match:
            papers.append(data)

print('# Found papers : ({})'.format(len(papers)))

pdf = PDF(papers)

pdf.add_font(args.font, '', f'./font/{args.font}.ttf', uni=True)
pdf.font_name = args.font

pdf.update()
pdf.output(args.pdf_path)