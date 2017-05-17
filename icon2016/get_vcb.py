#!/usr/bin/python

import sys, re, codecs

'''
Created by Raj Nath, 24th Sept 2016
Purpose: Get the vocab and vocab-size given the corpus

Usgae: python get_vcb.py text-file

'''
if len(sys.argv) !=2:
	print 'Usgae: python', sys.argv[0], 'text-file'
	exit()

fname = sys.argv[1]
fin = codecs.open(fname, 'r', 'utf-8')
d = {}

for line in fin:
	words = line.split()
	for word in words:
		if word not in d:
			d[word] = 1
		else:
			d[word] +=1

for key in d.keys():
	print key, d[key] 
print len(d)
