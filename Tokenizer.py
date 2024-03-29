#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import traceback

import sbd
from sbd import *
from sbd.core import *
from sbd.detector import *

import sbd.core.Tokenizer as tokenizer
import sbd.core.Token as token

def wrap_horizontal_line(str):
    length = 60
    print '\n' + '='*length
    print str
    print '='*length + '\n'

def print_usage():
    str = 'Document Tokenizer'
    str += '\nUsage: python Tokenizer.py [filename]'
    str += '\nUsage: python Tokenizer.py test'
    wrap_horizontal_line(str)

def exit():
    sys.exit()

if __name__ == '__main__':
    try:
        stream = raw_input()
        while (len(stream) > 0):
            tokenizer_ = tokenizer.Tokenizer()
            prev = token.Token()
            line = 0
            for curr in tokenizer_.stokenize(stream):
                key = curr.value + '\t'
                type = curr.part_of_type
                pos = curr.part_of_speech
                if len(key) < 9:
                    key += '\t'
                value = curr.part_of_type + '\t'
                if len(value) < 12:
                    value += '\t'
                if len(key.strip()) > 0:
                    print key, value, "type:"+type, "pos:" + pos, curr.end_of_sentence
                #print prev.value, curr.value, curr.end_of_sentence
                prev = curr
                line += 1
            stream = raw_input()

    except:
        traceback.print_exc(file=sys.stderr)


