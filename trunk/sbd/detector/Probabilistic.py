#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sbd.util.Util as util
import sbd.core.Token as token


class Probabilistic:
    def __init__(self):
        pass

    def simplify_prob(self, prob):
        if prob == '?':
            return prob
        else:
            return float(prob) * 10 // 1

    def add_maxent_parameter(self, buf, i, property):
        i += 1
        buf += ' ' + str(i) + ':' + str(property)
        return (buf, i)

    def add_weka_parameter(self, buf, property):
        if type(property) == str and len(property.strip()) == 0:
            property = '?'
        buf += str(property) + ','
        return buf

    def detect(self, document, dict, classifier=util.Common.MAXENT, syllable_length=0, merged_use=False):
        common = util.Common()
        # finding sentence boundary candidate
        for id in range(document.length()):
            currToken = document.token(id)
            # if True: # 2008.10.13, 문장경계후보를 모든 위치로 변경  currToken.isEoe(): # end-of-sentecne candidate
            # default token value
            if classifier == util.Common.MAXENT: default = '_'
            elif classifier == util.Common.WEKA: default = '?'
            else: default = '_'
            # name_of_type() is defined only for special characters
            prevToken = document.prev(id)
            nextToken = document.next(id)
            if util.Common.DEBUG:
                print "\t", "id:", id, prevToken.value, currToken.value, nextToken.value
                print prevToken.id, prevToken.value, currToken.id, currToken.value, nextToken.id, nextToken.value
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

            buf = ''
            i = 0
            # { building instances }
            if classifier == util.Common.MAXENT:
                buf = end_of_sentence
                (buf, i) = self.add_maxent_parameter(buf, i, current_pos_type)
                (buf, i) = self.add_maxent_parameter(buf, i, current_pos_name)
                (buf, i) = self.add_maxent_parameter(buf, i, prefix_pos_type)
                (buf, i) = self.add_maxent_parameter(buf, i, prefix_pos_name)
                (buf, i) = self.add_maxent_parameter(buf, i, suffix_pos_type)
                (buf, i) = self.add_maxent_parameter(buf, i, suffix_pos_name)
                # XXX: maxent use NAME instead of PROBABILITY
                for length in xrange(syllable_length):
                    (buf, i) = self.add_maxent_parameter(buf, i, prefix_syllable_name[length])
                    (buf, i) = self.add_maxent_parameter(buf, i, suffix_syllable_name[length])
                    if merged_use:
                        (buf, i) = self.add_maxent_parameter(buf, i, merged_syllable_name[length])
                (buf, i) = self.add_maxent_parameter(buf, i, current_token_name)
                (buf, i) = self.add_maxent_parameter(buf, i, prefix_token_name)
                (buf, i) = self.add_maxent_parameter(buf, i, suffix_token_name)
                (buf, i) = self.add_maxent_parameter(buf, i, str(current_token_length))
                (buf, i) = self.add_maxent_parameter(buf, i, str(prefix_token_length))
                (buf, i) = self.add_maxent_parameter(buf, i, str(suffix_token_length))

                print buf

            elif classifier == util.Common.WEKA:
                buf = self.add_weka_parameter(buf, current_pos_type)
                buf = self.add_weka_parameter(buf, current_pos_name)
                buf = self.add_weka_parameter(buf, prefix_pos_type)
                buf = self.add_weka_parameter(buf, prefix_pos_name)
                buf = self.add_weka_parameter(buf, suffix_pos_type)
                buf = self.add_weka_parameter(buf, suffix_pos_name)
                # XXX: maxent use PROBABILITY instead of NAME 
                for length in xrange(syllable_length):
                    buf = self.add_weka_parameter(buf, prefix_syllable_prob[length])
                    buf = self.add_weka_parameter(buf, suffix_syllable_prob[length])
                    if merged_use:
                        buf = self.add_weka_parameter(buf, merged_syllable_prob[length])
                buf = self.add_weka_parameter(buf, current_token_prob)
                buf = self.add_weka_parameter(buf, prefix_token_prob)
                buf = self.add_weka_parameter(buf, suffix_token_prob)
                buf = self.add_weka_parameter(buf, current_token_length)
                buf = self.add_weka_parameter(buf, prefix_token_length)
                buf = self.add_weka_parameter(buf, suffix_token_length)
                buf += end_of_sentence

                print buf

            else:
                print 'Invalid classifier selected : ' + classifier
                assert(False)


    def debug(self, document, maxent_use=False, skip_print=False):
        common = util.Common()
        buff = ''
        skip_buff = ''
        # finding sentence boundary candidate
        for id in range(document.length()):
            token = document.token(id)
            buff += token.value
            # append tag {<EOS>,<TN>,<FP>}, except <FN>
            # if True: # 2008.10.13, 문장 경계후보를 모든 위치로 변경 token.isEoe():
            tag = ''
            prevToken = document.prev(id)
            nextToken = document.next(id)
            answer = token.end_of_sentence
            if answer:
                tag = '<EOS>'
            elif answer == True:
                tag = '<TN>'
            elif answer == False:
                tag = '<FP>'
            else:
                continue
            buff += tag + '\n'
            if skip_print:
                if tag == '<TN>' or tag == '<FP>':
                    skip_buff += buff
                    buff = ''
                elif tag == '<EOS>':
                    buff = ''
            else:
                if token.end_of_eojeol:
                    buff += ' '
        if skip_print:
            print skip_buff
        else:
            print buff

    def statinfo(self, document, pattern):
        common = util.Common()
        line = ''
        # finding sentence boundary candidate
        for id in range(document.length()):
            curr = document.token(id)
            prev = document.prev(id)
            next = document.next(id)
            # 어절찾기 : end_of_eojeol == True and end_of_sentence == False
            # 문장찾기 : end_of_eojeol == True and end_of_sentence == True
            # " + 공백 + 어절 -> 어절출력
            line += curr.raw
            if curr.end_of_sentence:
                line += '\n'
            elif curr.value == '"' and next.value == '"' and curr.end_of_eojeol:
                line += '\n'
            elif curr.end_of_eojeol:
                line += ' '
        print line
