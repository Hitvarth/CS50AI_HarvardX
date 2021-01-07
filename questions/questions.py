import nltk
import sys

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
    import os
    mapping=dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory,file)) as f:
            mapping[file]=f.read()

    return mapping

    # raise NotImplementedError


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    import string
    document=document.lower()
    tokens=nltk.tokenize.word_tokenize(document)
    final_list=list()
    for token in tokens:
        if token in string.punctuation or token in nltk.corpus.stopwords.words("english"):
            continue
        else:
            final_list.append(token)

    return final_list

    # raise NotImplementedError


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    import math
    TotalDocs=len(documents)
    IDF=dict()
    for filename in documents:                #documents is a dictionary. iterated over keys
        for word in documents[filename]:
            DocHavingWord=len([filename for filename in documents if word in documents[filename]])
            IDF[word]=math.log(TotalDocs/DocHavingWord)

    return IDF

    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    def func(t):
        return t[1]

    tf_idfs=dict()
    for file in files:
        tf_idf=0
        for word in query:
            tf=0
            for item in files[file]:
                if item==word:
                    tf+=1
            tf_idf+=tf*idfs[word]
        tf_idfs[file]=tf_idf
    sorted_values=list(tf_idfs.items())
    sorted_values.sort(reverse=True,key=func)
    final_list=[t[0] for t in sorted_values]
    
    return final_list[:n]

    # raise NotImplementedError


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    def func(t):
        return t[1]

    # for calculating query term density
    def qtd(words_of_sentence):
        qtd=0
        for word in words_of_sentence:
            if word in query:
                qtd+=1
        return qtd/len(words_of_sentence)

    mwm=dict() # matching word measure
    for sentence in sentences:
        idf_sum=0
        for word in query:
            if word in sentences[sentence]:
                idf_sum+=idfs[word]
        mwm[sentence]=idf_sum

    ranked=list(mwm.items())
    ranked.sort(reverse=True,key=func)
    
    #solving a tie
    for i in range(len(ranked)-1):
        if ranked[i][1]==ranked[i+1][1]:
            if qtd(sentences[ranked[i+1][0]])>qtd(sentences[ranked[i][0]]):
                copy=ranked[i]
                ranked[i]=ranked[i+1]
                ranked[i+1]=copy
    
    #ranked is a list of tuples of the form (sentence,matching word measure)
    final_ranked=[r[0] for r in ranked] #now it is a list of sentences

    return final_ranked[:n]

    # raise NotImplementedError


if __name__ == "__main__":
    main()
