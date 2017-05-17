#!/usr/bin/env

import glob
import sys, re, codecs, os
import subprocess

def _translate(to_translate, translate_to=u''):
    not_letters_or_digits = u'!"#%\'()*+,-/.:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)
    return to_translate.translate(translate_table)

def _get_text(doc):

	"""
	For UnAnonymized Version of Text
	"""
	t_start='[SN]JPStoryTokenizedLabelled[SN]'
	t_end='[SN]StoryAnonymized[SN]'
	s_start = '[SN]JPHighlightsTokenized[SN]'
	s_end = '[SN]HighlightsAnonymized[SN]'

	"""
	For Anonymized Version of Text
	"""
	#t_start = '[SN]JPStoryAnonymizedLabelled[SN]'
	#t_end = '[SN]HighlightsOrg[SN]'
	#s_start = '[SN]JPHighlightsAnonymized[SN]'
	#s_end = '[SN]TitleTokenized[SN]'

	_text = []
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
		else:
			i += 1
	return _text

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


def _write_text(_dir, text, mod='w'):
	f_out = codecs.open(_dir, mod, 'utf-8')
	f_out.write("\n".join(text))

			
def _main(dir_name):

	file_list = glob.glob(dir_name+'/*.summary.final')

	text_dir = dir_name+'/clean/text/'
	try:
		os.makedirs(text_dir)
	except OSError as e:
    		if e.errno == 17:  # errno.EEXIST
			os.chmod(text_dir, 0755)

	log = codecs.open(text_dir + '/flog.txt', 'w', 'utf-8')
	c = 0
	n = len(file_list)
	empty = 0
	file_name = text_dir + '/complete_text.txt'
	for f in file_list:
		print 'Processing file no', c+1, 'in', n
		lines = []
		try:
			lines = codecs.open(f, 'r', 'utf-8').readlines()
		except Exception:
			pass
		lines = lines[2:]

		#e2w, _text, _sum = _get_emap_and_text(lines)
		_text = _get_text(lines)

		#This will remove the empty files in the process
		if len(_text) == 0:
			empty += 1
			continue

		#c_text =  _clean2(_text)
		_write_text(file_name, _text, mod='a')
		c += 1
		#if c == 10:
		#	break

	print 'No of empty files removed', empty, ' in ', n

if __name__ == '__main__':
	_main(sys.argv[1])		
