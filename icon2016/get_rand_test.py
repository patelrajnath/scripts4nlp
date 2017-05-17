#!/usr/bin/python

import sys, re, codecs, random

"""
Created by Raj Nath Patel, 25th Sept, 2016
Purpose: To get n test and dev samples from the data and remaining for training


Usage: python get_rand_test.py text_file tags_file lang manual-tag test/dev_size

"""

if len(sys.argv) != 6:
	print 'Usage: python', sys.argv[0], 'text_file tags_file lang_file manual-tag test/dev_size'
	exit()


f1= sys.argv[1]
f2= sys.argv[2]
f3= sys.argv[3]
f4= sys.argv[4]

f1_in = codecs.open(f1, 'r', 'utf-8')
f2_in = codecs.open(f2, 'r', 'utf-8')
f3_in = codecs.open(f3, 'r', 'utf-8')
f4_in = codecs.open(f4, 'r', 'utf-8')

f1_test = codecs.open(f1 + '.test', 'w', 'utf-8')
f2_test = codecs.open(f2 + '.test', 'w', 'utf-8')
f3_test = codecs.open(f3 + '.test', 'w', 'utf-8')
f4_test = codecs.open(f4 + '.test', 'w', 'utf-8')

f1_dev = codecs.open(f1 + '.dev', 'w', 'utf-8')
f2_dev = codecs.open(f2 + '.dev', 'w', 'utf-8')
f3_dev = codecs.open(f3 + '.dev', 'w', 'utf-8')
f4_dev = codecs.open(f4 + '.dev', 'w', 'utf-8')

f1_train = codecs.open(f1 + '.train', 'w', 'utf-8')
f2_train = codecs.open(f2 + '.train', 'w', 'utf-8')
f3_train = codecs.open(f3 + '.train', 'w', 'utf-8')
f4_train = codecs.open(f4 + '.train', 'w', 'utf-8')

text_lines = f1_in.readlines()
tag_lines = f2_in.readlines()
lang_lines = f3_in.readlines()
pred_tag_lines = f4_in.readlines()


#test_size = len(text_lines)/10
test_size = int(sys.argv[5])

random.seed(345)
random.shuffle(text_lines)
random.seed(345)
random.shuffle(tag_lines)
random.seed(345)
random.shuffle(lang_lines)
random.seed(345)
random.shuffle(pred_tag_lines)

start = 0

f1_test.write(''.join(text_lines[start:test_size]))
f2_test.write(''.join(tag_lines[start:test_size]))
f3_test.write(''.join(lang_lines[start:test_size]))
f4_test.write(''.join(pred_tag_lines[start:test_size]))

start +=test_size
test_size += test_size

f1_dev.write(''.join(text_lines[start:test_size]))
f2_dev.write(''.join(tag_lines[start:test_size]))
f3_dev.write(''.join(lang_lines[start:test_size]))
f4_dev.write(''.join(pred_tag_lines[start:test_size]))

f1_train.write(''.join(text_lines[test_size:]))
f2_train.write(''.join(tag_lines[test_size:]))
f3_train.write(''.join(lang_lines[test_size:]))
f4_train.write(''.join(pred_tag_lines[test_size:]))

