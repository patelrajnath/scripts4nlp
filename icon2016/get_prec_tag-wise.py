#!/usr/bin/python

from __future__ import division
import sys, re, codecs
'''
Created by Raj Nath Patel, 27th Sept, 2016
Purpose: To get the tag-wise count+,- and precision

Usage: python get_prec_tag-wise.py test.tags ref.tags

'''
if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], 'test.tags', 'ref.tags'
	exit()

test = sys.argv[1]
ref = sys.argv[2]

fin_test = codecs.open(test, 'r', 'utf-8')
fin_ref = codecs.open(ref, 'r', 'utf-8')

d = {}
d_tags = {} 
for test, ref in zip(fin_test, fin_ref):
	tags_t = test.split()
	tags_r = ref.split()
	for t, r in zip(tags_t, tags_r):
		d_tags[r] = 0
		t = t.strip()
		r = r.strip()
		k = r+'+'
		if k not in d:
			d[k] = 0
		k = r+'-'
		if k not in d:
			d[k] = 0 

		if t == r:
			k = r+'+'
			d[k] += 1
		else:
			k = r+'-'
			d[k] += 1

#for key in d.keys():
#	print key, d[key]
for tag in d_tags.keys():
	print tag, d[tag+'+'], d[tag+'-'], d[tag+'+']/(d[tag+'-'] + d[tag+'+'])
