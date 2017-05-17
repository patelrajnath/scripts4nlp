#!/usr/bin/python

import sys, re, codecs

'''
Created by Raj Nath, 24th Sept 2016
Purpose: Created to get the text from the conll format file

Usage: python prep_test_data.py TEXT.conll


'''

if len(sys.argv) !=2:
	print 'Usage: python', sys.argv[0], 'TEXT.conll'
	exit()

fname = sys.argv[1]
fin = codecs.open(fname, 'r', 'utf-8')
fwords = codecs.open(fname+'.temp', 'w', 'utf-8')
#ftags = codecs.open(fname+'.tags', 'w', 'utf-8')
#pos = ''
text = ''
for line in fin:
	words = line.strip().split("\t")
	print words
	if line.strip() == "":
		print 'its empty line'
		if text.strip() != "":
			fwords.write(text.strip().lower() + '\n')
			#ftags.write(pos.strip() + '\n')
		#pos = ''
		text = ''
	else:
		#flag = re.search(r'\W', words[0].strip())
		#if flag:
		#	print line
		#else:
			text += words[0] + ' '
		#	pos += words[2] + ' '

fin.close()
fwords.close()
#ftags.close()
