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

class BatchSBD:
    def __init__(self, dictpath):
        util.Logger.info('Initializing sbd instance...')
        self.tokenizer = Tokenizer.Tokenizer()
        self.statistics = defaultdict(int)
        self.dictionary = Dictionary.Dictionary(dictpath)
        self.dictionary.load('syllable')
        self.dictionary.load('token')
        self.dictionary.load('type')
        self.dictionary.load('length')
        self.model = MaxentModel()
        self.threshold = 0.0
        util.Logger.info('sbd instance Initialized.')

    def load(self, modelname=None, threshold=0.0):
        util.Logger.info('Loading model...')
        assert(modelname != None)
        assert(modelname.strip() != '')
        try:
            util.Logger.debug("Started to load model...")
            self.model.load(modelname)
            self.threshold = threshold
            util.Logger.debug("Completed to load model '%s'" % modelname)
        except:
            raise
        util.Logger.info('Model loaded.')

    def run(self, input=None, output=None, syllable_length=1, merged_use=False):
        util.Logger.info('run ' + input + ',' + output)
        assert(input != None)
        assert(input.strip() != '')
        assert(output != None)
        assert(output.strip() != '')
        try:
            # load document 
            util.Logger.info("Started to load document.")
            document = Document.Document()
            ifile = open(input)
            # build document
            util.Logger.info("Adding token to document.")
            self.tokenizer.clear()
            for token in self.tokenizer.tokenize(ifile):
                document.add(token)
            ifile.close()
            # detect sentence boundaries
            util.Logger.info("Detecting sentence boundaries.")
            ofile = open(output, "w+")
            line = ''
            lineno = 1
            for id in range(document.length()):
                prev = document.prev(id)
                curr = document.token(id)
                next = document.next(id)
                eos = False
                # check every position
                eos = self.eval(document, id, prev, curr, next, syllable_length, merged_use)
                if eos == None:
                    continue; # null field found
                line += curr.value
                if curr.isEoe():
                    line += ' '
                if eos and len(line.strip()) > 0:
                    if line[0:1] == ' ':
                        ofile.write('\n')
                    ofile.write(line.strip() + '\n')
                    line = ''
            ofile.write(line.strip() + '\n')
            ofile.close()
            document.clear()
            util.Logger.info("Detecting '%s' document completed." % input)
        except:
            raise

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
    print "python BatchSBD.py [dictpath] [modelname] [syllable_length] [merged_yn] [ignore_case_yn] [threshold] [config] [fileid]"
    print "python BatchSBD.py dict/sejong model/maxent.model 1 yes no 0.8 config 1"
    print "python BatchSBD.py dict/pentree model/maxent.model 0 no yes 0.8 config 1"

def exit(msg):
    print msg
    sys.exit()

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 9:
        print_usage()
        exit("System exit")
    dictpath = sys.argv[1]
    modelname = sys.argv[2]
    syllable_length = int(sys.argv[3])
    merged_yn = sys.argv[4]
    ignore_case_yn = sys.argv[5]
    threshold = float(sys.argv[6])
    filelist = sys.argv[7]
    fileid = sys.argv[8]
    merged_use = False
    if merged_yn != 'yes' and merged_yn != 'no':
        print_usage()
        exit("System exit")
    if merged_yn == 'yes':
        merged_use = True

    # read header from filelist
    # file from fileid
    try:
        file = open(filelist, "r")
        Rule=None
        Input=None
        Output=None
        # initialize sbd instance
        sbd = BatchSBD(dictpath)
        sbd.load(modelname, threshold)
        for line in file:
            Key, Value = line.strip().split('\t')
            if Key == "@Rule":
                Rule = Value
                continue
            elif Key == "@Input":
                Input = Value
                continue
            elif Key == "@Output":
                Output = Value
                continue
            # assert configuration
            if Rule == None or Input == None or Output == None:
                exit("Illegal config format, must include Rule, Input, Output section")
            else:
                import datetime
                util.Logger.info(datetime.datetime.today())
            # skip previous fildid
            input_filename = os.path.join(Input, Value)
            output_filename = os.path.join(Output, Value)
            if Key < fileid:
                print "Skip " + input_filename
                continue
            else:
                print "Processing " + input_filename
            sbd.run(input_filename, output_filename)

        file.close()

    except:
        file.close()
        traceback.print_exc(file=sys.stderr)

