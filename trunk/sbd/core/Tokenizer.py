#!/usr/bin/env python
# -*- coding:utf-8 -*-

import re
import Token as token
import sbd.util.Util as util

class Tokenizer:
    def __init__(self):
        self.tokens = []
        self.util = util.Common()

    def __del__(self):
        self.clear()

    def clear(self):
        del self.tokens[:]

    def parse(self, eojeol): # 어절단위 유니코드 파싱
        util = self.util
        POS_FUNC = [ \
            util.is_pos_xx, util.is_pos_hg, util.is_pos_jm, \
            util.is_pos_sf, util.is_pos_sp, util.is_pos_ss, \
            util.is_pos_sm, util.is_pos_so, util.is_pos_si, \
            util.is_pos_sj, util.is_pos_sl, util.is_pos_sh, \
            util.is_pos_sw, util.is_pos_sn, util.is_pos_uk ]
        list = []
        prevToken = ''
        prevType = ''
        prevPos = ''
        for c in unicode(eojeol, 'utf-8'):
            for i in range(0, len(POS_FUNC)):
                RESULT, currType, currPos = POS_FUNC[i](c)
                if RESULT:
                    if len(prevType) > 0 and len(prevPos) > 0:
                        if prevPos == currPos:
                            # 공백의 경우는 하나만 유지한다. 공백 = { CR, LF, SP }
                            prevToken += c
                            continue
                        else:
                            list.append((prevToken, prevType, prevPos))
                            prevToken = c
                            prevType = currType
                            prevPos = currPos
                    else:
                        prevToken = c
                        prevType = currType
                        prevPos = currPos
        list.append((prevToken, prevType, prevPos))
        return list

    def stokenize(self, stream):
        id = 0
        tokens = self.tokens
        space = ' '
        crlf = '\n'
        for line in stream.split('\n'):
            # 1. 문장의 처음/끝 공백제거
            # 1. 공백라인은 스킵
            line = line.strip()
            if len(line) == 0: continue
            eojeols = re.split(r'[\s]+', line.strip())
            ej_index = 0
            for eojeol in eojeols:
                _eos = False # end_of_sentence
                if ej_index+1 == len(eojeols):
                    _eos = True
                parsed_eojeol = self.parse(eojeol)
                eojeol_size = len(parsed_eojeol)
                for index, (word, type, pos) in enumerate(parsed_eojeol):
                    util.Logger.debug(id, word.encode('utf-8'), pos)
                    eoe = False # end_of_eojeol
                    eos = False # end_of_sentence
                    if index+1 == eojeol_size:
                        eoe = True
                        eos = _eos
                    else:
                        eos = False
                        util.Logger.debug(word.encode('utf-8')+'/'+type+'-'+pos, eoe, eos)
                    tokens.append(token.Token(id, word.encode('utf-8'), type, pos, eoe, eos))
                    id += 1
                    index += 1
                ej_index += 1
        return tokens

    def tokenize(self, file):
        id = 0
        tokens = self.tokens
        space = ' '
        crlf = '\n'
        for line in file:
            # 1. 문장의 처음/끝 공백제거
            # 1. 공백라인은 스킵
            line = line.strip()
            if len(line) == 0: continue
            eojeols = re.split(r'[\s]+', line.strip())
            ej_index = 0
            for eojeol in eojeols:
                _eos = False # end_of_sentence
                if ej_index+1 == len(eojeols):
                    _eos = True
                parsed_eojeol = self.parse(eojeol)
                eojeol_size = len(parsed_eojeol)
                for index, (word, type, pos) in enumerate(parsed_eojeol):
                    util.Logger.debug(id, word.encode('utf-8'), pos)
                    eoe = False # end_of_eojeol
                    eos = False # end_of_sentence
                    if index+1 == eojeol_size:
                        eoe = True
                        eos = _eos
                    else:
                        eos = False
                        util.Logger.debug(word.encode('utf-8')+'/'+type+'-'+pos, eoe, eos)
                    tokens.append(token.Token(id, word.encode('utf-8'), type, pos, eoe, eos))
                    id += 1
                    index += 1
                ej_index += 1
        file.close()
        return tokens

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "python Tokenizer.py filename"
        print "python Tokenizer.py /home/psyoblade/workspace/corpus/sejong/tagged/raws/Spoken/Quasi/1/AH000475.TMP.raws"
        sys.exit()
    tokenizer = Tokenizer()
    file = open(sys.argv[1])
    for token in tokenizer.tokenize(file):
        token.debug()
    file.close()

