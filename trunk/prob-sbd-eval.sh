#!/bin/bash
if [ $# != 3 ]; then
    echo "./prob-sbd-eval.sh [skip-count] [exec-count] [arffname]"
    echo "./prob-sbd-eval.sh 0 1 temp"
    exit
fi
SKIP=$1
EXEC=$2
ARFF=$3

# generating answer arff
python sbd/util/Directory.py /home/psyoblade/workspace/corpus/sejong/tagged/raws raws $SKIP $EXEC SentenceBoundaryDetector.py build-arff > weka/${ARFF}_.arff
cat weka/header_.arff > weka/$ARFF.arff
cat weka/${ARFF}_.arff >> weka/$ARFF.arff

# testing arff
J48="sbd/weka"
jython $J48/J48.py $J48/model/j48.model weka/${ARFF}.arff > test/${ARFF}.test

# printing tagged document
python sbd/util/Directory.py /home/psyoblade/workspace/corpus/sejong/tagged/raws raws $SKIP $EXEC SentenceBoundaryDetector.py prob-sbd-eval test/${ARFF}.test
