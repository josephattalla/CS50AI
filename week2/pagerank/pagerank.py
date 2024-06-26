import os
import random
import re
import sys
import numpy as np

# global variables for the damping rate and sample size
DAMPING = 0.85
SAMPLES = 10000


def main():
    
    # uses command line arguement to take in a folder with html files
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    
    # uses crawl function, which is later defined, to store
    # the html file as the key and value is the 
    # list of all other html files that link to that page
    corpus = crawl(sys.argv[1])

    # uses sample_pagerank algorithm, later defined, 
    # to get the estimated rank values from algorithm
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)

    # prints the results
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    # uses iterate_pagerank, later defined, to get true rank values from algorithm
    ranks = iterate_pagerank(corpus, DAMPING)

    # prints the results
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    print(np.sum(list(ranks.values())))


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
        pages[filename] = set( link for link in pages[filename] if link in pages )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    probability_dist = dict()

    # if the page has links
    if len(corpus[page]) > 0:
        # loop through the pages
        for page_ in corpus:
            # each page has a probability of 1-d/n
            probability = (1-damping_factor)/len(corpus)
            # if the iterated page is not the page currently on
            if page_ != page and page_ in corpus[page]:
                probability += damping_factor*(1/len(corpus[page]))
            probability_dist[page_] = probability
    else:
        for page_ in corpus:
            probability_dist[page_] = 1 / len(corpus)

    return probability_dist



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    rank = dict()
    # random choice for first page
    page = random.choice(list(corpus))
    # make the count of the current page 1
    rank[page] = 1
    # loop for the sampling
    for _ in range(n):
        # get the probability distribution of the current page
        probabilities = transition_model(corpus, page, damping_factor)
        # choose the next page using the probabilities as the weight
        page = random.choices(list(probabilities), weights=list(probabilities.values()), k=1)[0]
        # add 1 to the page that is chosen
        if page not in rank:
            rank[page] = 1
        else:
            rank[page] += 1
    # get the probabilities of the rank
    for page in rank:
        rank[page] /= n

    return rank
    

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # dictionary for the ranks
    rank = dict()
    # copy of corpus to use instead of the original, to not change the original
    corpus_ = corpus.copy()

    # setting the ranks to even probabilities for each page in the corpus
    for page in corpus_:
        rank[page] = 1 / len(corpus_)
        # if the page doesn't link to any others, have it link to every page
        if len(corpus_[page]) == 0:
            corpus_[page] = set(corpus_.keys())
    
    # setting variable to track the change in rank, arbitrarily setting to infinity
    change = np.inf

    # while the change is greater than 0.001 (threshold to stop)
    while change > 0.001:

        # dictionary to keep track of the change in rank of each page
        change_ = dict()

        # loop through pages
        for page in corpus_:

            # list of the pages that link to the currently indexed page
            pages_linked = [i for i in corpus_ if page in corpus_[i]]

            # the first part of the equation: (1-d)/N
            new_rank = (1-damping_factor)/len(corpus_)

            # adding the sum of the ranks of the pages that link to the current page, divided by the #
            # of links that page has, all times the damping factor
            new_rank += damping_factor*np.sum([rank[i]/len(corpus_[i]) for i in pages_linked])
            
            # calculate change in the current rank for the page and the new rank
            change_[page] = np.abs(rank[page] - new_rank)
            # set the rank of the page to the new rank
            rank[page] = new_rank
    
        # set the change variable to the max change
        change = max(list(change_.values()))

    return rank

        


if __name__ == "__main__":
    main()
