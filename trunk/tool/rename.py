#/usr/bin/env python

import os
os.system('ls *.txt > temp')
file = open('temp')
for line in file:
    filenames = line.strip().split(' ')
    for filename in filenames:
	rename = filename.replace('txt', 'raw')
	os.system('mv ' + filename + ' ' + rename)
os.system('rm temp')
