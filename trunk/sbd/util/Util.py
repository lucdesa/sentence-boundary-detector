#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from collections import defaultdict


class Common:
    DEBUG = os.environ.get("DEBUG")
    POS_TYPE_LIST = [ '공백', '한글', '자모', '마침표', '쉼표', \
                '따옴표', '묶음표', '이음표', '드러냄표', \
                '안드러냄표', '영문자', '한자', '기타기호', \
                '숫자', '미지기호' ]
    POS_INDEX = {}
    UNKNOWN = 'UNK'
    POS_NAME = defaultdict(str)
    POS_TYPE = defaultdict(str)

    # Classifier
    MAXENT = 'maxent'
    WEKA = 'weka'

    ROOT_PATH = '/home/psyoblade/workspace/py/sentence-boundary-detection/sejong'
    ARFF_HEADER = os.path.join(ROOT_PATH, 'arff/header.arff')

    def __init__(self):
        # 인덱스
        self.POS_INDEX['공백'] = 0
        self.POS_INDEX['한글'] = 1
        self.POS_INDEX['자모'] = 2
        self.POS_INDEX['마침표'] = 3
        self.POS_INDEX['쉼표'] = 4
        self.POS_INDEX['따옴표'] = 5
        self.POS_INDEX['묶음표'] = 6
        self.POS_INDEX['이음표'] = 7
        self.POS_INDEX['드러냄표'] = 8
        self.POS_INDEX['안드러냄표'] = 9
        self.POS_INDEX['영문자'] = 10
        self.POS_INDEX['한자'] = 11
        self.POS_INDEX['기타기호'] = 12 
        self.POS_INDEX['숫자'] = 13
        self.POS_INDEX['미지기호'] = 14
        # 한글, 영문자, 한자,  숫자
        self.POS_NAME['한글'] = '한글'
        self.POS_NAME['자모'] = '자모'
        self.POS_NAME['영문자'] = '영문자'
        self.POS_NAME['한자'] = '한자'
        self.POS_NAME['숫자'] = '숫자'
        # 공백
        self.POS_NAME[' '] = '공백'
        self.POS_NAME['\r'] = '캐리지리턴'
        self.POS_NAME['\n'] = '라인피드'
        # 마침표
        self.POS_NAME['.'] = '온점'
        self.POS_NAME['?'] = '물음표'
        self.POS_NAME['!'] = '느낌표'
        # 쉼표
        self.POS_NAME[','] = '반점'
        self.POS_NAME['·'] = '가운뎃점'
        self.POS_NAME[':'] = '쌍점'
        self.POS_NAME['/'] = '빗금'
        # 따옴표
        self.POS_NAME['"'] = '큰따옴표'
        self.POS_NAME['\''] = '작은따옴표'
        # 묶음표
        self.POS_NAME['('] = '소괄호'
        self.POS_NAME['{'] = '중괄호'
        self.POS_NAME['['] = '대괄호'
        self.POS_NAME[')'] = '소괄호'
        self.POS_NAME['}'] = '중괄호'
        self.POS_NAME[']'] = '대괄호'
        # 이음표
        self.POS_NAME['─'] = '줄표'
        self.POS_NAME['-'] = '붙임표'
        self.POS_NAME['~'] = '물결표'
        self.POS_NAME['∼'] = '물결표'
        # 드러냄표
        self.POS_NAME['˙'] = '드러냄표'
        # 안드러냄표
        self.POS_NAME['×'] = '숨김표'
        self.POS_NAME['○'] = '숨김표'
        self.POS_NAME['□'] = '빠짐표'
        self.POS_NAME['…'] = '줄임표'
        # 기타기호
        self.POS_NAME['#'] = '샾'
        self.POS_NAME['$'] = '달러'
        self.POS_NAME['%'] = '퍼센트'
        self.POS_NAME['&'] = '앰퍼센드'
        self.POS_NAME['*'] = '곱하기'
        self.POS_NAME['+'] = '더하기'
        self.POS_NAME[';'] = '세미콜론'
        self.POS_NAME['<'] = '보다작다'
        self.POS_NAME['='] = '같다'
        self.POS_NAME['>'] = '보다크다'
        self.POS_NAME['@'] = '골벵이'
        # 미지기호
        self.POS_NAME['미지기호'] = '미지기호'
        # 공백
        self.POS_TYPE[' '] = '공백'
        self.POS_TYPE['\r'] = '공백'
        self.POS_TYPE['\n'] = '공백'
        # 마침표
        self.POS_TYPE['.'] = '마침표'
        self.POS_TYPE['?'] = '마침표'
        self.POS_TYPE['!'] = '마침표'
        # 쉼표
        self.POS_TYPE[','] = '쉼표'
        self.POS_TYPE['·'] = '쉼표'
        self.POS_TYPE[':'] = '쉼표'
        self.POS_TYPE['/'] = '쉼표'
        # 따옴표
        self.POS_TYPE['"'] = '따옴표'
        self.POS_TYPE['\''] = '따옴표'
        # 묶음표
        self.POS_TYPE['('] = '묶음표'
        self.POS_TYPE['{'] = '묶음표'
        self.POS_TYPE['['] = '묶음표'
        self.POS_TYPE[')'] = '묶음표'
        self.POS_TYPE['}'] = '묶음표'
        self.POS_TYPE[']'] = '묶음표'
        # 이음표
        self.POS_TYPE['─'] = '이음표'
        self.POS_TYPE['-'] = '이음표'
        self.POS_TYPE['~'] = '이음표'
        # 드러냄표
        self.POS_TYPE['˙'] = '드러냄표'
        # 안드러냄표
        self.POS_TYPE['×'] = '안드러냄표'
        self.POS_TYPE['○'] = '안드러냄표'
        self.POS_TYPE['□'] = '안드러냄표'
        self.POS_TYPE['…'] = '안드러냄표'
        # 기타기호
        self.POS_TYPE['#'] = '기타기호'
        self.POS_TYPE['$'] = '기타기호'
        self.POS_TYPE['%'] = '기타기호'
        self.POS_TYPE['&'] = '기타기호'
        self.POS_TYPE['*'] = '기타기호'
        self.POS_TYPE['+'] = '기타기호'
        self.POS_TYPE[';'] = '기타기호'
        self.POS_TYPE['<'] = '기타기호'
        self.POS_TYPE['='] = '기타기호'
        self.POS_TYPE['>'] = '기타기호'
        self.POS_TYPE['@'] = '기타기호'

    def get_true(self, type, c):
        i = self.POS_INDEX[type]
        return True, self.POS_TYPE_LIST[i], self.POS_NAME[c]

    def get_false(self):
        return False, '', ''
        
    def is_pos_xx(self, c): # 공백
        cr = unicode(u'\x0a')
        lf = unicode(u'\x0d')
        space = unicode(u'\x20')
        if c == cr or c == lf or c == space \
            or c == '\r' or c == '\n' or c == ' ':
            return self.get_true('공백', c)
        return self.get_false()

    def is_pos_hg(self, c): # 한글 ==> 가 ... 힣
        start_hanguel = unicode(u'\uac00')        # 가
        end_hanguel = unicode(u'\ud7a3')        # 힣
        if c >= start_hanguel and c <= end_hanguel:
            return self.get_true('한글', '한글')
        return self.get_false()

    def is_pos_jm(self, c):
        start_jamo = unicode(u'\u3131')        # ㄱ
        end_jamo = unicode(u'\u318c')        # ㆌ
        if c >= start_jamo and c <= end_jamo:
            return self.get_true('한글', '자모')
        return self.get_false()

    def is_pos_sf(self, c): # 마침표 ==> . ? !
        if c == '.' or c == '?' or c == '!':
            return self.get_true('마침표', c)
        return self.get_false()

    def is_pos_sp(self, c): # 쉼표 ==> , · : /
        middle_point = unicode(u'\xb7') # 가운뎃점(·)
        if c == ',' or c == ':' or c == '/':
            return self.get_true('쉼표', c)
        if c == middle_point:
            return self.get_true('쉼표', '·')
        return self.get_false()

    def is_pos_ss(self, c): # 따옴표 ==> ' "
        start_single_quote = unicode(u'\u2018') # ‘
        end_single_quote = unicode(u'\u2019')   # ’
        start_double_quote = unicode(u'\u201c') # “
        end_double_quote = unicode(u'\u201d')   # ”
        if c == '\'' or c == '"':
            return self.get_true('따옴표', c)
        if c == start_single_quote or c == end_single_quote:
            return self.get_true('따옴표', '\'')
        if c == start_double_quote or c == end_double_quote:
            return self.get_true('따옴표', '"')
        return self.get_false()

    def is_pos_sm(self, c): # 묶음표 ==> ( { [ ) } ]
        if c == '(' or c == '{' or c == '[' \
            or c == ')' or c == '}' or c == ']':
            return self.get_true('묶음표', c)
        return self.get_false()

    def is_pos_so(self, c): # 이음표 ==> － - ∼ ~
        concat = unicode(u'\uff0d')        # 붙임표(－)
        tild = unicode(u'\u223c')        # 물결표(∼)
        if c == '-' or c == '~':
            return self.get_true('이음표', c)
        if c == concat:
            return self.get_true('이음표', '-')
        if c == tild:
            return self.get_true('이음표', '~')
        return self.get_false()

    def is_pos_si(self, c): # 드러냄표 ˙
        exposure = unicode(u'\u02d9')   # 드러냄표(˙)
        if c == exposure:
            return self.get_true('드러냄표', '˙')
        return self.get_false()

    def is_pos_sj(self, c): # 안드러냄표 × ○ □ …
        hide_x = unicode(u'\xd7')        # 숨김표(×)
        hide_o = unicode(u'\u25cb')        # 숨김표(○)
        extract = unicode(u'\u25a1')        # 빠짐표(□)
        etc = unicode(u'\u2026')        # 줄임표(…)
        if c == hide_x:
            return self.get_true('안드러냄표', '×')
        if c == hide_o:
            return self.get_true('안드러냄표', '○')
        if c == extract:
            return self.get_true('안드러냄표', '□')
        if c == etc:
            return self.get_true('안드러냄표', '…')
        return self.get_false()

    def is_pos_sl(self, c): # 영문자
        if (c >= 'A' and c <= 'Z') or (c >= 'a' and c <= 'z'):
            return self.get_true('영문자', '영문자')
        return self.get_false()

    def is_pos_sh(self, c): # 한자
        start_hanja_1 = unicode(u'\u3400')
        end_hanja_1 = unicode(u'\u9fbb')
        start_hanja_2 = unicode(u'\uf900')
        end_hanja_2 = unicode(u'\ufaff')
        if (c >= start_hanja_1 and c <= end_hanja_1) \
            or (c >= start_hanja_2 and c <= end_hanja_2):
            return self.get_true('한자', '한자')
        return self.get_false()

    def is_pos_sw(self, c): # 기타기호 ===> # $ % & * + ; < = > @
        sharp = unicode(u'\x23')
        dollar = unicode(u'\x24')
        percent = unicode(u'\x25')
        ampersand = unicode(u'\x26')
        multiply = unicode(u'\x2a')
        plus = unicode(u'\x2b')
        semicolon = unicode(u'\x3b')
        lessthan = unicode(u'\x3c')
        equal = unicode(u'\x3d')
        greaterthan = unicode(u'\x3e')
        at = unicode(u'\x40')
        if c == sharp or c == dollar or c == percent \
            or c == ampersand or c == multiply \
            or c == plus or c == semicolon \
            or c == lessthan or c == equal \
            or c == greaterthan or c == at:
            return self.get_true('기타기호', c)
        return self.get_false()
        
    def is_pos_sn(self, c): # 숫자
        start_num = unicode(u'\x30')
        end_num = unicode(u'\x39')
        if (c >= '0' and c <= '9') or \
            (c >= start_num and c <= end_num):
            return self.get_true('숫자', '숫자')
        return self.get_false()

    def is_pos_uk(self, c): # 미지기호 ==> ‰ ‱   ※ ... ⵥ
        start_xx = unicode(u'\u202f')
        end_xx = unicode(u'\u2e7f')
        if c >= start_xx and c <= end_xx:
            return self.get_true('미지기호', '미지기호')
        return self.get_false()

    def is_pos_type(self, s):
        return s in self.POS_TYPE_LIST

    # default value: 기호
    def name_of_type(self, token):
        s = token.value
        if s in self.POS_TYPE:
            return self.POS_TYPE[s]
        if token.part_of_type in ['한글', '영문자', '한자']:
            return '문자'
        if len(token.part_of_type.strip()) == 0:
            return '기호'
        return token.part_of_type

    # default value: 미지기호
    def name_of_pos(self, token):
        s = token.value
        if s in self.POS_NAME:
            return self.POS_NAME[s]
        if len(token.part_of_speech.strip()) == 0:
            return '미지기호'
        return token.part_of_speech

class Formatter(object):
    def printUsage(message, length=60):
        print '\n' + '=' * length
        print message
        print '=' * length + '\n'

    print_usage = staticmethod(printUsage)


class Reader(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        try:
            self.file = open(self.filename)
            for line in self.file:
                print line.strip()
            self.file.close()
        except:
            raise

class Logger(object):
    def _info(*args):
        buf = ''
        for i in xrange(0, len(args)):
            buf += str(args[i]) + ' '
        print '[Info]', buf[0:-1]

    def _debug(*args):
        env = os.environ.get("DEBUG")
        if env != None and env == 'True':
            buf = ''
            for i in xrange(0, len(args)):
                buf += str(args[i]) + ' '
            print '[Debug]', buf[0:-1]

    def _error(*args):
        buf = ''
        for i in xrange(0, len(args)):
            buf += str(args[i]) + ' '
        print '[Error]', buf[0:-1]

    info = staticmethod(_info)
    debug = staticmethod(_debug)
    error = staticmethod(_error)
