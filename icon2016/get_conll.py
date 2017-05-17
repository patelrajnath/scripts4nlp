#!/usr/bin/python

import sys, re, codecs

textfname = sys.argv[1]
langfname = sys.argv[2]
tagsfname = sys.argv[3]

ftext = codecs.open(textfname, 'r', 'utf-8')
flang = codecs.open(langfname, 'r', 'utf-8')
ftags = codecs.open(tagsfname, 'r', 'utf-8')

fout = codecs.open(textfname+ '.conll', 'w', 'utf-8')

for l1, l2, l3 in zip(ftext, flang, ftags):
	words = l1.strip().split()
	langs = l2.strip().split()
	tags = l3.strip().split()
	for word, lang, tag in zip(words, langs, tags):
		fout.write(word + '\t' + lang + '\t' + tag + '\n')
	fout.write('\n')

ftext.close()
flang.close()
ftags.close()
fout.close()
