#!/bin/bash

function print_usage() {
    echo './build-maxent-model.sh [sejong|pentree] [all|learn|eval]'
    echo './build-maxent-model.sh sejong all'
    echo './build-maxent-model.sh pentree all'
}

if [ $# != 2 ]; then
    print_usage
    exit
fi

CORPUS=$1
FUNC=$2
CLASSIFIER="maxent"
TENFOLDS="tenfolds"

if [ "$FUNC" == "all" ] || [ "$FUNC" == "learn" ]; then
    # Building models
    for I in $(seq 0 9); do
        maxent -v -mmodel/$CORPUS.$CLASSIFIER.$I.model -i200 -g3.5 $CLASSIFIER/$CORPUS.$I.maxent > log/$CORPUS/$CORPUS.$CLASSIFIER.$I.out
    done
fi
if [ "$FUNC" == "all" ] || [ "$FUNC" == "eval" ]; then
    # Evaluating result
    RESULT="result/$CORPUS.$CLASSIFIER"
    rm -rf $RESULT.tmp
    for I in $(seq 0 9); do
        if [ "$CORPUS" == "sejong" ]; then
            python MaxentBasedSBD.py dict/$CORPUS model/$CORPUS.$CLASSIFIER.$I.model 1 yes no 0.8 $TENFOLDS/$CORPUS/$I.evals eval >> $RESULT.tmp
        elif [ "$CORPUS" == "pentree" ]; then
            python MaxentBasedSBD.py dict/$CORPUS model/$CORPUS.$CLASSIFIER.$I.model 0 no yes 0.8 $TENFOLDS/$CORPUS/$I.evals eval >> $RESULT.tmp
        else
            python MaxentBasedSBD.py dict/$CORPUS model/$CORPUS.$CLASSIFIER.$I.model 1 yes no 0.8 $TENFOLDS/$CORPUS/$I.evals eval >> $RESULT.tmp
        fi
    done
    python MergeResult.py $RESULT.tmp
fi
