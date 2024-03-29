import nltk
import sys
import string


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
S -> NP Gen
Gen -> VP | VP NP PP | VP Conj NP VP Adv | VP Conj VP | VP NP PP F9 | VP PP PP | VP Conj NP VP
F9 -> Conj V NP PP
AP -> Adj | Adj AP 
NP -> N | Det N | AP NP | N PP | Det AP N | Det AP AP AP N
PP -> P NP
VP -> V | V NP | V PP | Adv V NP | V Adv
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
    tokenized_raw = nltk.tokenize.word_tokenize(sentence)
    preprocessed_cap = []
    for each in tokenized_raw:
        for letter in each:
            if letter in string.ascii_letters:
                preprocessed_cap.append(each)
                break
    preprocessed = [each.lower() for each in preprocessed_cap]
    return preprocessed


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = []
    for each in tree.subtrees():
        if each.label() == 'NP' and not "NP" in str(each[0:]):
            chunks.append(each)
    return chunks


if __name__ == "__main__":
    main()

