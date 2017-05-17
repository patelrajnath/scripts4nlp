#!/bin/env python

import shlex, subprocess
import sys, re, codecs 

path = sys.argv[1]
fin = codecs.open(path, 'r', 'utf-8')

data='/home/raj/smt/article_translation/cnn-dm-sideinfo-data/cnn/test/clean/'
#data='/home/raj/smt/article_translation/cnn-dm-sideinfo-data/dailymail/test/clean/'
out_dir = data + 'summary/system/mead/'
script = "perl bin/mead.pl -data_path " + data +"text/ "
count = 0
for line in fin:
	perl_script = script + line
	output = codecs.open(out_dir + line.strip() + ".mead.spl", 'w', 'utf-8')
	args = shlex.split(perl_script)
	subprocess.call(args, stdout=output)

	#if count == 10:
	#	break
	#count +=1 
