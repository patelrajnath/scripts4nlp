#!/usr/bin/env python

import sys, re, codecs
import glob

inp_path = sys.argv[1]
flag = sys.argv[2]
files_list = glob.glob(inp_path+'/*')
count = 0
prefix = ''
for f in sorted(files_list):
	print f
	fin = codecs.open(f, 'r', 'utf-8')
	if flag == '1':
		prefix = 'mead_hyp'
	if flag == '2':
		prefix = 'ref'
	fname_out = prefix + str(count).zfill(5) + '.spl'
	fout = codecs.open(inp_path + fname_out, 'w', 'utf-8')
	para = []
	for line in fin:
		if flag == '1':
			para.append((line.strip().split(' ', 1)[1]).lower())
		if flag == '2':
			para.append(line.strip())
	#print para
	fout.write(('\n'.join(para)).strip())
	#if count == 10:
	#	break
	count +=1
