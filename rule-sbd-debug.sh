#!/bin/bash
if [ $# == 1 ]; then
    filelist=`ls Sejong`
    target=$1
    for filename in $filelist; do
        echo "$filename is processing..."
        python RuleBasedSBD.py "Sejong/$filename" $target > "Result/$filename"
    done
else
    echo './rule-sbd-debug.sh [debug-tn|debug-fp]'
fi
