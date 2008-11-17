#!/bin/bash

if [ $# != 1 ]; then
    echo './eval-tenfolds.sh [sejong|pentree]'
else
    corpus=$1
    # Learning n times
    for i in $(seq 0 9); do
        maxent -v -mmodel/maxent-$i.model -i200 -g3.5 tenfolds/$corpus/$i.learn > log/$corpus/$i.out
    done
    # Evaluating result
    result="result/tenfolds-$corpus"
    rm -rf "$result.*"
    # Evaluating n times
    for i in $(seq 0 9); do
        python MaxentBasedSBD.py model/maxent-$i.model 0 no yes 0.8 tenfolds/$corpus/$i.eval eval >> $result.tmp
    done
    cat $result.tmp | LC_ALL=0 sort | LC_ALL=0 uniq -c | LC_ALL=0 sort -n -r > $result.out
    python MergeResult.py $result.out
fi
