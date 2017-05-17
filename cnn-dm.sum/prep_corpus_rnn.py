#!/usr/bin/env python

"""
Createb by Raj Nath Patel, April 7 2017
Purpose: To clean and prepare data for cnn and dailymail corpora for summarization 

Usage: python scripts/prep_corpus_rnn.py neuralsum/cnn/

"""
import json
import glob, numpy 
from collections import OrderedDict
import sys, re, codecs, os, gzip, cPickle
import subprocess

def _translate(to_translate, translate_to=u''):
    not_letters_or_digits = u'!"#%\'()*+,-/.:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)

def _get_text(doc):

	"""
	Following is for UnAnonymized version
	"""
	t_start='[SN]JPStoryTokenizedLabelled[SN]'
	t_end='[SN]StoryAnonymized[SN]'
	s_start = '[SN]JPHighlightsTokenized[SN]'
	s_end = '[SN]HighlightsAnonymized[SN]'

	"""
	Following is for Anonymized version
	"""
	#t_start = '[SN]JPStoryAnonymizedLabelled[SN]'
	#t_end = '[SN]HighlightsOrg[SN]'
	#s_start = '[SN]JPHighlightsAnonymized[SN]'
	#s_end = '[SN]TitleTokenized[SN]'

	_text = []
	_sum = []
	y = []
	n = len(doc)
	i = 0
	while i < n:
		line = doc[i].strip()
		if line == t_start:
			while True:
				i += 1
				line = doc[i].strip()
				if line == t_end:
					break
				
				splits = line.strip().split('\t')
				if len(splits) == 2 and splits[0] != '':
					_text.append(splits[0].strip())
					if splits[1] == '1':
						y.append(1)
					else:
						y.append(0)
		if line == s_start:	
			while True:
				i += 1
				line = doc[i].strip()
				if line == s_end:
					break
				
				if line != '':
					_sum.append(line)
				
		else:
			i += 1
	return _text, _sum, y

def _get_emap_and_text(lines):
	e2w = {}
	text = []
	y = []
	for line in lines:
		#if len(line.strip().split()) == 1:
		words = line.split(':')
		if len(words) == 2:
			e2w[words[0].strip()] = words[1].strip()
		else:
			splits = line.strip().split('\t\t\t')
			if len(splits) ==  2 and splits[0].strip() != '' and splits[1].strip() != '':
				text.append(' '.join(splits[0].strip().split()))
				tag = splits[1].strip()
				if tag == '2':
					y.append(int(0))
				else:
					y.append(int(tag))
	return e2w, text, y

def _upcase_first_letter(s):
	regex = re.compile("[A-Za-z]") # find a alpha
	if regex.search(s):
		cs = regex.search(s).group()
		return s.replace(cs, cs.upper(), 1)
	else:
		return s

def _clean2(doc):
	c_text = []
	for s in doc:
		c_sent = _upcase_first_letter(s.strip()+ ' .')
		c_text.append(c_sent)
	return c_text

def _clean(doc, e2w):
	c_text = []
	for s in doc:
		sent = []
		words = s.split()
		for w in words:
			w = w.strip()
			if w in e2w:
				sent.append(e2w[w])
			else:
				sent.append(w)
		c_sent = _translate(' '.join(sent))
		c_sent = _upcase_first_letter(c_sent+ '.')
		c_text.append(c_sent)
	return c_text

def _write_text(_dir, text):
	f_out = codecs.open(_dir, 'w', 'utf-8')
	f_out.write("\n".join(text))

def word2index(lines, word2idx):
    data = []
    for line in lines:
        sent_idx = []
        words = line.split()
        for word in words:
            w = word.strip().lower()
            if w in word2idx:
                sent_idx.append(word2idx[w])
            else:
                sent_idx.append(word2idx['UNK'])
        data.append(sent_idx)

    return data

def process_file_list(file_list, word2idx):
	train = []
	n = len(file_list)
	c = 0
	empty = 0 
	for f in file_list:
                print 'Processing file no', c, 'in', n
		lines = []
		try:
                	lines = codecs.open(f, 'r', 'utf-8').readlines()
		except UnicodeDecodeError:
			pass
			
                lines = lines[2:]
                #e2w, c_text, y = _get_emap_and_text(lines)
                c_text, c_sum, y = _get_text(lines)

		#The following condition will remove the empty documents if any
		if len(c_text) == 0:
			empty += 1
			continue

                #c_text =  _clean(c_text, e2w)
                text_idx = word2index(c_text, word2idx)
                train.append([text_idx, y])
                c += 1

                #if c == 10:
                #        break
	return train, empty

def _main(dir_name):
	
	_dict = 'cnn-dm_dict'
	word2idx = json.load(open(_dict + '_wf5.json'))

	#'.summary' is the extension of the files in CNN and dailymail 
	file_list_train = glob.glob(dir_name+'training/*.summary.final')
	file_list_test = glob.glob(dir_name+'test/*.summary.final')
	file_list_valid = glob.glob(dir_name+'validation/*.summary.final')

	train, empty_train = process_file_list(file_list_train, word2idx)
	test, empty_test = process_file_list(file_list_test, word2idx)
	valid, empty_valid = process_file_list(file_list_valid, word2idx)
	print 'Empty documents', ' Train:', empty_train, ' Test:', empty_test, ' Valid:', empty_valid
	#print 'Empty documents', ' Test:', empty_test, ' Valid:', empty_valid
	
	dicts = {'word2idx': word2idx}

	#data = [train, test, valid, dicts]
	data = [test, valid, dicts]
	
	data_train = 'dm_train.pkl.gz'
    	fp = gzip.open(data_train,'wb')
       	cPickle.dump(data, fp)

if __name__ == '__main__':
	_main(sys.argv[1])		
