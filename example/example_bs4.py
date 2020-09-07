import requests
from bs4 import BeautifulSoup

main_url = 'https://openaccess.thecvf.com/'
req = requests.get(main_url + 'CVPR2020?day=2020-06-16')

html = req.text
soup = BeautifulSoup(html, 'html.parser')

soup.get_pretty

papers = soup.select(
    'dt > a'
)

for paper in papers[:5]:
    pdf_url = main_url + paper.get('href')
    pdf_url = pdf_url.replace('.html', '.pdf')
    pdf_url = pdf_url.replace('/html/', '/papers/')
    
    print(paper.text)
    print(pdf_url)

    print()
