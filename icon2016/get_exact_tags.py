#!/usr/bin/python

import sys, codecs, re

'''
Created by Raj Nath Patel, 26th Sept, 2016
Purpose: tag the words having exact ones,

Usage: python get_map_list.py Text.conll
'''
if len(sys.argv) != 2:
	print 'Usage: python', sys.argv[0], 'Text.conll'
	exit()

fname = sys.argv[1]
fin = codecs.open(fname, 'r', 'utf-8')
ftext1 = codecs.open(fname+'.text.raw', 'w', 'utf-8')
ftext = codecs.open(fname+'.text', 'w', 'utf-8')
ftags1 = codecs.open(fname+'.tags', 'w', 'utf-8')
ftags = codecs.open(fname+'.tags.pred', 'w', 'utf-8')
flang = codecs.open(fname+'.lang', 'w', 'utf-8')
flog = codecs.open(fname+'.log', 'w', 'utf-8')


smiley = "^[(>:;*8][a-zA-Z0-9',v(>:#;=*+[8|\-B/\\@<~^%$LXoO0}3Vb)]+$"
url = 'http'

text = ''
tags = ''
text_raw = ''
tags_raw = ''
langs = ''
d = {'@user':'', '#user':'', '@url':'', '@smiley':'', '@num':'', '@punct':''}
d_tags = {'@+':0, '#+':0, 'U+':0, 'E+':0, '$+':0, 'G_X+':0,'@-':0, '#-':0, 'U-':0, 'E-':0, '$-':0, 'G_X-':0}

for line in fin:
	if line.strip() == '':
		ftext.write(text.strip().lower()+ '\n')
		ftags.write(tags.strip()+ '\n')
		ftext1.write(text_raw.strip().lower()+ '\n')
		ftags1.write(tags_raw.strip()+ '\n')
		flang.write(langs.strip()+ '\n')
		if len(text.strip().split()) != len(tags.strip().split()):
			flog.write(text.strip() + '\t', + tags.strip() + '\n')
		text = ''
		tags = ''
		text_raw = ''
		tags_raw = ''
		langs = ''
	else:
		words = line.split('\t')
		word = words[0].strip()
		tag = words[2].strip()
		lang = words[1].strip()
		if re.search(r'\W', word):
			if re.search(r'^@', word):
				text += '@user '
				tags += '@ '
				d['@user'] += word + ' '
				if tag == '@':
					d_tags['@+'] +=1
				else:
					d_tags['@-'] +=1
					
			elif re.search(r'^#', word):
				text += '#user '
				tags += '# '
				d['#user'] += word + ' '
				if tag == '#':
					d_tags['#+'] +=1
				else:
					d_tags['#-'] +=1
			elif re.search(url, word):
				text += '@url '
				tags += 'U '
				d['@url'] += word + ' '
				if tag == 'U':
					d_tags['U+'] +=1
				else:
					d_tags['U-'] +=1
			elif re.search(smiley, word):
				text += '@smiley '
				tags += 'E '
				d['@smiley'] += word + ' '
				if tag == 'E':
					d_tags['E+'] +=1
				else:
					d_tags['E-'] +=1
			elif re.search(r'\d', word):
				text += '@num '
				tags += '$ '
				d['@num'] += word + ' '
				if tag == '$':
					d_tags['$+'] +=1
				else:
					d_tags['$-'] +=1
			else:
				if re.search(r'\w', word):
					d['@punct'] += word + ' '
					text += word + ' '
					tags += word + ' '
				else:
					text += '@punct '
					tags += 'G_X '
					d['@punct'] += word + ' '
					if tag == 'G_X':
						d_tags['G_X+'] +=1
					else:
						d_tags['G_X-'] +=1
		else:
			if re.search(r'\d', word):
				text += '@num '
				tags += '$ '
				d['@num'] += word + ' '
				if tag == '$':
					d_tags['$+'] +=1
				else:
					d_tags['$-'] +=1
			else:
				text += word +' '
				tags += word +' '
		langs += lang + ' '
		text_raw += word + ' '
		tags_raw += tag + ' '


for key in d.keys():
	flog.write(key + '\t' + d[key]+'\n\n')
for k in d_tags.keys():
	print k, d_tags[k]

fin.close()
ftext.close()
ftags.close()
flang.close()
flog.close()
