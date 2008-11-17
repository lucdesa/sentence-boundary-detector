#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
import traceback

from collections import defaultdict

import sbd
from sbd import *
from sbd.core import *
import sbd.util.Util as util

class RuleBasedSBD:
    def __init__(self):
        self.tokenizer = Tokenizer.Tokenizer()
        self.documents = defaultdict(Document.Document)
        self.statistics = defaultdict(int)

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

    def eval(self, document, prev, curr, next, DEBUG=False):
        eos = False
        # Slash/ : 이전 구두점까지의 거리가 1보다 크거나, 인용문이 있는경우
        if prev.isEoe() and (document.prevPunctuationDist(id) >= 1 or prev.isDoubleQuote()) \
            and curr.isEoe() and curr.isSlash():
            eos = True
            util.Logger.debug('\tSlash', curr.value)
        # Numeric0~9
        elif prev.isEoe() and prev.isNumeric() \
            and curr.isEoe() and curr.isNumeric():
            eos = True
            util.Logger.debug('\tNumeric', curr.value)
        # Ellipsis…
        elif not prev.isEoe() and prev.isHanguel() and document.prevPunctuationDist(id) >= 1 \
            and curr.isEoe() and curr.isEllipsis():
            eos = True
            util.Logger.debug('\tEllipsis', curr.value)
        # Period.            다음문장 처음에 인용부호나 괄호가 있는 경우는 왜 예외로 했는지... -_-
        elif not prev.isEoe() \
            and (prev.isHanguel() or prev.isCloseParenthesis(0) or prev.isSingleQuote() or prev.isEllipsis() or prev.isUnknown()) \
            and not prev.isEnglish() and not prev.isNumeric() \
            and curr.isPeriod() and curr.isEoe():# \
            #and not (next.isQuote() and next.isEoe()) and not next.isLesserThan():
            eos = True
            util.Logger.debug('\tPeriod', curr.value)
        # Period.            '...했습니다 .' 으로 끝나는 경우
        elif prev.isHanguel() and prev.isEoe() \
            and curr.isPeriod() and curr.isEoe():
            eos = True
        # Period.            '39.5%.', '031-393-4523.', '...}.', '...].', '...###', 'psyoblade@nate.com', '...M.C.', '...".', '... --' 등등
        # 예외처리 할 수도 있지만, 워낙 건 수도 작고 overfitting의 우려가 있어서 하지 않음
        # DoubleQuote" : singlequote를 넣으면 recall이 상당히 떨어짐
        elif not prev.isEoe() and (prev.isPeriod() or prev.isHanguel() or prev.isQuestion() or prev.isExclamation()) \
            and curr.isDoubleQuote() and curr.isEoe() \
            and not next.isParenthesis(0) and not next.isSlash():
            eos = True
            util.Logger.debug('\tDoubleQuote', curr.value)
        # Question? : parenthesis()를 넣으면 recall이 상당히 떨어짐
        elif not prev.isEoe() and prev.isHanguel() \
            and curr.isQuestion() and curr.isEoe() :
            eos = True
            util.Logger.debug('\tQuestion', curr.value)
        # Parenthesis(0){1}[2]
        elif (prev.isHanguel() or prev.isQuestion() or prev.isPeriod()) \
            and curr.isParenthesis(2) and curr.isEoe():
            eos = True
            util.Logger.debug('\tParenthesis', curr.value)
        # Exclamation!
        elif prev.isHanguel() \
            and curr.isExclamation() and curr.isEoe() \
            and not next.isQuote():
            eos = True
            util.Logger.debug('\tExclamation', curr.value)
        # GreaterThan>
        elif prev.isHanguel() and not prev.isEoe() \
            and curr.isGreaterThan() and curr.isEoe():
            eos = True
            util.Logger.debug('\tGreaterThan', curr.value)
        else:
            eos = False
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
        tp = self.statistics['TP']
        tn = self.statistics['TN']
        fp = self.statistics['FP']
        precision = tp * 1.0 / (tp + tn)
        recall = tp * 1.0 / (tp + fp)
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
        assert(i > 0)
    for j in xrange(id-i-1):
        curr = document.next(i+j)
        buff.append(curr.value)
        if curr.isEoe():
            buff.append(' ')
    return ''.join(buff)

def print_usage():
    print "python RuleBasedSBD.py [filename] [seg|eval]"
    print "seg: segmenting"
    print "eval: evaluation"

def exit():
    sys.exit()

if __name__ == '__main__':
    argc = len(sys.argv)
    if argc != 3:
        print_usage()
        exit()
    filename = sys.argv[1]
    functype = sys.argv[2]
    try:
        sbd = RuleBasedSBD()
        sbd.set(filename)
        document = sbd.get(filename)
        line = ''
        lineno = 1

        for id in range(document.length()):
            curr = document.token(id)
            prev = document.prev(id)
            next = document.next(id)
            if curr.isEoe():
                eos = sbd.eval(document, prev, curr, next)
            else:
                eos = False

            if functype == 'seg':
                line += curr.value
                if curr.isEoe():
                    line += ' '
                if eos:
                    print line
                    line = ''
            elif functype == 'eval':
                res = sbd.calc(curr.isEos(), eos)
                if curr.isEos():
                    lineno += 1
                if (lineno % 10000) == 0:
                    util.Logger.debug("Processing %d lines..." % lineno)
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

    except:
        traceback.print_exc(file=sys.stderr)

