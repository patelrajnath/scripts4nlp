#!/usr/bin/env

import gensim, glob
import sys, re, codecs, string

'''
Read all the files from the dir and add in a touple
'''

def _translate(to_translate, translate_to=u''):
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)

def _read_dir(dir_name):
	documents = []
	file_list = glob.glob(dir_name+'/*.summary')
	for f in file_list:
		text = ""
		lines = codecs.open(f, 'r', 'utf-8').readlines()
		for line in lines:
			text += _translate(line.strip())
		documents.append(text)
	return documents

if __name__ == '__main__':
	documents = _read_dir(sys.argv[1])
	print documents
