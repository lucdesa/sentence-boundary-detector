#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

class ResultParser:
    def __init__(self, filename):
        self.file = open(filename, 'r')

    def __del__(self):
        self.file.close()

    def detect(self, line):
        info, type, value = line.strip().split()
        return type[:-1], value[:-1]

    def parse(self):
        prec = 0.0
        recall = 0.0
        fscore = 0.0
        fold = 0
        for line in self.file:
            if line.find('%') < 0:
                continue
            type, svalue = self.detect(line)
            value = float(svalue)
            if type == 'Precision':
                fold += 1
                prec += value
            elif type == 'Recall':
                recall += value
            elif type == 'Fscore':
                fscore += value
            else:
                assert(False)
        print 'Precision:\t', prec/fold
        print 'Recall:\t\t', recall/fold
        print 'Fscore:\t\t', fscore/fold

def main():
    if len(sys.argv) != 2:
        print_usage()
        exit()
    filename = sys.argv[1]
    try:
        parser = ResultParser(filename)
        parser.parse()
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)

def print_usage():
    print 'python MergeResult.py result/tenfolds-sejong'
    print 'python MergeResult.py result/tenfolds-pentree'

def exit():
    sys.exit()

if __name__ == '__main__':
    main()
    
