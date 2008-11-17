#!/usr/bin/env python
# -*- coding:utf-8 -*-
import time
import sys
import os
import re
yes_filter=['(S']#, '(VP', '(NP'] #문장, 동사구, 명사구
def filter(value):
    single_quotes=['‘','’','`','「','」']
    double_quotes=['“','”','『','』']
    for quote in single_quotes:
	value = value.replace(quote, '\'')
    for quote in double_quotes:
	value = value.replace(quote, '"')
    value = value.replace('。', '.')
    value = value.replace('、', ',')
    return value
def is_yes_filter(value):
    for filter in yes_filter:
	if value.startswith(filter):
	    return True
    return False
if len(sys.argv) == 2:
    filename=sys.argv[1]
    file = open(filename)
    buff = ''
    for line in file:
	line = filter(line.strip())
	if buff != '' and is_yes_filter(line):
	    print buff
	    buff = ''
	    continue
	if line[0:1] != ';':
	    continue
	buff = line[2:]
    file.close()
else:
    print len(sys.argv)
    print "세종구문분석 코퍼스에서 특수문자 필터링과 문장추출"
    print "python Conversion.py filename"
