#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from collections import defaultdict

class Dictionary:
    def __init__(self, path):
        self.path = path
        self.dictionaries = defaultdict(dict)

    def init(self, dictname):
        dict = defaultdict(int)
        self.dictionaries[dictname] = dict

    def load(self, dictname):
        try:
            dictpath = os.path.join(self.path, str(dictname) + '.dict')
            dict = defaultdict(int)
            file = open(dictpath)
            for line in file:
                value, key = line.strip().split(' ')
                dict[key] = value
            file.close()
            self.dictionaries[str(dictname)] = dict
        except:
            raise

    def build(self, path):
        pass

    def search(self, dictname, key):
        dicts = self.dictionaries
        if dictname in dicts:
            dict = dicts[dictname]
            if key in dict:
                return dict[key]
        return None

    def getProbOfDict(self, dict, section, key):
        eosKey = section + "_True_" + str(key)
        nosKey = section + "_False_" + str(key)
        yesStat = 0.0
        eosFreq = 0.0
        nosFreq = 0.0
        if eosKey in dict: eosFreq = int(dict[eosKey]) * 1.0
        if nosKey in dict: nosFreq = int(dict[nosKey]) * 1.0
        if eosFreq > 0 or nosFreq > 0:
            yesStat = eosFreq / (eosFreq + nosFreq)
        if yesStat == 0.0:
            return "0.0"
        else:
            return str(yesStat)

    def getPrefixSyllableProb(self, key, size=1):
        dict = self.dictionaries['syllable']
        key = str(size) + '_' + key
        return self.getProbOfDict(dict, 'prefix', key)

    def getSuffixSyllableProb(self, key, size=1):
        dict = self.dictionaries['syllable']
        key = str(size) + '_' + key
        return self.getProbOfDict(dict, 'suffix', key)

    def getMergedSyllableProb(self, key, size=1):
        dict = self.dictionaries['syllable']
        key = str(size) + '_' + key
        return self.getProbOfDict(dict, 'merged', key)

    def getCurrentTokenProb(self, key):
        dict = self.dictionaries['token']
        return self.getProbOfDict(dict, 'current', key)

    def getPrefixTokenProb(self, key):
        dict = self.dictionaries['token']
        return self.getProbOfDict(dict, 'prefix', key)

    def getSuffixTokenProb(self, key):
        dict = self.dictionaries['token']
        return self.getProbOfDict(dict, 'suffix', key)

if __name__ == '__main__':
    try:
        dictpath = 'dict'
        d = Dictionary(dictpath)
        d.load('syllable')
        d.load('token')
        print d.search('syllable', 'prefix_True_1_다')
        print d.search('token', 'prefix_True_다')
        print d.getPrefixSyllableProb('다')
        print d.getPrefixTokenProb('다')
    except:
        import traceback
        traceback.print_exc(file=sys.stderr)
