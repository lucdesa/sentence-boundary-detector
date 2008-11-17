#!/bin/bash

function print_usage() {
    echo './build-dict.sh [rawfile-path] [dictfile-path] [syllable-length] [merged-yn] [ignore-case]'
    echo './build-dict.sh sample tenfolds dict/sample 1 yes no'
    echo './build-dict.sh sejong tenfolds dict/sejong 1 yes no'
    echo './build-dict.sh pentree tenfolds dict/pentree 0 no yes'
}

if [ $# == 6 ]; then
    corpus=$1
    rawfile_path=$2
    dictfile_path=$3
    syllable_length=$4
    merged_yn=$5
    ignore_case=$6
    
    rm -rf $dictfile_path/*.temp
    rm -rf $dictfile_path/*.raws
    rm -rf $dictfile_path/*.dict

    filenames=`ls $rawfile_path/$corpus/*.split`
    for filename in $filenames; do
        echo "processing $filename ..."
        python Builder.py $filename $dictfile_path $syllable_length $merged_yn $ignore_case
    done

    cd $dictfile_path
    dicts='token syllable type length'
    for dict in $dicts; do
        cat ${dict}.raws | LC_ALL=0 sort | LC_ALL=0 uniq -c | LC_ALL=0 sort -r > ${dict}.dict
    done
else
    print_usage
    exit
fi


