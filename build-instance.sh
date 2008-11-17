#!/bin/bash

function print_usage() {
    echo 'Usage: ./build-instance.sh [corpus-name] [input-path] [dict-path] [syllable-length] [merged-yn] [ignore-case] [weka|maxent]'
    echo './build-instance.sh sample tenfolds dict/sample 1 yes no weka'
    echo './build-instance.sh sample tenfolds dict/sample 1 yes no maxent'
    echo './build-instance.sh sejong tenfolds dict/sejong 1 yes no weka'
    echo './build-instance.sh sejong tenfolds dict/sejong 1 yes no maxent'
    echo './build-instance.sh pentree tenfolds dict/pentree 0 no yes weka'
    echo './build-instance.sh pentree tenfolds dict/pentree 0 no yes maxent'
}    

if [ $# == 7 ]; then
    CORPUS=$1
    INPUT=$2
    DICT=$3
    SYLLABLE_SIZE=$4
    MERGED=$5
    IGNORE_CASE=$6
    CLASSIFIER=$7

    # 학습용 파일생성 weka는 하나만 있어도 10폴드가능, 단 여러개의 분류기 학습
    if [ $CLASSIFIER == weka ]; then
        rm -rf $CLASSIFIER/$CORPUS.raws
        FILENAMEs=`ls $INPUT/$CORPUS/*.split`
        for FILENAME in $FILENAMEs; do
            echo "processing $FILENAME ..."
            python Learner.py $DICT $CLASSIFIER build $SYLLABLE_SIZE $MERGED $IGNORE_CASE $FILENAME >> $CLASSIFIER/$CORPUS.raws
        done
    # 10폴드를 위해서 학습집합을 10개, 물론 모델도 10개 생성
    elif [ $CLASSIFIER == maxent ]; then 
        rm -rf $CLASSIFIER/$CORPUS.?.raws
        FILENAMEs=`ls $INPUT/$CORPUS/*.learn`
        I=0
        for FILENAME in $FILENAMEs; do
            echo "processing $FILENAME ..."
            echo "python Learner.py $DICT $CLASSIFIER build $SYLLABLE_SIZE $MERGED $IGNORE_CASE $FILENAME > $CLASSIFIER/$CORPUS.$I.raws"
            let "I++"
        done
    else
        print_usage
    fi

    if [ $CLASSIFIER == weka ]; then
        if [ $SYLLABLE_SIZE -gt 0 ]; then
            cat $CLASSIFIER/use_syllable.header > $CLASSIFIER/$CORPUS.arff
            cat $CLASSIFIER/$CORPUS.raws >> $CLASSIFIER/$CORPUS.arff
        else
            cat $CLASSIFIER/nouse_syllable.header > $CLASSIFIER/$CORPUS.arff
            cat $CLASSIFIER/$CORPUS.raws >> $CLASSIFIER/$CORPUS.arff
        fi
    elif [ $CLASSIFIER == maxent ]; then
        for I in $(seq 0 9); do 
            mv $CLASSIFIER/$CORPUS.$I.raws $CLASSIFIER/$CORPUS.$I.maxent
        done
    else
        print_usage
        exit
    fi
else
    print_usage
    exit
fi

