#!/usr/bin/env python
# -*- coding:utf-8 -*-

class Heuristic:
    def __init__(self):
        pass

    def detect(self, document, dict=None, classifier=None, syllable_length=0, merged_use=False):
        # finding sentence boundary candidate
        for id in range(document.length()):
            token = document.token(id)
            prevToken = document.prev(id)
            nextToken = document.next(id)
            eos = 'no'
            if token.isCandidate():
                if self.check(prevToken, token, nextToken):
                    eos = 'yes'
            sys.stdout.write(token.value)
            sys.stdout.write(eos)

    def debug(self):
        pass

    def evaluate(self):
        pass

    def statinfo(self):
        pass

    def check(self, prev, curr, next):
        if prev.isNumeric() and curr.isPeriod():        # Rule.1
            return False
        elif prev.isEnglish() and curr.isPeriod():        # Rule.5
            return False
        elif curr.isCandidate() and next.isSpecial():        # Rule.6
            return False
        elif curr.isCandidate() and curr.end_of_eojeol:
            return True
        elif curr.isPeriod() and next.isQuote():
            return True
        elif prev.isPeriod() and curr.isQuote():
            return False
        elif prev.isQuestion() and curr.isQuote():
            return True
        elif prev.length <= 3 and curr.isExclamation():
            return False
        elif curr.isQuote():
            return False
#        elif curr.isCandidate() and next.isQuote():        # Rule.2
#            return False 
#        elif prev.value == curr.value:                        # Rule.3
#            return False
#        elif (prev.isHanguel() and prev.length == 1 and not prev.isCandidate()) \
#            and curr.isCandidate():                        # Rule.4
#            return False
        return True

"""
    Examples
    1. 한글, 영어, 한자, 숫자, 특수문자 등을 기준으로 문서를 토크나이징
    2. 한글 코퍼스의 경우 5개의 구두점{ . ! ? ' " }을 기준으로 문장경계 후보로 판단
        1. PERIOD : 마침표
        2. QUESTION : 물음표
        3. EXCLAMATION : 느낌표
        4. SINGLE QUOTE : 단일 인용부호
        5. DOUBLE QUOTE : 이중 인용부호
    3. 문장경계가 아니라고 판단되는 경우 , []가 현재 토큰
        1. 숫자 + [PERIOD]
            1. 중략 [조선일보 1984. 9. 27] 이러한 논평을 통해서도 우리는
            2. 12.2:1입니다.
            3. 4. 毛 皮 면섬유는 물을 흡수함에 따라 팽윤하고 섬유의 斷面은 점점 둥글어진다.
        2. [CANDIDATE] + QUOTE
            1. ‘참!’ ‘점을 찍는 걸 깜박 잊어버렸지 뭐야.’
        3. [CANDIDATE] + [CANDIDATE]
            1. 충분히 반영하는...
        4. 1음절 + [CANDIDATE]
            1. 주최한 한.중.일 3국의
            2. 예. 아까 영화
            3. 아! 네. 최시형 씨와 친구 분이십니다.
            4. 초기에는 매춘부들이나 금.은사로 만든 것을 입었으며 보통 여성들에게는 19세기까지 일상복이 되지 못하였다.
        5. 영문 + [PERIOD]
            1. 저는 자기는 P.D가 되고 싶대요.
            2. 1960년대의 큰 회사 벌링톤(Burlington)과 J.P. Stevens라는 미국회사에서 최초로 토탈패션 룩을 만들었다.
        6. [CANDIDATE] + 특수문자
            1. 또한 점이 위치한 방향으로 각이 이끌리는 것과 같이 느낀다.(그림 3-28 참조) 流行과 變化의 관계는 오랫동안 인식되어 왔다.
"""
