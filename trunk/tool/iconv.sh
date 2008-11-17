#!/bin/bash
if [ $# == 2 ]; then
    src_dir=$1
    dest_dir=$2
    file_names=`ls $src_dir`
    mkdir -p $dest_dir
    for filename in $file_names; do
	iconv -f UNICODE -t UTF8 $src_dir/$filename > $dest_dir/$filename
    done
else
    echo '입력폴더의 모든 파일들을 출력폴더에 UTF8으로 인코딩하여 저장한다.'
    echo 'iconv.sh 입력폴더 출력폴더'
fi
