#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Token import Token

class Document:
    def __init__(self):
        self.id = -1
        self.tokens = []

    def parse(self):
        pass

    def add(self, token):
        self.tokens.append(token)

    def length(self):
        return len(self.tokens)

    def token(self, id):
        tokens = self.tokens
        if id < 0 or len(tokens) <= id:
            return Token()
        return tokens[id]

    def prev(self, id):
        tokens = self.tokens
        prev = id-1
        if prev < 0 or len(tokens) <= prev:
            return Token()
        return tokens[prev]

    def next(self, id):
        tokens = self.tokens
        next = id+1
        if next < 0 or len(tokens) <= next:
            return Token()
        return tokens[next]

    def prevPunctuationDist(self, id):
        tokens = self.tokens
        dist = 0
        prev = id-1
        while prev >= 0 and len(tokens) > prev:
            if tokens[prev].isPunctuation(True): break
            dist += 1
            prev = id-dist
        if dist <= 0: return 0
        return dist-1

    def nextPunctuationDist(self, id):
        tokens = self.tokens
        dist = 0
        next = id+1
        while next >= 0 and len(tokens) > next:
            if tokens[next].isPunctuation(True): break
            dist += 1
            next = id+dist
        if dist <= 0: return 0
        return dist-1

    def prevCandidateDist(self, id):
        tokens = self.tokens
        dist = 0
        prev = id-1
        while prev >= 0 and len(tokens) > prev:
            if tokens[prev].isCandidate(): break
            dist += 1
            prev = id-dist
        if dist <= 0: return 0
        return dist-1

    def nextCandidateDist(self, id):
        tokens = self.tokens
        dist = 0
        next = id+1
        while next >= 0 and len(tokens) > next:
            if tokens[next].isCandidate(): break
            dist += 1
            next = id+dist
        if dist <= 0: return 0
        return dist-1

