#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os

from collections import defaultdict

import sbd
from sbd import *
from sbd.util import *
from sbd.core import *
from sbd.detector import *

class Learner:
    def __init__(self, detector, dictpath):
        self.tokenizer = Tokenizer.Tokenizer()
        self.documents = defaultdict(Document.Document)
        self.dictionary = Dictionary.Dictionary(dictpath)
        self.dictionary.load('syllable')
        self.dictionary.load('token')
        self.dictionary.load('type')
        self.dictionary.load('length')
        self.detector = detector

    def add(self, filename=None, file=None):
        assert(filename != None)
        assert(filename.strip() != '')
        try:
            document = Document.Document()
            if file == None:
                file = open(filename)
            for token in self.tokenizer.tokenize(file):
                document.add(token)
            file.close()
            self.documents[filename] = document
        except:
            raise
    
    def detect(self, filename, classifier, syllable_length, merged_use=False):
        document = self.documents[filename]
        dict = self.dictionary
        self.detector.detect(document, dict, classifier, syllable_length, merged_use)

    def debug(self, filename, heuristic_fn=None, skip_print=False):
        document = self.documents[filename]
        self.detector.debug(document, heuristic_fn)

    def evaluate(self, filename, testfile):
        document = self.documents[filename]
        self.detector.evaluate(document)

    def statinfo(self, filename, pattern):
        document = self.documents[filename]
        self.detector.statinfo(document, pattern)

def print_usage():
    import sbd.util.Util as util
    str = "python Learner.py [dict/kor|dict/eng] [maxent|weka] [build] [syllable_length] [merged_yn] [ignore_case_yn] filename > arff/train.arff\n"
    str += "python Learner.py dict/kor weka build 1 yes no corpus/sejong/sample.txt > weka/sejong.arff.raws\n"
    str += "python Learner.py dict/kor maxent build 1 yes no corpus/sejong/sample.txt > maxent/sejong.maxent.raws\n"
    str += "python Learner.py dict/eng weka build 0 no yes corpus/pentree/sample.txt > weka/pentree.arff.raws\n"
    str += "python Learner.py dict/eng maxent build 0 no yes corpus/pentree/sample.txt > maxent/pentree.maxent.raws"
    util.Formatter.print_usage(str, 150)


def exit():
    sys.exit()

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc < 8 or argc > 9:
        print_usage()
        exit()
    dictpath = sys.argv[1]
    classifier = sys.argv[2]
    functype = sys.argv[3]
    syllable_length = int(sys.argv[4])
    merged_yn = sys.argv[5]
    ignore_case_yn = sys.argv[6]
    filename = sys.argv[7]
    args = sys.argv[8:]
    if (classifier != util.Util.Common.MAXENT and classifier != util.Util.Common.WEKA) or (merged_yn != 'yes' and merged_yn != 'no'):
        print_usage()
        exit()
    try:
        sbd = Learner(Probabilistic.Probabilistic(), dictpath)
        sbd.add(filename)
        if functype.startswith('build'):
            merged_use = False
            if merged_yn == 'yes': merged_use = True
            sbd.detect(filename, classifier, syllable_length, merged_use)
        elif functype.startswith('debug'):
            sbd.debug(filename)
        elif functype == 'eval':
            sbd.evaluate(filename, args)
        elif functype == 'stat':
            sbd.statinfo(filename, int(args))
        else:
            print_usage()
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
    exit()

