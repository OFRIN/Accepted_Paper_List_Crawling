import arxiv
import difflib

titles = [
    # "Multi-Domain Multi-Task Rehearsal for Lifelong Learning",
    # "EfficientDeRain: Learning Pixel-Wise Dilation Filtering for High-Efficiency Single-Image Deraining",
    # "Puzzle-CAM: Improved localization via matching partial and full features",
    # "Co-Grounding Networks with Semantic Attention for Referring Expression Comprehension in Videos",
    # "Co-Grounding Networks with Semantic Attention for Referring Expression Comprehension inVideos",
    # 'Skill‐guided Look‐ahead Exploration for Reinforcement Learning of Manipulation Policies ',
    'Bi-GCN: Binary Graph Convolutional Network'
]

for title in titles:
    # results = arxiv.Search(title, max_results=5).get()
    results = arxiv.Search(title).get()

    info = None
    
    for i, result in enumerate(results):
        low_title = title.lower()
        searched_title = result.title.lower()

        similarity = difflib.SequenceMatcher(None, low_title, searched_title).ratio()

        if similarity >= 0.90:
            info = result
            break
    
    if info is not None:
        print('# try = {}'.format(i + 1))
        print(info.title)
        print(info.pdf_url)
        print(info.summary.replace('\n', ''))
        print()
    else:
        print('ERROR : {}'.format(title))