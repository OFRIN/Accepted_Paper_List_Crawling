from fpdf import FPDF

import json

def read_json(filepath, encoding=None):
    with open(filepath, 'r', encoding=encoding) as f:
        data = json.load(f)
    return data

class PDF(FPDF):
    def __init__(self, data_dict):
        super().__init__()

    def update(self):
        for data in data_dict:
            pdf.cell(0, 10, data['title'], 0, 1)
            pdf.cell(0, 10, data['abstract'], 0, 1)
            
            break

    def header(self):
        # Logo
        # self.image('logo_pb.png', 10, 8, 33)

        # Arial bold 15
        self.set_font('Arial', 'B', 15)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'Title', 1, 0, 'C')
        # Line break
        self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

# Instantiation of inherited class
data_dict = read_json('./data/CVPR2017.json')

pdf = PDF(data_dict)
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_font('Times', '', 12)
pdf.update()
pdf.output('./examples/tuto2.pdf', 'F')