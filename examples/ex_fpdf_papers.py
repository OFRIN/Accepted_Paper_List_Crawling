import json

from fpdf import FPDF

def read_json(filepath, encoding=None):
    with open(filepath, 'r', encoding=encoding) as f:
        data = json.load(f)
    return data

class PDF(FPDF):
    def __init__(self, papers):
        super().__init__()

        self.paper_index = 0
        self.papers = papers

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def write_title(self):
        self.set_font('Arial', '', 12)
        self.set_fill_color(200, 220, 255)

        self.cell(0, 6, self.papers[self.paper_index]['title'], 0, 1, 'L', 1)
        self.ln(4)
    
    def write_abstract(self):
        if self.papers[self.paper_index]['abstract'] != '':
            self.set_font('Arial', '', 10)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['abstract'])

            # Line break
            self.ln()

    def write_bibtex(self):
        if self.papers[self.paper_index]['bibtex'] != '':
            self.set_font('Arial', '', 8)
            self.set_fill_color(200, 200, 200)

            # Output justified text
            self.multi_cell(0, 5, self.papers[self.paper_index]['bibtex'], fill=1)

            # Line break
            self.ln()

    def write_pdf_url(self):
        # Mention in italics
        self.set_font('', 'I', 8)
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
            if self.paper_index >= 5:
                break

data_dict = read_json('./data/CVPR2017.json')

pdf = PDF(data_dict)
pdf.update()
pdf.output('./examples/tuto_papers.pdf', 'F')