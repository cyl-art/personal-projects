import os

import nltk
import sys
import string
import math
FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    data = {}
    files = os.listdir(directory)
    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            content = f.read()
            data[file] = content
    return data


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized_raw = nltk.tokenize.word_tokenize(document.lower())
    final = []
    for each in tokenized_raw:
        if each not in string.punctuation and each not in nltk.corpus.stopwords.words("english"):
            final.append(each)
    return final


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idf = {}
    docs_num = len(documents)
    for doc in documents.keys():
        for word in documents[doc]:
            num = 0
            for each_key in documents.keys():
                if word in documents[each_key]:
                    num += 1
            idf[word] = math.log(docs_num/num, math.e)
    return idf


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_rank = {}
    for each_file in files:
        score = 0
        for query_word in query:
            tf = 0
            if query_word in files[each_file]:
                for word in files[each_file]:
                    if word == query_word:
                        tf += 1
            score += tf*idfs[query_word]
        file_rank[score] = each_file
    score_list = list(file_rank.keys())
    score_list.sort(reverse=True)
    file_list = []
    for i in range(n):
        file_list.append(file_rank[score_list[i]])
    return file_list


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_rank = {}
    for each_sentence in sentences:
        score = 0
        match_times = 0
        for query_word in query:
            if query_word in sentences[each_sentence]:
                match_times += 1
                score += idfs[query_word]
        sentence_rank[each_sentence] = {'mwm': score, 'qtd': match_times/len(sentences[each_sentence])}
    sentence_list = sorted(sentence_rank, key=lambda k: (sentence_rank[k]['mwm'], sentence_rank[k]['qtd']), reverse=True)
    return sentence_list[:n]


if __name__ == "__main__":
    main()

