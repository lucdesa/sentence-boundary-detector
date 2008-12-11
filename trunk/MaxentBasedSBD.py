#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import traceback
import time

from collections import defaultdict
from maxent import MaxentModel

import sbd
from sbd import *
from sbd.util import *
from sbd.core import *
import sbd.util.Util as util

class MaxentBasedSBD:
    def __init__(self, dictpath):
        self.tokenizer = Tokenizer.Tokenizer()
        self.documents = defaultdict(Document.Document)
        self.statistics = defaultdict(int)
        self.dictionary = Dictionary.Dictionary(dictpath)
        self.dictionary.load('syllable')
        self.dictionary.load('token')
        self.dictionary.load('type')
        self.dictionary.load('length')
        self.model = MaxentModel()
        self.threshold = 0.0

    def set(self, modelname=None, threshold=0.0, filename=None):
        assert(modelname != None)
        assert(modelname.strip() != '')
        assert(filename != None)
        assert(filename.strip() != '')
        try:
            util.Logger.debug("Started to load model...")
            self.model.load(modelname)
            self.threshold = threshold
            util.Logger.debug("Completed to load model '%s'" % modelname)
        except:
            raise
        try:
            util.Logger.debug("Started to load document...")
            document = Document.Document()
            file = open(filename)
            for token in self.tokenizer.tokenize(file):
                document.add(token)
            file.close()
            self.documents[filename] = document
            util.Logger.debug("Competed to load document '%s'" % filename)
        except:
            raise

    def get(self, filename=None):
        assert(filename != None)
        assert(filename.strip() != '')
        if filename in self.documents:
            return self.documents[filename]
        else:
            return Document.Document()

    def eos(self, context):
        label = 'yes'
        prob = self.model.eval(context, label)
        buf = ''
        if prob >= self.threshold:
            return True
        else:
            return False

    # append property into list-buf
    def append_maxent_parameter(self, list, i, property):
        i += 1
        list.append(str(i) + ':' + str(property))
        return i

    # FIXME: code duplicattion with sbd.detector.Probabilistic.py
    def eval(self, document, id, prevToken, currToken, nextToken, syllable_length=0, merged_use=False):
        dict = self.dictionary
        common = util.Common()
        # default token value
        default = '_'
        # { pos-type, pos-name }
        current_pos_type = common.name_of_type(currToken)
        current_pos_name = common.name_of_pos(currToken)
        prefix_pos_type = common.name_of_type(prevToken)
        prefix_pos_name = common.name_of_pos(prevToken)
        suffix_pos_type = common.name_of_type(nextToken)
        suffix_pos_name = common.name_of_pos(nextToken)
        # { syllables }
        prefix_syllable_name = []
        prefix_syllable_prob = []
        suffix_syllable_name = []
        suffix_syllable_prob = []
        merged_syllable_name = []
        merged_syllable_prob = []
        for length in xrange(syllable_length):
            if prevToken.length == 0: prefixName = default * syllable_length
            else: prefixName = prevToken.syllable(-1*(length+1))
            prefix_syllable_name.append(prefixName)
            prefix_syllable_prob.append(dict.getPrefixSyllableProb(prefixName))
            if nextToken.length == 0: suffixName = default * syllable_length
            else: suffixName = nextToken.syllable(length+1)
            suffix_syllable_name.append(suffixName)
            suffix_syllable_prob.append(dict.getSuffixSyllableProb(suffixName))
            if merged_use:
                mergedName = prefixName + '_' + suffixName
                merged_syllable_name.append(mergedName)
                merged_syllable_prob.append(dict.getMergedSyllableProb(mergedName))
        # { token-name, token-prob }
        if currToken.length == 0: current_token_name = default
        else: current_token_name = currToken.value
        current_token_prob = dict.getCurrentTokenProb(current_token_name)
        if prevToken.length == 0: prefix_token_name = default
        else: prefix_token_name = prevToken.value
        prefix_token_prob = dict.getPrefixTokenProb(prefix_token_name)
        if nextToken.length == 0: suffix_token_name = default
        else: suffix_token_name = nextToken.value
        suffix_token_prob = dict.getSuffixTokenProb(suffix_token_name)
        # { candidate-distance }
        prefix_candidate_dist = document.prevCandidateDist(id)
        suffix_candidate_dist = document.nextCandidateDist(id)
        # { punctuation-distance }
        prefix_punctuation_dist = document.prevPunctuationDist(id)
        suffix_punctuation_dist = document.nextPunctuationDist(id)
        # { token-length }
        current_token_length = currToken.length
        prefix_token_length = prevToken.length
        suffix_token_length = nextToken.length
        # { end-of-sentence }
        end_of_sentence = 'no'
        if currToken.end_of_sentence:
            end_of_sentence = 'yes'
        context = [end_of_sentence]
        i = 0
        # { building instances }
        i = self.append_maxent_parameter(context, i, current_pos_type)
        i = self.append_maxent_parameter(context, i, current_pos_name)
        i = self.append_maxent_parameter(context, i, prefix_pos_type)
        i = self.append_maxent_parameter(context, i, prefix_pos_name)
        i = self.append_maxent_parameter(context, i, suffix_pos_type)
        i = self.append_maxent_parameter(context, i, suffix_pos_name)
        # XXX: maxent use NAME instead of PROBABILITY
        for length in xrange(syllable_length):
            i = self.append_maxent_parameter(context, i, prefix_syllable_name[length])
            i = self.append_maxent_parameter(context, i, suffix_syllable_name[length])
            if merged_use:
                i = self.append_maxent_parameter(context, i, merged_syllable_name[length])
        i = self.append_maxent_parameter(context, i, current_token_name)
        i = self.append_maxent_parameter(context, i, prefix_token_name)
        i = self.append_maxent_parameter(context, i, suffix_token_name)
        i = self.append_maxent_parameter(context, i, str(current_token_length))
        i = self.append_maxent_parameter(context, i, str(prefix_token_length))
        i = self.append_maxent_parameter(context, i, str(suffix_token_length))
        eos = self.eos(context)
        return eos

    def calc(self, answer, rule):
        if answer == True and rule == True:
            result = 'TP'
        elif answer == True and rule == False:
            result = 'TN'
        elif answer == False and rule == True:
            result = 'FP'
        else:
            result = 'FN'
        self.statistics[result] += 1

    def summary(self):
        precision = 0.0
        recall = 0.0
        fscore = 0.0
        tp = self.statistics['TP']
        tn = self.statistics['TN']
        fp = self.statistics['FP']
        util.Logger.info("tp:", tp, "tn:", tn, "fp:", fp)
        if (tp + tn) > 0:
            precision = tp * 1.0 / (tp + tn)
        if (tp + fp) > 0:
            recall = tp * 1.0 / (tp + fp)
        if (precision+recall) > 0:
            fscore = (2*precision*recall) / (precision+recall)
        util.Logger.info("Precision:\t%0.3f%%" % (precision * 100.0))
        util.Logger.info("Recall:\t\t%0.3f%%" % (recall * 100.0))
        util.Logger.info("Fscore:\t\t%0.3f%%" % (fscore * 100.0))




