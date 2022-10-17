""" 
    retriever - takes in dictionary.txt, postings.txt and docids.txt from indexer.py. It asks the users to insert a query and uses 'q' to exit the loop. 
    The underlying logic of this implementation is to take the 'query' input from the user, listed out the top 10 results with the docid, Title, line number and similarity score that is not 0.
    The similarity score was calculated using the inner product and then noramlized. 
 """

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import PorterStemmer
import re
import math

ldoc = '$DOC'
ltit = '$TITLE'
ltxt = '$TEXT'
qid = '$QRY'

stop_words = stopwords.words()


def someLinesPreprocess(txt):
    ps = PorterStemmer()

    sents = sent_tokenize(txt.replace('\n', ' ').lower())
    sents = [re.sub(r'[0-9]+', '', word) for word in sents];
    sents = [re.sub(r' +', ' ', word) for word in sents];

    ret = ''

    tokens = {}
    for sent in sents:  # Stop words removal and Stemming
        tokens = word_tokenize(sent)
        tokens = [ps.stem(word) for word in tokens if not word in stop_words
                  and not word in ',-:n\'t---.;```\'\'\'$)(][}{+=-#@!']

    return tokens


def preprocess(txt):
    tokens = txt.split()
    tokens = [str(x).strip().lower() for x in tokens]
    return tokens


def get_query_tf(query):
    tokens = someLinesPreprocess(query)
    #tokens = preprocess(query)
    tf = {}
    for token in tokens:
        if token not in tf.keys():
            tf[token] = 1
        else:
            tf[token] += 1
    return tf


def get_index(query_list, query):
    index = -1
    for q in query_list:
        index += 1
        if q[0] == query:
            break
    return index


def processQuery(dictionary, query_dict, postings, docs, N):
    similarity_score = {}
    size_posting = len(postings)
    for doc in docs.keys():
        d_score = 0
        q_score = 0
        for query in query_dict.keys():
            index = get_index(dictionary, query)
            if index != -1:
                if index == len(dictionary) - 1:
                    df_doc = size_posting - dictionary[len(dictionary) - 1][1]
                else:
                    df_doc = dictionary[index + 1][1] - dictionary[index][1]
                tf_query = query_dict[query]
                tf_doc = 0
                i = postings[dictionary[index][1]][1]
                while i <= (postings[dictionary[index][1]][1] + df_doc):
                    if postings[i][0] == doc:
                        tf_doc = postings[i][1]
                        break
                    i += 1
                d_score = tf_doc * math.log2(N/df_doc)
                q_score = tf_query * math.log2(N/df_doc)
                if doc not in similarity_score:
                    similarity_score[doc] = {"x": [d_score], "y": [q_score]}
                else:
                    similarity_score[doc]["x"].append(d_score)
                    similarity_score[doc]["y"].append(q_score)
    normalized_similarity_score = {}
    for key in similarity_score.keys():
        numerator = 0
        x_square_sum = 0
        y_square_sum = 0
        for i in range(len(similarity_score[key]["x"])):
            x_square_sum += similarity_score[key]["x"][i] ** 2
            y_square_sum += similarity_score[key]["y"][i] ** 2
            numerator += similarity_score[key]["x"][i] * similarity_score[key]["y"][i]
        denominator = x_square_sum * y_square_sum
        if denominator > 0:
            normalized_similarity_score[key] = float(numerator / math.sqrt(denominator))
        else:
            normalized_similarity_score[key] = 0.0

    result = dict(sorted(normalized_similarity_score.items(),
                         key=lambda item: item[1],
                         reverse=True))
    index = 0
    print("Top matched documents are:")
    for doc in result.keys():
        if index < 10:
            if result[doc] > 0:
                print("Document name: {} Title: {}  "
                      "LineNumber: {} Similarity Score: {}".format(docs[doc][0],
                                                                      docs[doc][1],
                                                                      doc, result[doc]))
        index += 1


def runOnlineProcessing(fnDict, fnPost, fnDocid):
    dictionary = []
    offset = 0
    postings = []
    with open(fnPost, 'r') as f:
        line = f.readline()
        while line:
            tokens = line.split()
            postings.append([int(tokens[0].strip()), int(tokens[1].strip())])
            line = f.readline()
        f.close()

    with open(fnDict, 'r') as f:
        line = f.readline()
        while line:
            tokens = line.split()
            stem = tokens[0].strip()
            df = int(tokens[1].strip())
            dictionary.append([stem, offset])
            offset += df
            line = f.readline()
        f.close()

    docs = {}
    N = 0
    with open(fnDocid, 'r') as f:
        line = f.readline()
        while line:
            tokens = line.split("  ")
            tokens = [x for x in tokens if x.strip() != ""]
            if len(tokens) >= 2:
                doc_id = tokens[0].strip()
                index = int(tokens[1].strip())
                doc_title = ''
                if len(tokens) >= 3:
                    doc_title = tokens[2].strip()
                docs[index] = [doc_id, doc_title]
                N += 1
            line = f.readline()
        f.close()

    while True:
        user_query = input("Enter your query: ")
        if user_query.lower() == "q":
            break
        query_dict = get_query_tf(user_query)
        processQuery(dictionary, query_dict, postings, docs, N)


if __name__ == "__main__":
    fninDict = "dictionary.txt"
    fninPost = "postings.txt"
    fninDocid = "docids.txt"

    runOnlineProcessing(fninDict, fninPost, fninDocid)
