#!/bin/bash
if [ $# != 2 ]; then
    echo './merge.sh split sejong.raw'
    exit
else
    ext=$1
    out=$2
    rm -rf $outputfile
    filenames=`ls *.$ext`
    for filename in $filenames; do
	cat $filename >> $out
    done
fi
