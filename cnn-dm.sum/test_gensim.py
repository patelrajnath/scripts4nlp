#!/usr/bin/env python

from gensim import corpora, models, similarities
from pprint import pprint  # pretty-printer
from collections import defaultdict

documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

print documents

stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

# remove words that appear only once
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1]
         for text in texts]

pprint(texts)
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict')  # store the dictionary, for future reference
print(dictionary)

corpus = [dictionary.doc2bow(text) for text in texts]
print corpus

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

print tfidf
corpus_tfidf = tfidf[corpus]

d = {dictionary.get(id): value for doc in corpus_tfidf for id, value in doc}

for key in d:
	print key, d[key]