# 이전 문장경계 이전까지의. 토큰을 버퍼에 담아서 반환.
def getPrevNValue(docucment, id):
    buff = []
    token = document.prev(id)
    i = id-1
    assert(i > 0)
    while (not token.isEos()):
        token = document.prev(i)
        i = i-1
        if (i > 0):
            return ''
        assert(i > 0)
    for j in xrange(id-i-1):
        curr = document.next(i+j)
        buff.append(curr.value)
        if curr.isEoe():
            buff.append(' ')
    return ''.join(buff)

def print_usage():
    print "python MaxentBasedSBD.py [dictpath] [modelname] [syllable_length] [merged_yn] [ignore_case_yn] [threshold] [filename] [eval|seg]"
    print "python MaxentBasedSBD.py dict/sejong model/maxent.model 1 yes no 0.8 corpus/sejong/sample.txt eval"
    print "python MaxentBasedSBD.py dict/sejong model/maxent.model 1 yes no 0.8 corpus/sejong/sample.txt seg"
    print "python MaxentBasedSBD.py dict/pentree model/maxent.model 0 no yes 0.8 corpus/pentree/sample.txt eval"
    print "python MaxentBasedSBD.py dict/pentree model/maxent.model 0 no yes 0.8 corpus/pentree/sample.txt seg"

def exit():
    sys.exit()

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 9:
        print_usage()
        exit()
    dictpath = sys.argv[1]
    modelname = sys.argv[2]
    syllable_length = int(sys.argv[3])
    merged_yn = sys.argv[4]
    ignore_case_yn = sys.argv[5]
    threshold = float(sys.argv[6])
    filename = sys.argv[7]
    functype = sys.argv[8]
    merged_use = False
    if merged_yn != 'yes' and merged_yn != 'no':
        print_usage()
        exit()
    if merged_yn == 'yes':
        merged_use = True
    try:
        sbd = MaxentBasedSBD(dictpath)
        sbd.set(modelname, threshold, filename)
        document = sbd.get(filename)
        line = ''
        lineno = 1
        for id in range(document.length()):
            prev = document.prev(id)
            curr = document.token(id)
            next = document.next(id)
            eos = False
            if True: # 2008.10.13 문장경계후보를 모든위치로 변경 curr.isEoe():
                eos = sbd.eval(document, id, prev, curr, next, syllable_length, merged_use)
            else:
                assert(False == curr.isEos())
                eos = False
            if eos == None:
                continue; # null field found
            if functype == 'seg':
                line += curr.value
                if curr.isEoe():
                    line += ' '
                if eos and len(line.strip()) > 0:
                    if line[0:1] == ' ':
                        print ''
                    print line.strip() + '\n'
                    line = ''
            elif functype == 'eval':
                res = sbd.calc(curr.isEos(), eos)
                if curr.isEos():
                    lineno += 1
                if (id % 10000) == 0:
                    util.Logger.debug("Processing token[%d]..." % id)
            # 문장경계인데 찾아내지 못한 경우 (TrueNegative)
            elif functype == 'debug-tn':
                if id > 10 and curr.isEos() == True and eos == False:
                    prevBuffer = getPrevNValue(document, id)
                    print prevBuffer + curr.value
            # 문장경계가 아닌데 문장경계로 인식하는 경우 (FalsePositive)
            elif functype == 'debug-fp':
                if id > 10 and curr.isEos() == False and eos == True:
                    prevBuffer = getPrevNValue(document, id)
                    print prevBuffer + curr.value
        
        if functype == 'eval':
            sbd.summary()
        elif functype == 'seg' and line != '':
            print line.strip() + '\n'

    except:
        traceback.print_exc(file=sys.stderr)

