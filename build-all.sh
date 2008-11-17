#!/bin/bash

function print_usage() {
    echo "./build-all.sh [all|tenfolds|dict|instance|weka|maxent] [sejong|pentree]"
}

if [ $# != 2 ]; then
    print_usage
    exit
fi

# 원본 코퍼스를 10폴딩을 위해서 나누어서 다시 폴딩, weka의 경우 10폴드를 지원하므로 maxent에서만 사용됨
# IN:        corpus/corpus-name/*.raw
# OUT:        tenfolds/corpus-name/*.[split|learn|eval]
if [ "$1" == "all" ] || [ "$1" == "tenfolds" ]; then
    echo "1. SPLITTING & FOLDING INSTANCES"
    if [ "$2" == "sejong" ]; then
        rm -rf tenfolds/sejong
        mkdir -p tenfolds/sejong
        ./build-tenfolds.sh sejong split tenfolds
        ./build-tenfolds.sh sejong folding tenfolds
    elif [ "$2" == "pentree" ]; then
        rm -rf tenfolds/pentree
        mkdir -p tenfolds/pentree
        ./build-tenfolds.sh pentree split tenfolds
        ./build-tenfolds.sh pentree folding tenfolds
    fi
fi
# dict 폴더 아래에 컴파일된 사전을 생성
if [ "$1" == "all" ] || [ "$1" == "dict" ]; then
    echo 2. BUILDING DICTIONARIES
    if [ "$2" == "sejong" ]; then
        rm -rf dict/sejong
        mkdir -p dict/sejong
        ./build-dict.sh sejong tenfolds dict/sejong 1 yes no
    elif [ "$2" == "pentree" ]; then
        rm -rf dict/pentree
        mkdir -p dict/pentree
        ./build-dict.sh pentree tenfolds dict/pentree 0 no yes
    fi
fi
# 폴딩된 파일을 하나의 학습용 집합으로 생성
if [ "$1" == "all" ] || [ "$1" == "instance" ]; then
    echo 3. BUILD INSTANCES
    if [ "$2" == "sejong" ]; then
        ./build-instance.sh sejong tenfolds dict/sejong 1 yes no weka
        ./build-instance.sh sejong tenfolds dict/sejong 1 yes no maxent
    elif [ "$2" == "pentree" ]; then
        ./build-instance.sh pentree tenfolds dict/pentree 0 no yes weka
        ./build-instance.sh pentree tenfolds dict/pentree 0 no yes maxent
    fi
fi
# 학습집합으로부터 웨카 모델생성 및 검증
if [ "$1" == "all" ] || [ "$1" == "weka" ]; then
    echo "4. LEARNING "$1" MODELS"
    if [ "$2" == "sejong" ]; then
        ./build-weka-model.sh sejong all
    elif [ "$2" == "pentree" ]; then
        ./build-weka-model.sh pentree all
    fi
fi
# 학습집합으로부터 맥센트  모델생성 및 검증
if [ "$1" == "all" ] || [ "$1" == "maxent" ]; then
    echo "5. LEARNING "$1" MODELS"
    if [ "$2" == "sejong" ]; then
        mkdir -p log/sejong
        ./build-maxent-model.sh sejong all
    elif [ "$2" == "pentree" ]; then
        mkdir -p log/pentree
        ./build-maxent-model.sh pentree all
    fi
fi

# echo 5. SENTENCE BOUNDARY DETECTION
# python MaxentBasedSBD.py model/maxent.model 0 no yes 0.8 corpus/pentree/single.txt seg > single.out

