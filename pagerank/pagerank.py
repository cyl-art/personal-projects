import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    trans_dict = dict()
    if len(corpus[page]) == 0:
        for key in corpus.keys():
            distrib = 1 / len(corpus.keys())
            trans_dict[key] = distrib
    else:
        for key in corpus.keys():
            basic = (1 - damping_factor) / len(corpus.keys())
            additional = damping_factor / len(corpus[page])
            if key in corpus[page]:
                distrib = basic + additional
                trans_dict[key] = distrib
            else:
                distrib = basic
                trans_dict[key] = distrib
    return trans_dict

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rankings = {}
    storage = []
    choice = random.choice(list(corpus.keys()))
    storage.append(choice)
    for i in range(n - 1):
        a = transition_model(corpus, choice, damping_factor)
        keys = list(corpus.keys())
        weights = [a[i] for i in keys]
        choice = random.choices(keys, weights, k=1)[0]
        storage.append(choice)
    for key in corpus.keys():
        number = storage.count(key) / len(storage)
        rankings[key] = number
    return rankings

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    old_dict = {}
    new_dict = {}
    N = len(corpus.keys())
    for key in corpus:
        old_dict[key] = 1 / N
    while True:
        for current_p in corpus:
            rank = 0
            for p_that_linked in corpus:
                if current_p in corpus[p_that_linked]:
                    rank = rank + old_dict[p_that_linked] / len(corpus[p_that_linked])
                if len(corpus[p_that_linked]) == 0:
                    rank = rank + old_dict[p_that_linked] / len(corpus)
            rank = rank * damping_factor
            rank = rank + (1 - damping_factor) / N
            new_dict[current_p] = rank
        change = max([abs(old_dict[x] - new_dict[x]) for x in old_dict])
        if change < 0.001:
            break
        else:
            old_dict = new_dict.copy()
    return old_dict


if __name__ == "__main__":
    main()

