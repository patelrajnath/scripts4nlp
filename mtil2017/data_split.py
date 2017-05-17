#!/usr/bin/env python

import os
import sys
import random 
import re
import numpy as np
import codecs 

from random import shuffle

src = sys.argv[1]
tgt = sys.argv[2]

src_file = os.path.basename(src)
tgt_file = os.path.basename(tgt)

src_name = os.path.splitext(src_file)[0]
tgt_name = os.path.splitext(tgt_file)[0]

src_ext = os.path.splitext(src_file)[1][1:]
tgt_ext = os.path.splitext(tgt_file)[1][1:]

dir_name = src_ext + '-' + tgt_ext

dir_train = dir_name + '/train'
dir_test = dir_name + '/test'
dir_tunning = dir_name + '/tunning'

try:
	os.mkdir(dir_name)
	os.mkdir(dir_train)
	os.mkdir(dir_test)
	os.mkdir(dir_tunning)
except OSError as e:
	if  e.errno == 17:
		os.chmod(dir_train, 0775)
		os.chmod(dir_test, 0775)
		os.chmod(dir_tunning, 0775)

df_src = codecs.open(src, 'r', 'utf-8').readlines()
df_tgt = codecs.open(tgt, 'r', 'utf-8').readlines()

n = len(df_src) #number of rows in your dataset
indices = range(n)
shuffle(indices)

test_indices = indices[:500]
tunning_indices = indices[500:1000]
train_indices =  indices[1000:]

test_src = []
test_tgt = []
for idx in test_indices:
	test_src.append(df_src[idx].strip().lower())	
	test_tgt.append(df_tgt[idx].strip())

tunning_src = []
tunning_tgt = []
for idx in tunning_indices:
	tunning_src.append(df_src[idx].strip().lower())
	tunning_tgt.append(df_tgt[idx].strip())

train_src = []
train_tgt = []
for idx in test_indices:
	train_src.append(df_src[idx].strip().lower())
	train_tgt.append(df_tgt[idx].strip())

with codecs.open(dir_train + '/train.' + src_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(train_src))
with codecs.open(dir_train + '/train.' + tgt_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(train_tgt))

with codecs.open(dir_test + '/test.' + src_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(test_src))
with codecs.open(dir_test + '/test.' + tgt_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(test_tgt))

with codecs.open(dir_tunning + '/tunning.' + src_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(tunning_src))
with codecs.open(dir_tunning + '/tunning.' + tgt_ext, 'w', 'utf-8') as f:
	f.write('\n'.join(tunning_tgt))
