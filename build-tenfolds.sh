#!/bin/bash

function print_usage {
    echo './build-tenfolds.sh [sejong|pentree] [split|folding] [inputpath]'
    echo './build-tenfolds.sh sample split tenfolds'
    echo './build-tenfolds.sh sample folding tenfolds'
    echo './build-tenfolds.sh sejong split tenfolds'
    echo './build-tenfolds.sh sejong folding tenfolds'
    echo './build-tenfolds.sh pentree split tenfolds'
    echo './build-tenfolds.sh pentree folding tenfolds'
}

function split() {
    CORPUS=$1
    INPUT=$2
    python Split.py corpus/$CORPUS/$CORPUS.raw tenfolds/$CORPUS 10
}

function folding() {
    CORPUS=$1
    INPUT=$2
    python Folder.py corpus/$CORPUS/$CORPUS.raw tenfolds/$CORPUS 10 random
}

if [ $# != 3 ]; then
    print_usage
    exit
fi

CORPUS=$1
TARGET=$2
INPUT=$3

if [ $TARGET == 'split' ]; then
    split $CORPUS $INPUT
elif [ $TARGET == 'folding' ]; then
    folding $CORPUS $INPUT
else
    print_usage
    exit
fi
