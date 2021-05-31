import arxiv

titles = [
    "Multi-Domain Multi-Task Rehearsal for Lifelong Learning",
    "EfficientDeRain: Learning Pixel-Wise Dilation Filtering for High-Efficiency Single-Image Deraining",
    "Puzzle-CAM: Improved localization via matching partial and full features",
    "Co-Grounding Networks with Semantic Attention for Referring Expression Comprehension in Videos"
]

for title in titles:
    results = arxiv.Search(title, max_results=5).get()

    info = None
    
    for result in results:
        if result.title.lower() == title.lower():
            info = result
            break
    
    if info is not None:
        print(result.title)
        print(result.pdf_url)
        print(result.summary.replace('\n', ''))
        print()
    else:
        print('ERROR : {}'.format(title))