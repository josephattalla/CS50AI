import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """

S -> NP VP | VP | S Conj S | S P S

NP -> N | Det N | Det NP | P NP | Adj NP | Adv NP | Conj NP | N NP | N Adv

VP -> V | V NP | Adv VP | V Adv
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)


    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """

    # get tokens from sentence
    tokens = nltk.tokenize.word_tokenize(sentence)

    # loop through the words
    for idx, token in enumerate(tokens):
        
        # if there is no alphabetic values in the token, remove it
        if not any([i.isalpha() for i in token]):
            tokens.remove(token)
        
        # if there are capital letters in the token, make it lowercase
        if any([i.isupper() for i in token]):
            tokens[idx] = token.lower()
    
    return tokens


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    
    noun_phrases = []

    # loop through the subtrees
    for subtree in tree.subtrees():

        # if the label is a noun phrase and there are no noun phrases, other than itself, in the subtree's labels, then append to noun_phrases
        if subtree.label() == 'NP':
            if [i.label() for i in subtree.subtrees()].count('NP') == 1:
                noun_phrases.append(subtree)


    return noun_phrases


if __name__ == "__main__":
    main()
