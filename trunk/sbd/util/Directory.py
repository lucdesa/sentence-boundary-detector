#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
import time
import traceback

class Directory:
    def __init__(self):
        self.index = 0
        self.filelist = []

    def println(self, filename, index):
        print "[", index, "]", filename

    def printnull(self, filename, index):
        null = ""

    def traverse(self, directory, ext, function, end):
        for filename in os.listdir(directory):
            filename = os.path.join(directory, filename)
            if os.path.isfile(filename):
                if self.index >= end:
                    return
                length = len(filename)
                extension = filename[length-4:].lower()
                #print "debug", self.index, length, extension, filename, "ext:"+ext, "extension:"+extension
                if extension == ext:
                    function(filename, self.index)
                    self.filelist.append(filename)
                    self.index += 1
        for dirname in os.listdir(directory):
            dirname = os.path.join(directory, dirname)
            if os.path.isdir(dirname):
                self.traverse(dirname, ext, function, end)

    def getlist(self):
        return self.filelist

def print_usage():
    print 'python Directory.py [rootpath] [extension] [skip-count] [exec-count] [python] [argv]'
    print 'python Directory.py /home/psyoblade/workspace/corpus/sejong/tagged/raws raws 0 1 DicBuilder.py dictpath'
    print 'python Directory.py /home/psyoblade/workspace/corpus/sejong/tagged/raws raws 0 1 SentenceBoundaryDetector.py build-arff'

if __name__ == '__main__':
    PYTHON = 'python'
    _ = ' '
    if len(sys.argv) < 6:
        print_usage()
        exit()
    try:
        ROOTPATH = str(sys.argv[1])
        EXT = str(sys.argv[2])
        SKIP = int(sys.argv[3])
        COUNT = int(sys.argv[4]) + SKIP
        PYFILE = str(sys.argv[5])
        ARGV = sys.argv[6]
        file = Directory()
        file.traverse(ROOTPATH, EXT, file.printnull, COUNT)
        filelist = file.getlist()
        for FILENAME in filelist:
            if SKIP > 0:
                SKIP -= 1
                continue
            os.system(PYTHON +_+ PYFILE +_+ FILENAME +_+ ARGV)
            print "Executed:\t'", PYTHON +_+ PYFILE +_+ FILENAME +_+ ARGV, "'"
    except:
        traceback.print_exc(file=sys.stderr)

