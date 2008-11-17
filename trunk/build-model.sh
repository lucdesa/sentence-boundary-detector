#!/bin/bash

function printUsage {
    echo 'Usage: ./build-model.sh [instance-filename] [learning-filename] [output-filename] [weka|maxent]'
    echo './build-model.sh weka weka/sejong.arff model/sejong_weka_j48.model weka/sejong_j48.out'
    echo './build-model.sh weka weka/pentree.arff model/pentree_weka_j48.model weka/pentree_j48.out'
    echo './build-model.sh maxent maxent/sejong.maxent model/sejong_maxent.model maxent/sejong_maxent.out'
    echo './build-model.sh maxent maxent/pentree.maxent model/pentree_maxent.model maxent/pentree_maxent.out'
}

if [ $# == 4 ]; then
    classifier=$1
    instance_path=$2
    model_path=$3
    output_path=$4
    if [ $classifier == weka ]; then
        java -Xmx2048m -classpath jar/weka.jar:jar/libsvm.jar weka.classifiers.trees.J48 -C 0.25 -M 2 -t $instance_path -d $model_path > $output_path
    elif [ $classifier == maxent ]; then
        maxent -v -m$model_path -i200 -g3.5 $instance_path > $output_path
    else
        printUsage
    fi
else
    printUsage
fi

