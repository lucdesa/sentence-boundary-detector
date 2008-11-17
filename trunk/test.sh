#!/bin/bash
export CLASSPATH=$CLASSPATH:jar/weka.jar:jar/libsvm.jar
JAVA="java -Xmx2048m -classpath jar/weka.jar:jar/libsvm.jar:jar/mysql-connector-java-5.0.8-bin.jar"
CLASSNAME="weka.classifiers.trees.J48"
ARFF="weka/example.arff"
MODEL="model/example.model"
J48="-C 0.25 -M 2"
MODELOPTION=$J48
set -v
$JAVA $CLASSNAME -i -t $ARFF -d $MODEL $MODELOPTION
