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


def get_vocab(filename):
    v = {}
    fin = codecs.open(filename, 'r', 'utf-8')
    for line in fin:
        words = line.split()
        for word in words:
            w = word.strip().lower()
            if w not in v:
                v[w] = 1
            else:
                v[w] += 1
    
    fin.close()
    return v

def vocab_with_frequency(vocab, f):
    v = {}
    for key in vocab.keys():
        if vocab[key] >= f:
            v[key] = vocab[key]
    return v

def vocab_with_size(vocab, size):
    v_mfw = []
    count = 1
    v = sorted(vocab, key = vocab.get, reverse = True)
    
    for w in v:
        if count <= size:
            v_mfw.append(w.strip())
            count += 1
    return v_mfw

def save_dict(word_freqs, filename):
  	words = word_freqs.keys()
        freqs = word_freqs.values()

        sorted_idx = numpy.argsort(freqs)
        sorted_words = [words[ii] for ii in sorted_idx[::-1]]

        worddict = OrderedDict()
        worddict['eos'] = 0
        worddict['UNK'] = 1
        for ii, ww in enumerate(sorted_words):
            worddict[ww] = ii+2

        with open('%s.json'%filename, 'wb') as f:
            json.dump(worddict, f, indent=2)
            #json.dump(worddict, f, indent=2, ensure_ascii=False)



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
        #For slot fitting
        #data.append(np.asarray(sent_idx))
        
        #For neural machine transaltion
        data.append(sent_idx)

    #sorted_data = sorted(data, key=len)
    #return sorted_data

    return data


def extract(text, ids):
	summary = []
	if len(text) == len(ids):
		for line, idx in zip(text, ids):
			if idx == 1:
				summary.append(line.strip())
		return summary
	else:
		return ['It is not', 'OK']

def extract_n_words(text, ids, n):
	summary = []
	count = 0
	if len(text) == len(ids):
		for line, idx in zip(text, ids):
			count += len(line.split())
			if count >= n:
				break
			if idx == 1:
				summary.append(line.strip())
		return summary
	else:
		return ['It is not', 'OK']

def process_file_list(dir_name, file_list, hyp_lines):
	c = 0
	w = 75
	n = len(file_list)
	empty = 0
	for f in sorted(file_list):
                print 'Processing file no', c, 'in', n
		lines = []
		try:
                	lines = codecs.open(f, 'r', 'utf-8').readlines()
		except UnicodeDecodeError:
			pass
			
                lines = lines[2:]
                c_text, c_sum, y = _get_text(lines)
		if len(c_text) == 0:
			empty += 1
			continue	
                #c_text =  _clean(c_text, e2w)
		pred_y = hyp_lines[c]
		pred_y = [int(s) for s in pred_y.split()]
		#summary_hyp = extract_n_words(c_text, pred_y, w)
		summary_hyp = extract(c_text, pred_y)
		summary_ref = extract(c_text, y)
		print f, pred_y, y
		try:	
			hyp_sum_dir = dir_name+'/clean/summary/system/hrnn/hyp' + str(c).zfill(5) + '.spl'
			ref_sum_dir = dir_name+'/clean/summary/system/hrnn/ref' + str(c).zfill(5) + '.spl'
			print hyp_sum_dir
			fout_hyp = codecs.open(hyp_sum_dir, 'w', 'utf-8')
			fout_ref = codecs.open(ref_sum_dir, 'w', 'utf-8')
			fout_hyp.write("\n".join(summary_hyp))
			#fout_ref.write("\n".join(summary_ref))
			fout_ref.write("\n".join(c_sum))

			fout_hyp.close()
			fout_ref.close()
		except Exception:
			pass
                c += 1
                #if c == 10:
                #        break
	print 'No of empty files:',  empty, ' in ', n
def _main(dir_name):
	
	#'.summary' is the extension of the files in CNN 
	file_list_test = glob.glob(dir_name+'test/*.summary.final')
	#file_list_valid = glob.glob(dir_name+'validation/*.summary')

	hyp_test = codecs.open('hrnn_out/dailymail/dm_best_test_hyp', 'r', 'utf-8').readlines()
	#hyp_valid = codecs.open('hrnn_out/best_valid_hyp', 'r', 'utf-8').readlines()

	test_summary = process_file_list(dir_name + 'test/', file_list_test, hyp_test)
	#valid_summary = process_file_list(dir_name + 'validation/', file_list_valid, hyp_valid)
	
if __name__ == '__main__':
	_main(sys.argv[1])		
