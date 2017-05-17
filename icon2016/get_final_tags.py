#!/usr/bin/python

'''

USAGE: python get_final_tags.py  predicted manual_taged
'''

import sys, re, codecs

if len(sys.argv) != 3:
	print "Usage: python", sys.argv[0], "manual predicted"
	exit()

fn1 = sys.argv[1]
fn2 = sys.argv[2]

fin1 = codecs.open(fn1, 'r', 'utf-8')
fin2 = codecs.open(fn2, 'r', 'utf-8')

fout = codecs.open(fn1 + '.proc', 'w', 'utf-8')
flog = codecs.open(fn1 + '.log', 'w', 'utf-8')

manual_tag_list = ['#', '@', '$', 'U', 'E', 'G_X', 'RD_PUNC']
count = 0
for l1, l2 in zip(fin1, fin2):
        predictions = l1.strip().split()
        manual_tags = l2.strip().split()
        final_tags = []
        for manual_tag, prediction in zip(manual_tags, predictions):
                manual_tag = manual_tag.strip()
                if manual_tag in manual_tag_list and manual_tag != prediction:
			count += 1
                        final_tags.append(manual_tag)
		else:
			final_tags.append(prediction.strip())
	if len(predictions) != len(final_tags):
		flog.write(l1 + l2)
	fout.write(' '.join(final_tags) + '\n')
print count
fin1.close()
fin2.close()
fout.close()
