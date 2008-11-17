#!/bin/bash
# read all files from Sentence, remove tags and conversion 2byte character to 1byte
filenames=`ls Sentence`
for filename in $filenames; do
    python tool/Conversion.py "Sentence/$filename" > "Sejong/$filename"
done
