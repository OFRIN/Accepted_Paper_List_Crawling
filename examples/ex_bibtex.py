from doi2bib.crossref import get_bib_from_doi

# doi = '10.1038/s41524-017-0032-0'
doi = '10.1007/978-3-030-58452-8_1'
found, bib = get_bib_from_doi(doi)

print(found)
print(bib)