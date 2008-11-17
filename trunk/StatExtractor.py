#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import traceback

from collections import defaultdict

import sbd
from sbd import *
from sbd.core import *
import sbd.core.Token as token

class StatExtractor:
    def __init__(self):
        self.tokenizer = Tokenizer.Tokenizer()
        self.documents = defaultdict(Document.Document)
        self.token = 0
        self.token_type = defaultdict(str)
        self.eos = 0
        self.eos_type = defaultdict(str)
        self.pair = 0
        self.pair_type = defaultdict(str)

    def set(self, filename=None):
        assert(filename != None)
        assert(filename.strip() != '')
        try:
            document = Document.Document()
            file = open(filename)
            for token in self.tokenizer.tokenize(file):
                document.add(token)
            file.close()
            self.documents[filename] = document
        except:
            raise

    def get(self, filename=None):
        assert(filename != None)
        assert(filename.strip() != '')
        if filename in self.documents:
            return self.documents[filename]
        else:
            return Document.Document()

    def add_token(self, type):
        self.token += 1
        if not type in self.token_type:
            self.token_type[type] = 1
        else:
            self.token_type[type] += 1

    def add_eos(self, type):
        self.eos += 1
        if not type in self.eos_type:
            self.eos_type[type] = 1
        else:
            self.eos_type[type] += 1

    def add_pair(self, typeA, typeB):
        self.pair += 1
        if not typeA+typeB in self.pair_type:
            self.pair_type[typeA+typeB] = 1
        else:
            self.pair_type[typeA+typeB] += 1

    def print_token(self, file):
        file.write(str(self.token) + '\n')
        for item, value in self.token_type.iteritems():
            file.write(str(item) + '\t' + str(value) + '\n')

    def print_eos(self, file):
        file.write(str(self.eos) + '\n')
        for item, value in self.eos_type.iteritems():
            file.write(str(item) + '\t' + str(value) + '\n')

    def print_pair(self, file):
        file.write(str(self.pair) + '\n')
        for item, value in self.pair_type.iteritems():
            file.write(str(item) + '\t' + str(value) + '\n')

def print_usage():
    print "python StatExtractor.py [filename] [init|emit|trans]"

def exit():
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit()
    filename = sys.argv[1]
    functype = sys.argv[2]
    try:
        se = StatExtractor()
        se.set(filename)
        document = se.get(filename)
        for id in range(document.length()):
            curr = document.token(id)
            prev = document.prev(id)
            next = document.next(id)
            se.add_token(curr.part_of_speech)
            if curr.isEos():
                se.add_eos(curr.part_of_speech)
            se.add_pair(curr.part_of_speech, next.part_of_speech)
        statfile = ["token", "eos", "pair"]
        for filename in statfile:
            file = open("stat/" + filename + ".stat", "w+")
            if filename == 'token':
                se.print_token(file)
            elif filename == 'eos':
                se.print_eos(file)
            elif filename == 'pair':
                se.print_pair(file)
            else:
                assert(False)
            file.close()
    except:
        traceback.print_exc(file=sys.stderr)


