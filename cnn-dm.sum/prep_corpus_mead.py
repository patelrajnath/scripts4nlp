#!/usr/bin/env

import glob
import sys, re, codecs, os
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
				if splits[0] != '':
					_text.append(splits[0].strip())
					#if len(splits) == 2 and splits[1] == '1':
					#	_sum.append(splits[0].strip())
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
	return _text, _sum

def _get_emap_and_text(lines):
	e2w = {}
	text = []
	summary = []
	for line in lines:
		#if len(line.strip().split()) == 1:
		words = line.split(':')
		if len(words) == 2:
			e2w[words[0].strip()] = words[1].strip()
		else:
			splits = line.strip().split('\t\t\t')
			if splits[0] != '':
				text.append(' '.join(splits[0].strip().split()))
				#if len(splits) == 2 and (splits[1] == '1' or splits[1] == '2'):
				if len(splits) == 2 and splits[1] == '1':
					summary.append(' '.join(splits[0].strip().split()))
	
	return e2w, text, summary

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

def _clean(doc, e2w, _lower=0):
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
		#c_sent = _translate(' '.join(sent))
		c_sent = ' '.join(sent)
		#c_sent = _upcase_first_letter(c_sent.strip()+ ' .')
		if _lower == 1:
			c_sent = c_sent.lower()

		c_text.append(c_sent)
	return c_text

def _write_text(_dir, text):
	f_out = codecs.open(_dir, 'w', 'utf-8')
	f_out.write("\n".join(text))

def _lead_nwords(text, n):
	_sum = []
	count = 0
	for line in text:
		words = line.strip().split()
		sent = []
		for word in words:
			count += 1
			sent.append(word.strip())
			if count == n:
				break
		_sum.append(' '.join(sent))
		if count == n:
			break
	return _sum
			
def _lead_nsent(text, n):
	_sum = []
	count = 0
	for line in text:
		count += 1
		_sum.append(line.strip())
		if count == n:
			break
	return _sum

def _main(dir_name):

	file_list = glob.glob(dir_name+'/*.summary.final')
	text_dir = dir_name+'/clean/text/'
	sum_dir = dir_name+'/clean/summary/model/'
	lead_sum_dir = dir_name+'/clean/summary/system/lead/'

	try:
		os.makedirs(sum_dir)
		os.makedirs(text_dir)
		os.makedirs(lead_sum_dir)
	except OSError as e:
    		if e.errno == 17:  # errno.EEXIST
        		os.chmod(text_dir, 0755)
        		os.chmod(sum_dir, 0755)
        		os.chmod(lead_sum_dir, 0755)

	log = codecs.open(text_dir + '/flog.txt', 'w', 'utf-8')

	c = 0
	n = len(file_list)
	empty = 0
	for f in sorted(file_list):
		print 'Processing file no', c+1, 'in', n
		new_f = 'd0' + str(c).zfill(5)
		#sum_f = 'ref' + str(c).zfill(5)
		sum_f = 'ref' + str(c).zfill(5) + '.spl'
		sum_l3 = 'lead3.' + str(c).zfill(5) + '.spl'
		sum_l100w = 'lead100w.' + str(c).zfill(5) + '.spl'
		log.write(new_f+'\n')

		orig_text_dir = text_dir + 'orig/'
		data_dir = text_dir + new_f + '/'
		docsent_dir = data_dir + 'docsent/'

		try:
			os.makedirs(data_dir)
			os.makedirs(docsent_dir)
			os.makedirs(orig_text_dir)
		except OSError as e:
    			if e.errno == 17:  # errno.EEXIST
				os.chmod(data_dir, 0755)
				os.chmod(docsent_dir, 0755)
				os.chmod(orig_text_dir, 0755)
		cluster_text = "<?xml version='1.0'?>\n<CLUSTER LANG='ENG'>\n <D DID='"+ new_f +"'/>\n</CLUSTER>\n"
		codecs.open(data_dir + new_f +'.cluster', 'w', 'utf-8').write(cluster_text)

		lines = []
		try:
			lines = codecs.open(f, 'r', 'utf-8').readlines()
		except Exception:
			pass
		lines = lines[2:]

		#e2w, _text, _sum = _get_emap_and_text(lines)
		c_text, c_sum = _get_text(lines)

		#This will remove the empty files in the process
		if len(c_text) == 0:
			empty += 1
			continue

		#c_text =  _clean(_text, e2w, _lower=1)
		#c_sum =  _clean(_sum, e2w, _lower=1)

		lead_sum =  _lead_nsent(c_text, 3)
		lead_sum_w =  _lead_nwords(c_text, 100)

		mead_text = _clean2(c_text)

		_write_text(orig_text_dir + new_f, c_text)
		_write_text(docsent_dir + new_f, mead_text)
		_write_text(sum_dir + sum_f, c_sum)
		_write_text(lead_sum_dir + sum_l3, lead_sum)
		_write_text(lead_sum_dir + sum_l100w, lead_sum_w)

		var = docsent_dir + new_f
		perl_script='/home/raj/smt/article_translation/mead/bin/addons/formatting/text2cluster.pl'
		subprocess.Popen(['perl', perl_script, var])

		c += 1
		#if c == 10:
		#	break

	print 'No of empty files removed', empty, ' in ', n

if __name__ == '__main__':
	_main(sys.argv[1])		
