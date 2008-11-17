#!/bin/bash

function print_usage() {
    echo "./dist.sh [TARGET] [DESTINATION-PATH]"
    echo "TARGET: rule | ml"
    echo "EXAMPLES: ./dist.sh rule ../rule-based-sbd"
    echo "EXAMPLES: ./dist.sh ml ../ml-based-sbd"
}

if [ $# != 2 ]; then
    print_usage
    exit
fi

TARGET=$1
DESTPATH=$2
MODELS="j48 libsvm maxent"
CORPUS="pentree sejong"                        # sejong-tagged
METHODS="maxent weka"
CP="rsync -a --exclude *.pyc --exclude *.raws --exclude *.model --exclude *.out --exclude *.split --exclude *.arff --exclude *.maxent --exclude *.orgn --exclude *.learn --exclude *.evals --exclude *.result"
MKDIR="mkdir -p"

if [ "$TARGET" == "rule" ]; then
    # core
    $CP sbd $DESTPATH
    $CP README $DESTPATH
    # tool
    $CP Split.py $DESTPATH
    $CP Tokenizer.py $DESTPATH
    # corpus
    $CP tenfolds $DESTPATH
    # evaluating 
    $CP RuleBasedSBD.py $DESTPATH
    echo "dist '$TARGET' completed"

elif [ "$TARGET" == "ml" ]; then
    # core
    $CP sbd $DESTPATH
    $CP log $DESTPATH
    $CP jar $DESTPATH
    $CP result $DESTPATH
    $CP README $DESTPATH
    # learning methods
    for METHOD in $METHODS; do
        $CP $METHOD $DESTPATH
    done
    # corpus
    for C in $CORPUS; do
        $CP -R corpus/$C $DESTPATH
        $CP -R tenfolds/$C $DESTPATH
    done
    # building
    $CP Tokenizer.py $DESTPATH
    $CP Builder.py $DESTPATH
    $CP build-all.sh $DESTPATH
    $CP build-dict.sh $DESTPATH
    $CP build-tenfolds.sh $DESTPATH
    $CP dict $DESTPATH
    # learning
    $CP Learner.py $DESTPATH
    $CP build-instance.sh $DESTPATH
    $CP build-weka-model.sh $DESTPATH
    $CP build-maxent-model.sh $DESTPATH
    # evaluating
    $CP Evaluator.py $DESTPATH
    $CP Split.py $DESTPATH
    $CP Folder.py $DESTPATH
    $CP MergeResult.py $DESTPATH
    # model
    for model in $MODELS; do
        $CP -R model/$model.model $DESTPATH
    done
    # weka
    if [ ! -d $DESTPATH/jar ]; then
        mkdir $DESTPATH/jar;
    fi
    $CP /home/psyoblade/workspace/java/weka/dist/weka.jar $DESTPATH/jar/weka.jar
    $CP /home/psyoblade/workspace/WLSVM/lib/libsvm.jar $DESTPATH/jar/libsvm.jar
    # main
    $CP MaxentBasedSBD.py $DESTPATH
    $CP StatExtractor.py $DESTPATH
    # etc
    $CP tool $DESTPATH
    echo "dist '$TARGET' completed"
else
    print_usage
fi
