#!/usr/bin/python

import sys, re, codecs

'''
Created by Raj Nath, 27th Sept, 2016
Purpose: Get the word-list for given tag list 

Usage: python get_text_given-tag.py text_file tag_file

'''

if len(sys.argv) != 3:
	print 'Usage: python', sys.argv[0], 'text_file', 'tag_file'
	exit()

#Specify the tag-list below for which you want to generate the word list
target_tags = ['GJ', '$', 'G_SYM', 'CC']

ftext = codecs.open(sys.argv[1], 'r', 'utf-8')
ftags = codecs.open(sys.argv[2], 'r', 'utf-8')

d = {}
for l1, l2 in zip(ftext, ftags):
	words = l1.split()
	tags = l2.split()
	for tag, word in zip(tags, words):
		if tag in target_tags:
			if tag not in d:
				d[tag.strip()] = word + ' '
			else:
				d[tag.strip()] += word + ' '
				

for key in d.keys():
	print key, d[key].strip()
