#!/bin/bash
filelist=`ls 10folds/sequential/*.orgn`
tempfile=`date +%Y%m%d_%H%M`
rm -rf $tempfile
for filename in $filelist; do
    echo "$filename is processing..."
    python RuleBasedSBD.py "$filename" eval >> $tempfile
done
cat $tempfile | LC_ALL=0 sort | LC_ALL=0 uniq -c | LC_ALL=0 sort -n -r > $tempfile.out
python Evaluator.py $tempfile.out
