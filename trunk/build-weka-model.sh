#!/bin/bash

function print_usage() {
    echo './build-weka-model.sh [sejong|pentree] [all|learn|eval]'
    echo './build-weka-model.sh sejong all'
    echo './build-weka-model.sh pentree all'
}

if [ $# != 2 ]; then
    print_usage
    exit
fi
# libsvm:   /home/psyoblade/workspace/WLSVM/lib/libsvm.jar
# mysql:    /usr/local/mysql-jdbc/mysql-connector-java-5.0.8-bin.jar
export CLASSPATH=$CLASSPATH:jar/weka.jar:jar/libsvm.jar

JAVA="java -Xmx2048m -classpath jar/weka.jar:jar/libsvm.jar:jar/mysql-connector-java-5.0.8-bin.jar"

CLASSNAMES[1]="weka.classifiers.bayes.BayesNet"
CLASSNAMES[2]="weka.classifiers.bayes.NaiveBayes"
CLASSNAMES[3]="weka.classifiers.functions.Logistic"
CLASSNAMES[4]="weka.classifiers.functions.MultilayerPerceptron"
CLASSNAMES[5]="weka.classifiers.functions.LibSVM"
CLASSNAMES[6]="weka.classifiers.lazy.KStar"
CLASSNAMES[7]="weka.classifiers.meta.AdaBoostM1"
CLASSNAMES[8]="weka.classifiers.meta.Bagging"
CLASSNAMES[9]="weka.classifiers.meta.Dagging"
CLASSNAMES[10]="weka.classifiers.meta.Decorate"
CLASSNAMES[11]="weka.classifiers.meta.LogitBoost"
CLASSNAMES[12]="weka.classifiers.trees.ADTree"
CLASSNAMES[13]="weka.classifiers.trees.J48"
CLASSNAMES[14]="weka.classifiers.trees.RandomForest"

BAYESNET="-D -Q weka.classifiers.bayes.net.search.local.K2 -- -P 1 -S BAYES -E weka.classifiers.bayes.net.estimate.SimpleEstimator -- -A 0.5"
NAIVEBAYES="" 
LOGISTIC="-R 1.0E-8 -M -1" 
MULTILAYERPERCEPTRON="-L 0.3 -M 0.2 -N 500 -V 0 -S 0 -E 20 -H a" 
LIBSVM="-S 0 -K 2 -D 3 -G 0.0 -R 0.0 -N 0.5 -M 40.0 -C 1.0 -E 0.0010 -P 0.1" 
KSTAR="-B 20 -M a" 
ADABOOST="-P 100 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump" 
BAGGING="-P 100 -S 1 -I 10 -W weka.classifiers.trees.REPTree -- -M 2 -V 0.0010 -N 3 -S 1 -L -1" 
DAGGING="-F 10 -S 1 -W weka.classifiers.functions.SMO -- -C 1.0 -L 0.0010 -P 1.0E-12 -N 0 -V -1 -W 1 -K \"weka.classifiers.functions.supportVector.PolyKernel -C 250007 -E 1.0\""
DECORATE="-E 10 -R 1.0 -S 1 -I 10 -W weka.classifiers.trees.J48 -- -C 0.25 -M 2" 
LOGITBOOST="-P 100 -F 0 -R 1 -L -1.7976931348623157E308 -H 1.0 -S 1 -I 10 -W weka.classifiers.trees.DecisionStump" 
ADTREE="-B 10 -E -3"
J48="-C 0.25 -M 2"
RANDOMFOREST="-I 10 -K 0 -S 1"

MODELOPTIONS[1]=$BAYESNET
MODELOPTIONS[2]=$NAIVEBAYES
MODELOPTIONS[3]=$LOGISTIC 
MODELOPTIONS[4]=$MULTILAYERPERCEPTRON
MODELOPTIONS[5]=$LIBSVM
MODELOPTIONS[6]=$KSTAR
MODELOPTIONS[7]=$ADABOOST
MODELOPTIONS[8]=$BAGGING
MODELOPTIONS[9]=$DAGGING
MODELOPTIONS[10]=$DECORATE
MODELOPTIONS[11]=$LOGITBOOST
MODELOPTIONS[12]=$ADTREE
MODELOPTIONS[13]=$J48
MODELOPTIONS[14]=$RANDOMFOREST


# LEARNING
CORPUS=$1
FUNC=$2

ARFF=weka/$CORPUS.arff
TEST=$ARFF


for i in $(seq 1 14);
do
    MODELOPTION=${MODELOPTIONS[i]}
    CLASSNAME=${CLASSNAMES[i]}
    MODEL="model/$CORPUS.$CLASSNAME.model"
    RESULT="result/$CORPUS.$CLASSNAME.result"

    if [ "$FUNC" == "all" ] || [ "$FUNC" == "learn" ]; then
        echo "Learning $CLASSNAME..."
        echo $JAVA $CLASSNAME -i -t $ARFF -d $MODEL $MODELOPTION
        echo 
        if [ $i -gt 2 ] && [ $i -lt 7 ]; then
            echo "Skipping $MODEL learning..."
            echo
            echo
            sleep 1
        elif [ $i -eq 9 ]; then
            echo $JAVA $CLASSNAME -i -t $ARFF -d $MODEL $MODELOPTION > ./temp.sh
            chmod +x ./temp.sh
            ./temp.sh > $RESULT
            rm -rf ./temp.sh
        elif [ $i -gt 9 ] && [ $i -lt 11 ]; then
            echo "Skipping $MODEL learning..."
            echo
            echo
            sleep 1
        else
            $JAVA $CLASSNAME -i -t $ARFF -d $MODEL $MODELOPTION > $RESULT
        fi

    elif [ "$FUNC" == "all" ] || [ "$FUNC" == "eval" ]; then
        echo "Evaluating $CLASSNAME..."
        $JAVA $CLASSNAME -T $TEST -i -l $MODEL $MODELOPTION > $RESULT
    else
        print_usage
        exit
    fi
done

