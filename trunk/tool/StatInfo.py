#!/usr/bin/env python
# -*- coding:utf8 -*-

import traceback
import sys
import os

import sbd.core.Tokenizer as tokenizer

def print_usage():
    print 'python StatInfo.py [filename]'

def exit(errno=0):
    sys.exit(errno)

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 2:
	print_usage()
	exit()
    filename = sys.argv[1]
    try:
	_tokenizer = tokenizer.Tokenizer()
	file = open(filename)
	for token in _tokenizer.tokenize(file):
	    token.debug()
	file.close()
    except:
	traceback.print_exc(file=sys.stderr)

