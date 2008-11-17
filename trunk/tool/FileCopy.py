#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import traceback

from sbd.util import *
import sbd.util.Directory as directory

def print_usage():
    print 'python FileCopy.py [src_dir] [dest_dir] [extension]'
    print 'python FileCopy.py Sejong corpus raws'

if __name__ == '__main__':
    COMMAND = 'cp'
    _ = ' '
    if len(sys.argv) < 3:
	print_usage()
	exit()
    try:
	SRC_DIR = str(sys.argv[1])
	DEST_DIR = str(sys.argv[2])
	EXT = str(sys.argv[3])
	file = directory.Directory()
	COUNT = 1000
	file.traverse(SRC_DIR, EXT, file.printnull, COUNT)
	filelist = file.getlist()
	INDEX = 1
	for FILENAME in filelist:
	    DESTFILE = os.path.join(DEST_DIR, str(INDEX) + '.txt')
	    EXECUTE = COMMAND +_+ FILENAME +_+ DESTFILE
	    print EXECUTE
	    os.system(EXECUTE)
	    INDEX += 1
    except:
	traceback.print_exc(file=sys.stderr)

