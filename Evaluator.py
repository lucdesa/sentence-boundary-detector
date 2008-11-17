#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import traceback

class Evaluator:
    def __init__(self):
        pass

def print_usage():
    print 'python Evaluator.py [filename]'

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print_usage()
        exit()
    filename = sys.argv[1]
    try:
        file = open(filename)
        dict = {}
        for line in file:
            line = line.strip()
            count, func = line.split(' ')
            dict[func] = int(count)*1.0
        tp = dict['TP']
        tn = dict['TN']
        fp = dict['FP']
        precision = tp / (tp + tn)
        recall = tp / (tp + fp)
        fscore = (2*precision*recall) / (precision+recall)
        print "Precision:\t", precision
        print "Recall:\t\t", recall
        print "Fscore:\t\t", fscore
        file.close()
    except:
        traceback.print_exc(file=sys.stderr)
