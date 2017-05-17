#!/usr/bin/python

import sys, codecs, re

'''
Created by Raj Nath Patel, 26th Sept, 2016
Purpose: To normalize the social media text for pos tagging task (conll format only), and get the text and tags in line by line

Usage: python get_map_list.py Text.conll
'''
if len(sys.argv) != 2:
	print 'Usage: python', sys.argv[0], 'Text.conll'
	exit()

fname = sys.argv[1]
fin = codecs.open(fname, 'r', 'utf-8')
ftext = codecs.open(fname+'.text', 'w', 'utf-8')
ftags = codecs.open(fname+'.tags', 'w', 'utf-8')
flang = codecs.open(fname+'.lang', 'w', 'utf-8')
flog = codecs.open(fname+'.log', 'w', 'utf-8')


smiley = "^[(>:;*8][a-zA-Z0-9',v(>:#;=*+[8|\-B/\\@<~^%$LXoO0}3Vb)]+$"
url = 'http'

text = ''
tags = ''
langs = ''
d = {'@user':'', '#user':'', '@url':'', '@smiley':'', '@num':'', '@punct':''}

for line in fin:
	if line.strip() == '':
		ftext.write(text.strip().lower()+ '\n')
		ftags.write(tags.strip()+ '\n')
		flang.write(langs.strip()+ '\n')
		text = ''
		tags = ''
		langs = ''
	else:
		words = line.split('\t')
		word = words[0].strip()
		tag = words[2].strip()
		lang = words[1].strip()
		if re.search(r'\W', word):
			if re.search(r'^@', word):
				text += '@user '
				d['@user'] += word + ' '
			elif re.search(r'^#', word):
				text += '@user '
				d['#user'] += word + ' '
			elif re.search(url, word):
				text += '@url '
				d['@url'] += word + ' '
			elif re.search(smiley, word):
				text += '@smiley '
				d['@smiley'] += word + ' '
			elif re.search(r'\d', word):
				text += '@num '
				d['@num'] += word + ' '
			else:
				if re.search(r'\w', word):
					d['@punct'] += word + ' '
					text += word + ' '
				else:
					text += '@punct '
					d['@punct'] += word + ' '
		else:
			if re.search(r'\d', word):
				text += '@num' +' '
				d['@num'] += word + ' '
			else:
				text += word +' '
		tags += tag + ' '
		langs += lang + ' '


for key in d.keys():
	flog.write(key + '\t' + d[key]+'\n\n')
fin.close()
ftext.close()
ftags.close()
flang.close()
flog.close()
