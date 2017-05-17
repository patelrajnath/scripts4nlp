#!/usr/bin/env python

import sys, re, codecs
import glob, os

#hyp_path = 'combined_test/system/mead/'
#ref_path = 'combined_test/model/'

hyp_path = 'cnn/system/hrnn/'
ref_path = 'cnn/model/'

#hyp_path = 'cnn/model/'
#ref_path = 'cnn/model/'

#hyp_path = 'dailymail/system/lead/lead3/500/'
#ref_path = 'dailymail/model/500/'

hyp_list = glob.glob(hyp_path + '*')
ref_list = glob.glob(ref_path + '*')

start = '<ROUGE-EVAL version="1.0">'
end = '</ROUGE-EVAL>'


count = 0
c = 0
fout = codecs.open('cnn_hrnn_spl.xml', 'w', 'utf-8')
fout.write(start+ '\n')
for ref, hyp in zip(sorted(ref_list), sorted(hyp_list)):
	ref = os.path.basename(ref)
	hyp = os.path.basename(hyp)
	ID = str(count).zfill(5)
	hyp_ID =  str(c).zfill(5)
	ref_ID =  'A' + str(c).zfill(5)
	eval_start = '<EVAL ID="' + ID + '">\n'
	peer_root = '<PEER-ROOT>\n' + hyp_path + '\n</PEER-ROOT>\n'
	model_root = '<MODEL-ROOT>\n' + ref_path + '\n</MODEL-ROOT>\n'
	inp_format = '<INPUT-FORMAT TYPE="SPL">\n</INPUT-FORMAT>\n'
	peer = '<PEERS>\n<P ID="' + hyp_ID + '">' + hyp +'</P>\n</PEERS>\n'
	model = '<MODELS>\n<M ID="' + ref_ID + '">' + ref + '</M>\n</MODELS>\n'
	eval_end = '</EVAL>'
	doc = eval_start + peer_root + model_root + inp_format + peer + model + eval_end
	fout.write(doc + '\n')
	count += 1
	#if count == 5:
	#	break

fout.write(end)
fout.close()

