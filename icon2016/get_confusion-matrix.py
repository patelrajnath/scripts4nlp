#!/usr/bin/python

'''

Creted by Raj Nath Patel, 27nd sept, 2016
Purpose: Get the tag confussion with word and sentences

Usage: python get_confusion-matrix.py test.tags ref.tags text

'''
from __future__ import division
import sys, re, codecs

if len(sys.argv) != 4:
	print 'Usage: python',  sys.argv[0], 'test.tags', 'ref.tags', 'text'
	exit()

test = sys.argv[1]
ref = sys.argv[2]
text = sys.argv[3]


fin_test = codecs.open(test, 'r', 'utf-8')
fin_ref = codecs.open(ref, 'r', 'utf-8')
fin_text = codecs.open(text, 'r', 'utf-8')

d = {}
target_tags = ['G_X', 'G_V', 'G_N', 'G_J']
for test, ref, text in zip(fin_test, fin_ref, fin_text):
	tags_t = test.split()
	tags_r = ref.split()
	words = text.split()
	for t, r, w in zip(tags_t, tags_r, words):
		if r in target_tags:
		  t = t.strip()
		  r = r.strip()
		  w = w.strip()
		  if r != t:
			text = text.strip()
			if text not in d:
				d[text.strip()] = r +'&&'+ t + '&&' + w +' '
			else:	
				d[text.strip()] += r +'&&'+ t + '&&' + w +' '

for key in d.keys():
	words = d[key].strip().split()
	for word in words:
		tmp = word.split('&&')
		print tmp[0]+';'+ tmp[1] +';'+ tmp[2] +';' + key 
