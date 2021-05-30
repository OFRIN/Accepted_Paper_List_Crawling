import arxiv

# https://pypi.org/project/arxiv/
search = arxiv.Search("Inferring Super-Resolution Depth from a Moving Light-Source Enhanced RGB-D Sensor: A Variational Approach", max_results=1)

for search in search.get():
    print(search.title)
    print(search.pdf_url)
    print(search.summary.replace('\n', ''))
    # search.download_pdf(dirpath="./data/", filename="test.pdf")
    break
