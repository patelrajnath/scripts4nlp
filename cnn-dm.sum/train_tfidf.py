#!/usr/bin/env python

import re, codecs, sys
import glob
from gensim import corpora, models, similarities
from pprint import pprint  # pretty-printer
from collections import defaultdict

stoplist = set('for a of the and to in'.split())

data_dir = sys.argv[1]
file_list = glob.glob(data_dir+'/*')
documents = []
for f in file_list:
	print f
	lines = codecs.open(f, 'r', 'utf-').readlines()
	doc = []
	for line in lines:
		doc.append(line.strip())
	documents.append(' '.join(doc))

texts = [[word for word in document.split() if word not in stoplist] for document in documents]

#print texts
dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/cnn.dict')
corpus = [dictionary.doc2bow(text) for text in texts]

tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

corpus_tfidf = tfidf[corpus]

d = {dictionary.get(id): value for doc in corpus_tfidf for id, value in doc}
fout = codecs.open('cnn_tfidf.txt', 'w', 'utf-8')
for key in d:
        #print key, d[key]
	fout.write(key + '\t' + str(d[key]) + '\n')

