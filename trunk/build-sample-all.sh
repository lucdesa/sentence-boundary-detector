#!/bin/bash

function print_usage() {
    echo "./build-all.sh [all|tenfolds|dict|instance|weka|maxent]"
}

if [ $# != 1 ]; then
    print_usage
    exit
fi

# 원본 코퍼스를 10폴딩을 위해서 나누어서 다시 폴딩, weka의 경우 10폴드를 지원하므로 maxent에서만 사용됨
# IN:        corpus/corpus-name/*.raw
# OUT:        tenfolds/corpus-name/*.[split|learn|eval]
if [ "$1" == "all" ] || [ "$1" == "tenfolds" ]; then
    echo "1. SPLITTING & FOLDING INSTANCES"
    mkdir -p tenfolds/sample
    ./build-tenfolds.sh sample split tenfolds
    ./build-tenfolds.sh sample folding tenfolds
fi
# dict 폴더 아래에 컴파일된 사전을 생성
if [ "$1" == "all" ] || [ "$1" == "dict" ]; then
    echo 2. BUILDING DICTIONARIES
    mkdir -p dict/sample
    ./build-dict.sh sample tenfolds dict/sample 1 yes no
fi
# 폴딩된 파일을 하나의 학습용 집합으로 생성
if [ "$1" == "all" ] || [ "$1" == "instance" ]; then
    echo 3. BUILD INSTANCES
    mkdir -p dict/sample
    ./build-instance.sh sample tenfolds dict/sample 1 yes no weka
    ./build-instance.sh sample tenfolds dict/sample 1 yes no maxent
fi
# 학습집합으로부터 모델생성 및 검증
if [ "$1" == "all" ] || [ "$1" == "weka" ]; then
    echo "4. LEARNING "$1" MODELS"
    mkdir -p log/sample
    ./build-weka-model.sh sample all
fi

if [ "$1" == "all" ] || [ "$1" == "maxent" ]; then
    echo "5. LEARNING "$1" MODELS"
    mkdir -p log/sample
    ./build-maxent-model.sh sample all
fi

