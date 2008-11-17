#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sbd.util.Util as util

class Token():
    EMPTY =  ' '
    CR = '\r'
    LF = '\n'
    PERIOD = '.'
    QUESTION = '?'
    EXCLAMATION = '!'
    COMMA = ','
    MIDDLE_POINT = '·'
    SEMI_COLON = ':'
    SLASH = '/'
    DOUBLE_QUOTE = '"'     # == '”
    SINGLE_QUOTE = '\''    # == '’
    OPEN_PARENTHESIS = ['(', '{', '[']
    CLOSE_PARENTHESIS = [')', '}', ']']
    DASH = '─'
    HYPHEN = '-'
    TILD = '~'
    DURO = '˙'
    HIDE = [ '×', '○' ]
    EXTRACT = '□'
    ELLIPSIS = '…'
    TAG_GT = '>'
    TAG_LT = '<'

    CANDIDATE_TYPE = [ PERIOD, QUESTION, EXCLAMATION, DOUBLE_QUOTE, SINGLE_QUOTE, ELLIPSIS, SLASH ]
    
    # 공백 = [ '\r', '\n', ' ' ]
    SPACE = [ EMPTY ] #, CR, LF ]
    # 마침표 = [ 온점, 물음표, 느낌표 ]
    MACHIM = [ PERIOD, EXCLAMATION, QUESTION ]
    # 쉼표 = [ 반점, 가운뎃점, 쌍점, 빗금 ]
    SHUIM = [ COMMA, MIDDLE_POINT, SEMI_COLON, SLASH ]
    # 따옴표 = [ 큰따옴표, 작은따옴표 ]
    TTAOM = [ DOUBLE_QUOTE, SINGLE_QUOTE ]
    # 묶음표 = [ 소괄호, 중괄호, 대괄호 ]
    MMUKUM = OPEN_PARENTHESIS + CLOSE_PARENTHESIS
    # 이음표 = [ 줄표, 붙임표, 물결표 ]
    IUM = [ DASH, HYPHEN, TILD ]
    # 드러냄표 = [ 드러냄표 ]
    DURONEM = [ DURO ]
    # 안드러냄표 = [ 숨김표, 빠짐표, 줄임표 ]
    ANDURONEM = HIDE + [ EXTRACT, ELLIPSIS ]
    # 기타기호
    OTHERS = [TAG_GT, TAG_LT]
    # 한글문장에서  나올 수 있는 문장부호
    PUNCTUATION_TYPE = SPACE
    PUNCTUATION_TYPE += MACHIM + SHUIM + TTAOM + MMUKUM + IUM + DURONEM + ANDURONEM
    PUNCTUATION_TYPE += OTHERS
    def __init__(self, id = -1, value = '', type = '', pos = '', eoe = False, eos = False):
        self.id = id
        self.raw = value
        self.value = self.filter(value)
        self.part_of_type = type
        self.part_of_speech = pos
        self.length = len(unicode(self.value, 'utf-8'))
        self.byte_length = len(self.value)
        self.size_of_char = 0
        if self.length > 0:
            self.size_of_char = self.byte_length / self.length
        self.end_of_eojeol = eoe
        self.end_of_sentence = eos
        self.util = util.Common()

    def filter(self, value):
        single_quotes=['‘','’']
        double_quotes=['“','”']
        for quote in single_quotes:
            value = value.replace(quote, '\'')
        for quote in double_quotes:
            value = value.replace(quote, '"')
        #value = value.replace('∼', '~')
        return value

    def syllable(self, offset=0):
        offset *= self.size_of_char
        if offset == 0:
            return self.value
        elif offset > 0:
            return self.value[0:offset]
        elif offset < 0:
            return self.value[len(self.value)+offset:]

    def isCandidate(self):
        return self.raw in self.CANDIDATE_TYPE
    
    def isPunctuation(self, exceptSpace=False):
        if exceptSpace:
            return self.raw in self.PUNCTUATION_TYPE[1:]
        return self.raw in self.PUNCTUATION_TYPE

    def isPeriod(self):
        if self.value == self.PERIOD:
            return True
        return False
    
    def isExclamation(self):
        if self.value == self.EXCLAMATION:
            return True
        return False

    def isQuestion(self):
        if self.value == self.QUESTION:
            return True
        return False

    def isDoubleQuote(self):
        if self.value == self.DOUBLE_QUOTE:
            return True
        return False

    def isSingleQuote(self):
        if self.value == self.SINGLE_QUOTE:
            return True
        return False
    
    def isQuote(self):
        if self.value == self.SINGLE_QUOTE or \
           self.value == self.DOUBLE_QUOTE:
            return True
        return False

    def isOpenParenthesis(self, i = -1):
        if i in [ 0, 1, 2 ]:
            if self.value == self.OPEN_PARENTHESIS[i]:
                return True
        else:
            if self.value in self.OPEN_PARENTHESIS:
                return True
        return False

    def isCloseParenthesis(self, i = -1):
        if i in [ 0, 1, 2 ]:
            if self.value == self.CLOSE_PARENTHESIS[i]:
                return True
        else:
            if self.value in self.CLOSE_PARENTHESIS:
                return True
        return False

    def isParenthesis(self, i = -1):
        if i in [ 0, 1, 2 ]:
            if self.value == self.OPEN_PARENTHESIS[i] or \
                self.value == self.CLOSE_PARENTHESIS[i]:
                return True
        else:
            if self.value in self.OPEN_PARENTHESIS or \
                self.value in self.CLOSE_PARENTHESIS:
                return True
        return False

    def isEllipsis(self):
        if self.value.startswith(self.ELLIPSIS):
            return True
        return False

    def isSlash(self):
        if self.value == self.SLASH:
            return True
        return False

    def isGreaterThan(self):
        if self.value == self.TAG_GT:
            return True
        return False

    def isLesserThan(self):
        if self.value == self.TAG_LT:
            return True
        return False

    def isHanguel(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_hg(value)[0]:
            return True
        return False

    def isNumeric(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_sn(value)[0]:
            return True
        return False

    def isEnglish(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_sl(value)[0]:
            return True
        return False

    def isHanja(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_sh(value)[0]:
            return True
        return False

    def isSpecial(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_ss(value)[0]:
            return True
        return False

    def isUnknown(self):
        value = unicode(self.value, 'utf-8')
        if self.util.is_pos_xx(value)[0]:
            return True
        return False

    def isEoe(self):
        return self.end_of_eojeol

    def isEos(self):
        return self.end_of_sentence

    def debug(self):
        print '[%d] %s/%s (%d:%d:%s:%s)' % (self.id, \
            self.value, self.part_of_speech, \
            self.length, self.byte_length, \
            self.end_of_eojeol, self.end_of_sentence)

