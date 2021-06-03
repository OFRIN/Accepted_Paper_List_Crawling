from refextract import extract_references_from_file
references = extract_references_from_file("./results/2103.14581v1.pdf")

print(len(references))
for ref in references:
    print(ref)