#!/bin/bash
DIR=$1
NUM=$2
for i in $(seq 1 $NUM); do clear; ls -alh $DIR; sleep 1; done
