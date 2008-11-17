#!/usr/bin/env python
# -*- coding:utf-8 -*-

# IMPORTANT:
# If there are many raw files, every information must be appended so...
# Every dictionary file will be appended. so remove dictionaries if it's renewal

import sys
import os
import traceback

from collections import defaultdict

import sbd
from sbd import *
from sbd.core import *

import sbd.util.Util as util

class Builder:
    def __init__(self):
        self.tokenizer = Tokenizer.Tokenizer()
        self.documents = defaultdict(Document.Document)
        self.dictionary = Dictionary.Dictionary('dict')
        self.dictionary.init('syllable')
        self.dictionary.init('token')
        self.dictionary.init('type')
        self.dictionary.init('length')

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

def print_usage():
    str = 'Dictionary Builder'
    str += '\npython Builder.py [filename] [dict-path] [syllable-length] [merged-yn] [ignore-case]'
    str += '\npython Builder.py corpus/sejong/sample.txt dict/sejong 1 yes no'
    str += '\npython Builder.py corpus/pentree/sample.txt dict/pentree 1 no yes'
    util.Formatter.print_usage(str, 90)

def exit():
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print_usage()
        exit()
    filename = sys.argv[1]
    dictpath = sys.argv[2]
    syllable_length = int(sys.argv[3])
    merged_yn = sys.argv[4]
    ignore_case = sys.argv[5]
    try:
        builder = Builder()
        builder.set(filename)
        document = builder.get(filename)
        # { get-filename }
        token_filename = os.path.join(dictpath, 'token.raws')
        syllable_filename = os.path.join(dictpath, 'syllable.raws')
        type_filename = os.path.join(dictpath, 'type.raws')
        length_filename = os.path.join(dictpath, 'length.raws')
        # { open-file }
        token_file = open(token_filename, 'a+')
        syllable_file = open(syllable_filename, 'a+')
        type_file = open(type_filename, 'a+')
        length_file = open(length_filename, 'a+')
        for id in range(document.length()):
            currToken = document.token(id)
            assert(currToken.id == id)
            prevToken = document.prev(id)
            nextToken = document.next(id)
            if currToken.end_of_sentence:
                eos = 'True'
            else:
                eos = 'False'
            # { token-value }
            currValue = currToken.value
            prevValue = prevToken.value
            nextValue = nextToken.value
            if ignore_case == 'yes':
                currValue = currValue.lower()
                prevValue = prevValue.lower()
                nextValue = nextValue.lower()
            token_file.write('current_' + eos + '_' + currValue + '\n')
            token_file.write('prefix_' + eos + '_' + prevValue + '\n')
            token_file.write('suffix_' + eos + '_' + nextValue + '\n')
            for length in xrange(syllable_length):
                # { syllables }
                if syllable_length >= length and prevToken.length >= length:
                    prevSyllable = prevToken.syllable(-1*length)
                    nextSyllable = nextToken.syllable(length)
                    if ignore_case == 'yes':
                        prevSyllable = prevSyllable.lower()
                        nextSyllable = nextSyllable.lower()
                    syllable_file.write('prefix_' + eos + '_' + str(length+1) + '_' + prevSyllable + '\n')
                    syllable_file.write('suffix_' + eos + '_' + str(length+1) + '_' + nextSyllable + '\n')
                if merged_yn == 'yes':
                    syllable_file.write('merged_' + eos + '_' + str(length+1) + '_' + prevSyllable + '_' + nextSyllable + '\n')
            # { token-type }
            currType = currToken.part_of_type
            prevType = prevToken.part_of_type
            nextType = nextToken.part_of_type
            if len(currType) > 0:
                type_file.write('current_' + eos + '_' + currType + '\n')
            if len(prevType) > 0:
                type_file.write('prefix_' + eos + '_' + prevType + '\n')
            if len(nextType) > 0:
                type_file.write('suffix_' + eos + '_' + nextType + '\n')
            # { token-length }
            currLength = currToken.length
            prevLength = prevToken.length
            nextLength = nextToken.length
            if currLength > 0:
                length_file.write('current_' + eos + '_' + str(currLength) + '\n')
            if prevLength > 0:
                length_file.write('prefix_' + eos + '_' + str(prevLength) + '\n')
            if nextLength > 0:
                length_file.write('suffix_' + eos + '_' + str(nextLength) + '\n')

        token_file.close()
        syllable_file.close()
        type_file.close()
        length_file.close()

    except:
        traceback.print_exc(file=sys.stderr)

