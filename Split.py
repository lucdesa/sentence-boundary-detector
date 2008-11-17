#!/usr/bin/env python
# -*- coding:utf-8 -*-

# static methods
class Util(object):
    def get_total_lineno(filename):
        import os
        import time
        os.system('cat ./' + filename + ' | wc -l > lineno')
        file = open('lineno', 'r')
        lineno = int(file.readline().strip())
        file.close()
        os.system('rm -rf lineno')
        return lineno

    def split_filename(number):
        return str(number) + '.split'

    getTotalLineno = staticmethod(get_total_lineno)
    getSplitFilename = staticmethod(split_filename)

class Split:
    def __init__(self, filename, splitno):
        self.filename = filename
        self.file = open(filename)
        self.splitno = splitno

    def __del__(self):
        if (self.file.closed == False):
            self.file.close()

    def split(self, out):
        files = []
        for number in xrange(self.splitno):
            filename = Util.getSplitFilename(number)
            file = open(out + '/' + filename, 'w+')
            files.append(file)

        lineno = Util.getTotalLineno(self.filename)
        percount = lineno / self.splitno
        count = 0
        number = 1
        for line in self.file:
            count += 1
            if count < percount*number:
                dot = ''
                if number > 9:
                    number = self.splitno
                    dot += dot
                files[number-1].write(line)
            else:
                print str(percount*number) + " number"
                number += 1

        for file in files:
            file.close()

def print_usage():
    print "\tpython Split.py [filename] [outputfolder] [split-number]"
    print "\tpython Split.py corpus/sejong/sejong.raw tenfolds/sejong 10"
    print "\tpython Split.py corpus/pentree/pentree.raw tenfolds/pentree 10"

def exit():
    sys.exit()

if __name__ == '__main__':
    import traceback
    import sys
    if len(sys.argv) != 4:
        print_usage()
        exit()
    filename = sys.argv[1]
    outfolder = sys.argv[2]
    splitno = int(sys.argv[3])
    try:
        s = Split(filename, splitno)
        s.split(outfolder)
        del s
    except:
        traceback.print_exc(file=sys.stderr)

