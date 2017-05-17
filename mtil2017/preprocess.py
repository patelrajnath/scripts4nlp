#!/usr/bin/env python

import sys, re, codecs

fname = sys.argv[1]
SRC = sys.argv[2]
TGT = sys.argv[3]

fin = codecs.open(fname, 'r', 'utf-8')
fout_src = codecs.open(fname + '.' + SRC, 'w', 'utf-8')
fout_tgt = codecs.open(fname + '.' + TGT, 'w', 'utf-8')
log = codecs.open(SRC + '-' + TGT + '.log', 'w', 'utf-8')

for line in fin:
	sents = line.strip().split('@')
	if len(sents) ==  3:
		print sents[0]
		fout_src.write(sents[1].strip()+'\n')
		fout_tgt.write(sents[2].strip()+'\n')
	else:
		log.write(line)
