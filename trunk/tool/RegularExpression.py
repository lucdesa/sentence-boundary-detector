#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
s="<idno>BGAA0001.txt, 형태분석:BTAA001.txt, 원본:BRAA0001.txt </idno>"
p = re.compile(".*?, 원본:([A-Z]*[0-9]*\.txt) \</idno\>$")
m = p.match(s)
if m != None:
    print "/home/psyoblade/workspace/corpus/sejong/sentence/원시말뭉치/" + m.groups()[0]
