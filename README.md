# Motivation
Most researchers read papers to find new ideas or develop new algorithms. For example, I should spend the time on searching articles about weakly-supervised semantic segmentation. Specifically, I divided the searching procedures into three steps. 

1. Seek the papers online. (ex. Google Scholar)
2. Make the list of papers.
3. Read the abstract of a paper to decide which one to be studied.

Therefore, I developed the crawler to automatically create the list in line with keywords . I defined four principal parts which are title, abstract, tables, and figures. 

In the next section, I am going to explain the details of the crawler. 

<br>

# Overview

![Overview](./resource/Crawler_For_Searching_Papers-Overview.png)

Step 1. Type essential and additional keywords to the crawler.

Step 2. Transfer keywords the user chose into DB.

Step 3. Return the papers associated with the keywords. 

Step 4. Make the table of the papers from DB. 

Step 5. Export as a PDF file from the table. 

<br>

# Installation

### 1. PIP 
```bash
pip install requests
pip install bs4

pip install arxiv
pip install doi2bib
pip install bibcure

pip install fpdf
pip install pdfplumber

pip install refextract

pip uninstall python-magic
pip install python-magic-bin==0.4.14
```

### 2. Requirements
```bash
pip install -r requirements.txt
```

# Usage
```bash
# for weakly supervised learning
python make_report.py --essential_keywords weakly --additional_keywords segmentation,detection,localization --pdf_path ./results/Weakly_Supervised_Learning.pdf

# for semi-supervised learning
python make_report.py --essential_keywords semi --additional_keywords segmentation,detection,localization --pdf_path ./results/Semi_Supervised_Learning.pdf

# for data augmentation
python make_report.py --essential_keywords data,augmentation --pdf_path ./results/DataAugmentation.pdf

# for Refinements
python make_report.py --essential_keywords refine,semantic,segmentation --pdf_path ./results/Refinements_For_Semantic_Segmentation.pdf

# for semi-supervised learning of semantic segmentation
python make_report.py --essential_keywords semi,semantic,segmentation --pdf_path ./results/Semi_Supervised_Learning_For_Semantic_Segmentation.pdf

# for CRF of semantic segmentation
python make_report.py --essential_keywords crf,semantic,segmentation --pdf_path ./results/CRF_For_Semantic_Segmentation.pdf
```

# Available Conference List
- [x] CVPR 2017
- [x] CVPR 2018
- [x] CVPR 2019
- [x] CVPR 2020
- [x] CVPR 2021

- [x] ICCV 2017
- [x] ICCV 2019
- [ ] ICCV 2021

- [x] WACV 2020
- [x] WACV 2021

- [x] ECCV 2018
- [x] ECCV 2020

- [x] NIPS 2017
- [x] NIPS 2018
- [x] NIPS 2019
- [x] NIPS 2020
- [ ] NIPS 2021

- [ ] ICML 2017
- [ ] ICML 2018
- [ ] ICML 2019
- [ ] ICML 2020
- [ ] ICML 2021

- [x] ICLR 2018
- [x] ICLR 2019
- [x] ICLR 2020
- [x] ICLR 2021 

- [ ] AAAI 2017
- [ ] AAAI 2018
- [x] AAAI 2019
- [x] AAAI 2020
- [x] AAAI 2021

# TODO List
- [X] Crawl title, abstract, bibtex and pdf_url per a conference.
- [x] Search the papers using the keywords which the user typed. 
- [ ] Add figures and tables in the PDF.
- [ ] Add GUI
- [ ] Provide the other formats. (XLSX, Markdown)
- [ ] Make word cloud using title and abstract.
- [ ] Show figure, abstract, and title per a paper. 
- [ ] Make docker file.

# Reference
- https://github.com/hoya012/CVPR-2021-Paper-Statistics
- https://scholarly.readthedocs.io/en/latest/quickstart.html#example
- https://github.com/titipata/scipdf_parser
- https://github.com/evanzd/ICLR2021-OpenReviewData